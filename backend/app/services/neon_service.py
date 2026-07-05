import os
import json
from typing import Optional, Any
import asyncpg
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class NeonService:
    """
    Neon PostgreSQL Service
    Full database operations for AmkyawDev Tools
    """
    
    def __init__(self):
        self.database_url = os.getenv("NEON_DATABASE_URL", os.getenv("DATABASE_URL", ""))
        self.pool: Optional[asyncpg.Pool] = None
        self._connected = False

    async def connect(self) -> bool:
        """Connect to Neon PostgreSQL"""
        if not self.database_url:
            logger.warning("No Neon DATABASE_URL configured")
            return False
            
        if self.pool is not None:
            return self._connected
            
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            await self._init_tables()
            self._connected = True
            logger.info("Connected to Neon PostgreSQL")
            return True
        except Exception as e:
            logger.error(f"Neon connection failed: {e}")
            self.pool = None
            self._connected = False
            return False

    async def _init_tables(self):
        """Initialize all tables"""
        async with self.pool.acquire() as conn:
            # Users table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100),
                    is_active BOOLEAN DEFAULT TRUE,
                    is_superuser BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Conversations table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    session_id VARCHAR(100) NOT NULL,
                    title VARCHAR(255) DEFAULT 'New Conversation',
                    channel VARCHAR(20) DEFAULT 'web',
                    model_used VARCHAR(100),
                    total_tokens INTEGER DEFAULT 0,
                    message_count INTEGER DEFAULT 0,
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Messages table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
                    role VARCHAR(20) NOT NULL,
                    content TEXT NOT NULL,
                    task_type VARCHAR(20) DEFAULT 'chat',
                    tokens_used INTEGER DEFAULT 0,
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Knowledge base table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_base (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    skill VARCHAR(100),
                    title VARCHAR(255),
                    content TEXT NOT NULL,
                    content_hash VARCHAR(64),
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Skills table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    context_prompt TEXT NOT NULL,
                    category VARCHAR(50) DEFAULT 'general',
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Files table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS uploaded_files (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    conversation_id INTEGER REFERENCES conversations(id) ON DELETE SET NULL,
                    file_name VARCHAR(255) NOT NULL,
                    file_size INTEGER NOT NULL,
                    file_type VARCHAR(100),
                    storage_path TEXT NOT NULL,
                    is_processed BOOLEAN DEFAULT FALSE,
                    metadata JSONB DEFAULT '{}',
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Telegram sessions table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS telegram_sessions (
                    id SERIAL PRIMARY KEY,
                    telegram_chat_id VARCHAR(50) UNIQUE NOT NULL,
                    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                    username VARCHAR(100),
                    message_count INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Indexes
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_skill ON knowledge_base(skill)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_telegram_chat_id ON telegram_sessions(telegram_chat_id)")
            
            logger.info("Neon tables initialized")

    # ============ CONVERSATION METHODS ============
    
    async def create_conversation(
        self,
        session_id: str,
        user_id: Optional[int] = None,
        title: str = "New Conversation",
        channel: str = "web",
        model: Optional[str] = None
    ) -> Optional[int]:
        """Create a new conversation"""
        if not self.pool and not await self.connect():
            return None
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """INSERT INTO conversations (user_id, session_id, title, channel, model_used)
                   VALUES ($1, $2, $3, $4, $5) RETURNING id""",
                user_id, session_id, title, channel, model
            )
            return row['id'] if row else None

    async def save_message(
        self,
        conversation_id: int,
        role: str,
        content: str,
        task_type: str = "chat",
        tokens: int = 0,
        metadata: dict = None
    ):
        """Save a message to conversation"""
        if not self.pool and not await self.connect():
            return
        async with self.pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO messages (conversation_id, role, content, task_type, tokens_used, metadata)
                   VALUES ($1, $2, $3, $4, $5, $6)""",
                conversation_id, role, content, task_type, tokens, json.dumps(metadata or {})
            )

    async def get_conversation_history(
        self,
        session_id: str,
        limit: int = 50
    ) -> list[dict]:
        """Get conversation history by session_id"""
        if not self.pool and not await self.connect():
            return []
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """SELECT m.role, m.content, m.task_type, m.created_at
                   FROM messages m
                   JOIN conversations c ON m.conversation_id = c.id
                   WHERE c.session_id = $1
                   ORDER BY m.created_at ASC
                   LIMIT $2""",
                session_id, limit
            )
            return [dict(row) for row in rows]

    async def get_or_create_conversation(self, session_id: str) -> Optional[int]:
        """Get existing conversation or create new one"""
        if not self.pool and not await self.connect():
            return None
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id FROM conversations WHERE session_id = $1",
                session_id
            )
            if row:
                return row['id']
            row = await conn.fetchrow(
                "INSERT INTO conversations (session_id) VALUES ($1) RETURNING id",
                session_id
            )
            return row['id'] if row else None

    # ============ KNOWLEDGE METHODS ============
    
    async def save_knowledge(
        self,
        content: str,
        title: Optional[str] = None,
        skill: Optional[str] = None,
        user_id: Optional[int] = None,
        metadata: dict = None
    ) -> Optional[int]:
        """Save knowledge entry"""
        if not self.pool and not await self.connect():
            return None
        import hashlib
        content_hash = hashlib.md5(content.encode()).hexdigest()
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """INSERT INTO knowledge_base (user_id, skill, title, content, content_hash, metadata)
                   VALUES ($1, $2, $3, $4, $5, $6) RETURNING id""",
                user_id, skill, title, content, content_hash, json.dumps(metadata or {})
            )
            return row['id'] if row else None

    async def search_knowledge(
        self,
        query: str,
        skill: Optional[str] = None,
        user_id: Optional[int] = None,
        limit: int = 10
    ) -> list[dict]:
        """Search knowledge base"""
        if not self.pool and not await self.connect():
            return []
        async with self.pool.acquire() as conn:
            if skill:
                rows = await conn.fetch(
                    """SELECT id, title, content, skill, created_at
                       FROM knowledge_base
                       WHERE (title ILIKE $1 OR content ILIKE $1) AND skill = $2
                       ORDER BY created_at DESC LIMIT $3""",
                    f"%{query}%", skill, limit
                )
            else:
                rows = await conn.fetch(
                    """SELECT id, title, content, skill, created_at
                       FROM knowledge_base
                       WHERE title ILIKE $1 OR content ILIKE $1
                       ORDER BY created_at DESC LIMIT $2""",
                    f"%{query}%", limit
                )
            return [dict(row) for row in rows]

    # ============ TELEGRAM METHODS ============
    
    async def upsert_telegram_session(
        self,
        chat_id: str,
        username: Optional[str] = None
    ) -> bool:
        """Create or update telegram session"""
        if not self.pool and not await self.connect():
            return False
        async with self.pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO telegram_sessions (telegram_chat_id, username)
                   VALUES ($1, $2)
                   ON CONFLICT (telegram_chat_id) DO UPDATE SET
                   username = EXCLUDED.username,
                   message_count = telegram_sessions.message_count + 1""",
                chat_id, username
            )
            return True

    # ============ SKILLS METHODS ============
    
    async def save_skill(
        self,
        name: str,
        context_prompt: str,
        description: Optional[str] = None,
        category: str = "general",
        user_id: Optional[int] = None
    ) -> Optional[int]:
        """Save a skill"""
        if not self.pool and not await self.connect():
            return None
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """INSERT INTO skills (user_id, name, description, context_prompt, category)
                   VALUES ($1, $2, $3, $4, $5) RETURNING id""",
                user_id, name, description, context_prompt, category
            )
            return row['id'] if row else None

    async def list_skills(self, user_id: Optional[int] = None) -> list[dict]:
        """List all skills"""
        if not self.pool and not await self.connect():
            return []
        async with self.pool.acquire() as conn:
            if user_id:
                rows = await conn.fetch(
                    "SELECT * FROM skills WHERE user_id = $1 ORDER BY usage_count DESC",
                    user_id
                )
            else:
                rows = await conn.fetch(
                    "SELECT * FROM skills ORDER BY usage_count DESC"
                )
            return [dict(row) for row in rows]

    # ============ UTILITY METHODS ============
    
    async def close(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            self.pool = None
            self._connected = False
            logger.info("Neon connection closed")

    def is_connected(self) -> bool:
        return self._connected


NeonService = PostgresService = NeonService
