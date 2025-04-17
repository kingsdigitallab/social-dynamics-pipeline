from pathlib import Path

import pytest

TEST_DATA_DIR = Path(__file__).parent / "data"
PUBLIC_DATA = TEST_DATA_DIR / "public"
PRIVATE_DATA = TEST_DATA_DIR / "private"


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    return TEST_DATA_DIR


@pytest.fixture(scope="session")
def public_data_dir() -> Path:
    return PUBLIC_DATA


@pytest.fixture(scope="session")
def private_data_dir() -> Path:
    return PRIVATE_DATA


@pytest.fixture(scope="session", params=["public", "private"])
def pdf_dir(request, public_data_dir: Path, private_data_dir: Path) -> Path:
    data_dirs = {
        "public": public_data_dir / "pdfs",
        "private": private_data_dir / "pdfs",
    }
    folder = data_dirs[request.param]
    if not folder.exists() or not any(folder.iterdir()):
        pytest.skip(f"{request.param.capitalize()} test PDF directory not available")
    return folder


@pytest.fixture(scope="session", params=["public", "private"])
def image_dir(request, public_data_dir: Path, private_data_dir: Path) -> Path:
    data_dirs = {
        "public": public_data_dir / "images",
        "private": private_data_dir / "images",
    }
    folder = data_dirs[request.param]
    if not folder.exists() or not any(folder.iterdir()):
        pytest.skip(f"{request.param.capitalize()} test image directory not available")
    return folder


@pytest.fixture(scope="session")
def output_dir(test_data_dir: Path) -> Path:
    path = test_data_dir / "output"
    path.mkdir(parents=True, exist_ok=True)
    return path
