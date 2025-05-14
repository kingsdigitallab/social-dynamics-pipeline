from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    images_dir: Path = Path("tests/data/public/images/test_pdf_1")
    images_url_base: Path = Path("/images")
    demo_mode: bool = True

    project_root: Path = Path(__file__).resolve().parents[2]
    database_path: Path = project_root / "socdyn_db.db"

    class Config:
        env_file = ".env"


settings = Settings()
