from sqlmodel import SQLModel, create_engine

from pipeline.database import models  # noqa: F401 - all models are registered
from pipeline.ui.config import settings

engine = create_engine(f"sqlite:///{settings.database_path}")


def init_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
