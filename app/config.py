
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.database_url = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://postgres:postgres@localhost:5432/library",
        )


settings = Settings()
