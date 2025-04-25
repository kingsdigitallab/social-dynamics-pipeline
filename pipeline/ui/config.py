from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    images_dir: Path = Path("tests/data/public/images/test_pdf_1")
    images_url_base: Path = Path("/images")
    demo_mode: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
