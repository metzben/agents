import sqlite3
from config import Config
from .base_models import User
from typing import Optional


class BaseService:
    def __init__(self, conn: sqlite3.Connection, config: Config):
        self.conn = conn
        self.config = config

    def test(self) -> dict:
        return {"base project": f"Base project working...{self.config.github_url}"}

    def get_user(self, username: str) -> Optional[User]:
        return User(name=username)
