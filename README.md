uv init
uv venv
.venv\Scripts\activate 
uv add fastapi uvicorn sqlalchemy psycopg2-binary fastapi-pagination

Certifique que o postgresql local esteja desativado para conseguir logar no postgresql do docker -> net stop postgresql-x64-17

uv add alembic asyncpg

make create-migration d="init"
make run-migration

uv add pydantic_settings