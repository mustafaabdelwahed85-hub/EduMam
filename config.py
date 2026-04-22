import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def build_database_uri():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return f"sqlite:///{BASE_DIR / 'mamba.db'}"

    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg2://", 1)

    if database_url.startswith("postgresql://") and "+" not in database_url.split("://", 1)[0]:
        return database_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    return database_url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mamba-dev-secret-key")
    SQLALCHEMY_DATABASE_URI = build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }
