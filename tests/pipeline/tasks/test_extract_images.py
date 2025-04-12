import re
from pathlib import Path

import pytest
from PIL import Image, UnidentifiedImageError

from pipeline.tasks.pdf_processing import extract_images_from_pdf

TEST_DATA_DIR = Path(__file__).parent.parent.parent / "data"
PUBLIC_DATA, PRIVATE_DATA = (TEST_DATA_DIR / name for name in ("public", "private"))


def first_pdf_in(directory: Path) -> Path:
    try:
        return next(p for p in directory.iterdir() if p.suffix.lower() == ".pdf")
    except StopIteration as e:
        raise FileNotFoundError(f"No PDF files found in {directory}") from e


@pytest.fixture(scope="module")
def output_dir() -> Path:
    path = TEST_DATA_DIR / "output"
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.fixture(scope="module", params=["public", "private"])
def sample_pdf(request):
    data_dirs = {"public": PUBLIC_DATA / "pdfs", "private": PRIVATE_DATA / "pdfs"}
    folder = data_dirs[request.param]
    try:
        return first_pdf_in(folder)
    except FileNotFoundError:
        pytest.skip(f"{request.param.capitalize()} test data not available")


@pytest.fixture(scope="module")
def images_result(sample_pdf: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    return extract_images_from_pdf(sample_pdf, output_dir)


class TestExtractImagesFromPdf:
    def test_returns_image_paths(
        self, sample_pdf: Path, output_dir: Path, images_result
    ):
        assert isinstance(
            images_result, list
        ), "Result should be list of Path objects, but got: {}".format(
            type(images_result).__name__
        )
        assert len(
            images_result
        ), f"No images extracted from {sample_pdf.name}, but some expected."
        assert all(
            isinstance(p, Path) for p in images_result
        ), "Some items in result are not Path objects."
        assert all(
            p.exists() for p in images_result
        ), "One or more output paths do not exist."

    def test_image_paths_correctly_formed(
        self, sample_pdf: Path, output_dir: Path, images_result
    ):
        pdf_stem = sample_pdf.stem
        for path in images_result:
            # Expecting filenames like: APV002_page1_img1
            # - Starts with the original PDF stem (e.g., APV002)
            # - Followed by "_page" and a page number (digits)
            # - Followed by "_img" and an image number (digits)
            pattern = rf"^{re.escape(pdf_stem)}_page\d+_img\d+$"
            assert re.match(pattern, path.stem), (
                f"Filename {path.name} is not correctly formed — expected format: "
                f"'<PDF_STEM>_page<NUM>_img<NUM>', e.g. '{pdf_stem}_page1_img1'"
            )

    def test_image_paths_are_image_files(
        self, sample_pdf: Path, output_dir: Path, images_result
    ):
        for path in images_result:
            assert path.exists()
            assert path.suffix.lower() in {".jpg", ".png", ".tiff"}
            try:
                with Image.open(path) as img:
                    img.verify()  # Verifies structure, doesn't load full image
            except UnidentifiedImageError:
                pytest.fail(f"{path} is not a valid image")
