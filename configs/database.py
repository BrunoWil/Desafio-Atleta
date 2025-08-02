from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from configs.settings import settings

from sqlalchemy.pool import NullPool 


# Criação da engine assíncrona
engine = create_async_engine(
    settings.database_url,
    echo=False,
    # pool_pre_ping=True,
    # poolclass=NullPool  # ← evita reuso de conexões, ideal em contextos async
)

# Criador de sessões assíncronas
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,

)

# Dependência para injeção de sessão no FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
