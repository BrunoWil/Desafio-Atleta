from pydantic import Field
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    database_url: str = Field(default='postgresql+asyncpg://Atleta:Atleta@localhost/Atleta_db')
    
settings = Settings()