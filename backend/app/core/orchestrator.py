"""
AI Agent Orchestrator
Main agent logic & decision making for all input channels.
"""
import asyncio
import json
import time
from typing import Optional, Any
from datetime import datetime
from enum import Enum

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class InputChannel(Enum):
    WEB = "web"
    TELEGRAM = "telegram"
    CLI = "cli"
    VOICE = "voice"
    API = "api"


class TaskType(Enum):
    CHAT = "chat"
    CODE = "code"
    SCRAPE = "scrape"
    SEARCH = "search"
    EXPORT = "export"
    ANALYZE = "analyze"


class Orchestrator:
    """
    AI Agent Orchestrator - Central brain that coordinates:
    - LLM services (OpenRouter, NVIDIA NIM)
    - Memory (Neon PostgreSQL)
    - Web scraping (Browserless)
    - Event streaming (Kafka)
    """

    def __init__(
        self,
        llm_service=None,
        neon_service=None,
        browserless_service=None,
        kafka_service=None,
        skill_loader=None,
    ):
        self.llm = llm_service
        self.neon = neon_service
        self.browserless = browserless_service
        self.kafka = kafka_service
        self.skill_loader = skill_loader
        self._sessions: dict[str, dict] = {}

    async def process(
        self,
        message: str,
        channel: InputChannel = InputChannel.WEB,
        session_id: Optional[str] = None,
        skills: Optional[list[str]] = None,
        context: Optional[dict] = None,
    ) -> dict:
        start_time = time.time()
        session_id = session_id or f"{channel.value}_{int(time.time())}"

        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "channel": channel.value,
                "created_at": datetime.utcnow().isoformat(),
                "turns": 0,
            }
        self._sessions[session_id]["turns"] += 1

        ctx = await self._build_context(session_id, context)
        task_type = self._detect_task(message, context)

        if self.kafka:
            await self.kafka.send_event(
                event_type="user_message",
                data={
                    "session_id": session_id,
                    "channel": channel.value,
                    "task_type": task_type.value,
                    "message_length": len(message),
                },
            )

        try:
            if task_type == TaskType.SCRAPE:
                result = await self._handle_scrape(message, context)
            elif task_type == TaskType.SEARCH:
                result = await self._handle_search(message, ctx)
            else:
                result = await self._handle_chat(message, ctx, skills)

            await self._save_interaction(session_id, message, result["response"])

            duration = time.time() - start_time
            logger.info(f"Processed {task_type.value} in {duration:.2f}s for session {session_id}")

            return {
                "response": result["response"],
                "task_type": task_type.value,
                "session_id": session_id,
                "duration_ms": int(duration * 1000),
                "metadata": result.get("metadata", {}),
                "actions": result.get("actions", []),
            }

        except Exception as e:
            logger.error(f"Orchestrator error: {e}")
            raise

    async def _build_context(self, session_id: str, additional_context: Optional[dict]) -> dict:
        ctx = {"session_id": session_id, "timestamp": datetime.utcnow().isoformat()}

        if self.neon:
            try:
                history = await self.neon.get_conversation(session_id, limit=10)
                ctx["history"] = history
            except Exception as e:
                logger.warning(f"Failed to load history: {e}")

        if additional_context:
            ctx.update(additional_context)

        return ctx

    def _detect_task(self, message: str, context: Optional[dict]) -> TaskType:
        msg_lower = message.lower()

        if any(x in msg_lower for x in ["write code", "generate code", "create function", "implement"]):
            return TaskType.CODE
        if any(x in msg_lower for x in ["scrape", "fetch", "crawl", "get content from"]):
            return TaskType.SCRAPE
        if any(x in msg_lower for x in ["search", "find", "lookup"]):
            return TaskType.SEARCH
        if any(x in msg_lower for x in ["export", "download", "save as"]):
            return TaskType.EXPORT
        if any(x in msg_lower for x in ["analyze", "review", "explain"]):
            return TaskType.ANALYZE

        return TaskType.CHAT

    async def _handle_chat(self, message: str, context: dict, skills: Optional[list[str]]) -> dict:
        skill_prompts = []
        if skills and self.skill_loader:
            for skill_name in skills:
                content = self.skill_loader.load_skill(skill_name)
                if content:
                    skill_prompts.append(content)

        sys_prompt = self._build_system_prompt(skill_prompts)
        messages = [{"role": "system", "content": sys_prompt}]

        if context.get("history"):
            for turn in context["history"]:
                messages.append({"role": turn.get("role", "user"), "content": turn.get("content", "")})

        messages.append({"role": "user", "content": message})

        if not self.llm:
            return {"response": "LLM service not configured.", "metadata": {}, "actions": []}

        response = await self.llm.chat_completion(messages=messages)

        return {
            "response": response["choices"][0]["message"]["content"],
            "metadata": {"model": response.get("model", "unknown"), "usage": response.get("usage", {})},
            "actions": [],
        }

    async def _handle_scrape(self, message: str, context: dict) -> dict:
        if not self.browserless:
            return {"response": "Web scraping service not configured.", "metadata": {}, "actions": []}

        import re
        url_match = re.search(r"https?://[^\s]+", message)

        if not url_match:
            return {"response": "Please provide a valid URL to scrape.", "metadata": {}, "actions": []}

        url = url_match.group(0)
        content = await self.browserless.fetch_page(url)

        if not content:
            return {"response": f"Failed to fetch content from {url}", "metadata": {}, "actions": []}

        if self.llm:
            messages = [
                {"role": "system", "content": "Summarize the following web page content concisely."},
                {"role": "user", "content": f"URL: {url}\n\nContent:\n{content[:8000]}"},
            ]
            response = await self.llm.chat_completion(messages=messages)
            summary = response["choices"][0]["message"]["content"]
        else:
            summary = content[:2000] + "..." if len(content) > 2000 else content

        return {
            "response": f"**Scraped from:** {url}\n\n{summary}",
            "metadata": {"url": url, "content_length": len(content)},
            "actions": [{"type": "link", "url": url, "label": "Open original"}],
        }

    async def _handle_search(self, message: str, context: dict) -> dict:
        if not self.neon:
            return {"response": "Knowledge base not configured.", "metadata": {}, "actions": []}

        query = message.replace("search", "").replace("find", "").replace("lookup", "").strip()
        results = await self.neon.search_knowledge(query=query, limit=5)

        if not results:
            return {"response": f"No results found for: {query}", "metadata": {"query": query}, "actions": []}

        response_text = f"**Search results for:** {query}\n\n"
        for i, r in enumerate(results, 1):
            response_text += f"{i}. **{r.get('title', 'Untitled')}**\n{r.get('content', '')[:200]}...\n\n"

        return {"response": response_text, "metadata": {"query": query, "result_count": len(results)}, "actions": []}

    def _build_system_prompt(self, skill_prompts: list[str]) -> str:
        base = """You are AmkyawDev Tools AI Agent - an expert software developer and coding assistant.

Guidelines:
- Write clean, readable, well-documented code
- Use best practices and design patterns
- Be concise but thorough
- Follow security best practices"""

        if skill_prompts:
            base += "\n\n## Loaded Skills\n\n" + "\n\n---\n\n".join(skill_prompts)

        return base

    async def _save_interaction(self, session_id: str, user_message: str, agent_response: str):
        if not self.neon:
            return
        try:
            await self.neon.save_conversation(session_id=session_id, role="user", content=user_message)
            await self.neon.save_conversation(session_id=session_id, role="assistant", content=agent_response)
        except Exception as e:
            logger.warning(f"Failed to save conversation: {e}")

    async def get_session_info(self, session_id: str) -> dict:
        return self._sessions.get(session_id, {})

    async def clear_session(self, session_id: str):
        if session_id in self._sessions:
            del self._sessions[session_id]
