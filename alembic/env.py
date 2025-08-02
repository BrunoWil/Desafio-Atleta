#Importações necessárias para o funcionamento do Alembic com SQLAlchemy assíncrono
import asyncio
from logging.config import fileConfig

from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool

from alembic import context

# Importar o modelo base e todos os modelos para garantir que as tabelas sejam detectadas
from contrib.models import BaseModel
from contrib.repository.models import *

# Configuração do Alembic obtida do arquivo alembic.ini
config = context.config

# Configurar logging se o arquivo de configuração estiver especificado
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados do modelo base - contém informações de todas as tabelas SQLAlchemy
# Isso permite ao Alembic detectar automaticamente mudanças no schema
target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """
    Executa migrações no modo 'offline'.
    
    No modo offline, o Alembic não se conecta ao banco de dados,
    apenas gera scripts SQL que podem ser executados posteriormente.
    Útil para ambientes onde não há acesso direto ao banco.
    """
    # Obtém a URL de conexão do banco do arquivo de configuração
    url = config.get_main_option("sqlalchemy.url")
    
    # Configura o contexto do Alembic para modo offline
    context.configure(
        url=url,                          # URL de conexão com o banco
        target_metadata=target_metadata,  # Metadados das tabelas
        literal_binds=True,              # Usar valores literais em vez de parâmetros
        dialect_opts={"paramstyle": "named"},  # Estilo de parâmetros nomeados
    )

    # Executa as migrações dentro de uma transação
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Executa as migrações usando uma Connection ativa.
    
    Esta função é chamada dentro do contexto assíncrono para
    executar as migrações de forma síncrona usando run_sync().
    
    Args:
        connection: Conexão ativa com o banco de dados
    """
    # Configura o contexto do Alembic com a conexão fornecida
    context.configure(
        connection=connection,           # Conexão ativa com o banco
        target_metadata=target_metadata, # Metadados das tabelas
    )

    # Executa as migrações dentro de uma transação
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Cria uma engine assíncrona e executa as migrações.
    
    Esta função é responsável por:
    1. Criar uma engine assíncrona usando as configurações do alembic.ini
    2. Estabelecer uma conexão com o banco de dados
    3. Executar as migrações de forma síncrona usando run_sync()
    4. Fechar a engine adequadamente
    """
    # Cria uma engine assíncrona baseada na configuração do Alembic
    connectable = async_engine_from_config(
        # Obtém as configurações da seção [alembic] do arquivo .ini
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",    # Prefixo para configurações do SQLAlchemy
        poolclass=pool.NullPool, # Usa NullPool para evitar problemas com conexões assíncronas
    )

    # Estabelece conexão assíncrona com o banco
    async with connectable.connect() as connection:
        # Executa as migrações de forma síncrona dentro do contexto assíncrono
        # run_sync() permite executar código síncrono em um contexto assíncrono
        await connection.run_sync(do_run_migrations)
    
    # Fecha a engine e libera recursos
    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Executa migrações no modo 'online'.
    
    No modo online, o Alembic se conecta diretamente ao banco de dados
    e executa as migrações. Este é o modo padrão e mais comum de uso.
    
    Para aplicações assíncronas, usa asyncio.run() para executar
    a função assíncrona run_async_migrations().
    """
    # Executa a função assíncrona de migrações usando asyncio
    # asyncio.run() cria um novo event loop e executa a corrotina
    asyncio.run(run_async_migrations())


# Determina qual modo de execução usar baseado na configuração
if context.is_offline_mode():
    # Modo offline: gera scripts SQL sem conectar ao banco
    run_migrations_offline()
else:
    # Modo online: conecta ao banco e executa migrações diretamente
    run_migrations_online()