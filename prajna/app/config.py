import os
from pydantic import BaseModel

class Settings(BaseModel):
    FALKORDB_HOST: str = os.getenv("FALKORDB_HOST", "localhost")
    FALKORDB_PORT: int = int(os.getenv("FALKORDB_PORT", "6379"))
    DEFAULT_TENANT: str = os.getenv("DEFAULT_TENANT", "kirana")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ROUTER_MODEL: str = os.getenv("ROUTER_MODEL", "gpt-4o-mini")
    ACTOR_MODEL: str = os.getenv("ACTOR_MODEL", "gpt-4o")

settings = Settings()
