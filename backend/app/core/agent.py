from typing import Optional
from app.services.openrouter_service import OpenRouterService
from app.core.skill_loader import SkillLoader
from app.core.context_manager import ContextManager
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class CoderAgent:
    """AI coder agent that orchestrates LLM calls with dynamic skill injection."""

    def __init__(
        self,
        openrouter_service: OpenRouterService,
        skill_loader: SkillLoader,
        context_manager: Optional[ContextManager] = None,
    ):
        self.llm = openrouter_service
        self.skills = skill_loader
        self.context = context_manager or ContextManager()

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------

    async def chat(
        self,
        messages: list[dict],
        skills: Optional[list[str]] = None,
        model: Optional[str] = None,
    ) -> dict:
        """Chat with the agent, optionally loading `.amkyaw` skills."""

        skill_prompts: list[str] = []
        if skills:
            for skill_name in skills:
                skill_content = self.skills.load_skill(skill_name)
                if skill_content:
                    skill_prompts.append(skill_content)

        system_prompt = self._build_system_prompt(skill_prompts)

        full_messages = [{"role": "system", "content": system_prompt}]
        full_messages.extend(self.context.get_context_window(messages))

        response = await self.llm.chat_completion(
            messages=full_messages, model=model
        )

        assistant_message = response["choices"][0]["message"]["content"]
        tokens_used = response.get("usage", {}).get("total_tokens", 0)

        self.context.add_turn("assistant", assistant_message)

        return {
            "message": assistant_message,
            "skills_used": skills or [],
            "tokens_used": tokens_used,
        }

    # ------------------------------------------------------------------
    # Code Generation
    # ------------------------------------------------------------------

    async def generate_code(
        self,
        prompt: str,
        language: str = "python",
        skills: Optional[list[str]] = None,
        context: Optional[str] = None,
    ) -> dict:
        """Generate production-quality code with optional skill injection."""

        skill_prompts: list[str] = []
        if skills:
            for skill_name in skills:
                skill_content = self.skills.load_skill(skill_name)
                if skill_content:
                    skill_prompts.append(skill_content)

        system_prompt = self._build_code_generation_prompt(
            language=language, skill_prompts=skill_prompts
        )

        user_prompt = prompt
        if context:
            user_prompt = f"Context:\n{context}\n\nTask:\n{prompt}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = await self.llm.chat_completion(messages=messages)
        content = response["choices"][0]["message"]["content"]

        code, explanation = self._extract_code_and_explanation(content, language)

        return {
            "code": code,
            "language": language,
            "explanation": explanation,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_system_prompt(self, skill_prompts: list[str]) -> str:
        """Build the system prompt with loaded skills."""
        base_prompt = """You are an AmkyawDev Tools AI Agent — an expert software developer and coding assistant.
You help users write, debug, explain, and optimize code across many languages and frameworks.

Guidelines:
- Write clean, readable, well-documented code
- Use best practices and design patterns
- Handle errors gracefully
- Provide context-aware suggestions
- When generating code, include necessary imports and type hints
- Always explain complex decisions
"""

        if skill_prompts:
            skills_text = "\n\n---\n\n".join(skill_prompts)
            base_prompt += f"\n\n## Loaded Skills\n\n{skills_text}"

        return base_prompt

    def _build_code_generation_prompt(
        self, language: str, skill_prompts: list[str]
    ) -> str:
        """Build the code generation system prompt."""
        prompt = (
            f"You are an expert {language} developer. "
            f"Write production-quality {language} code with imports, "
            f"type hints, docstrings, and error handling."
        )

        if skill_prompts:
            skills_text = "\n\n---\n\n".join(skill_prompts)
            prompt += f"\n\n## Special Instructions\n\n{skills_text}"

        return prompt

    @staticmethod
    def _extract_code_and_explanation(
        content: str, language: str
    ) -> tuple[str, str]:
        """Extract code from markdown code blocks and return (code, explanation)."""
        import re

        # Try language-specific code block first
        code_block_pattern = rf"```(?:{language})?\s*\n(.*?)```"
        matches = re.findall(code_block_pattern, content, re.DOTALL)

        if matches:
            code = matches[0].strip()
            explanation = re.sub(
                code_block_pattern, "", content, flags=re.DOTALL
            ).strip()
            return code, explanation

        # Fallback: generic code block
        generic_pattern = r"```\s*\n(.*?)```"
        matches = re.findall(generic_pattern, content, re.DOTALL)

        if matches:
            code = matches[0].strip()
            explanation = re.sub(
                generic_pattern, "", content, flags=re.DOTALL
            ).strip()
            return code, explanation

        return content, ""
