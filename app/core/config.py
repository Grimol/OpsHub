import os

from pydantic import BaseModel


class Settings(BaseModel):
    # fichier SQLite local (à la racine du conteneur / du projet)
    SQLITE_PATH: str = os.getenv("SQLITE_PATH", "opshub.db")

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.SQLITE_PATH}"


settings = Settings()
