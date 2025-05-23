from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    images_dir: Path = Path("tests/data/public/images")
    images_url_base: Path = Path("/images")
    demo_mode: bool = True

    project_root: Path = Path(__file__).resolve().parents[2]
    database_name: Path = Path("socdyn_test_db.db")

    class Config:
        env_file = ".env"

    @property
    def database_path(self) -> Path:
        return self.project_root / self.database_name


settings = Settings()
