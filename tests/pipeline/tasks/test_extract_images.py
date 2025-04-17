import re
from pathlib import Path

import pytest
from PIL import Image, UnidentifiedImageError

from pipeline.tasks.pdf_processing import (
    extract_images_from_dir,
    extract_images_from_pdf,
)


# Returns a single PDF from the test data folder for testing
@pytest.fixture(scope="module")
def sample_pdf(pdf_dir: Path):
    for p in pdf_dir.iterdir():
        if p.suffix.lower() == ".pdf":
            return p
    pytest.skip(f"No PDF files found in {pdf_dir}")


# Extracts images from a single PDF only once for these tests to save time
@pytest.fixture(scope="module")
def images_result(sample_pdf: Path, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    return extract_images_from_pdf(sample_pdf, output_dir)


# Extracts images from a folder of PDFs only once for these tests to save time
@pytest.fixture(scope="module")
def images_result_from_dir(pdf_dir: Path, output_dir: Path) -> dict[Path, list[Path]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    return extract_images_from_dir(pdf_dir, output_dir)


class TestExtractImagesFromPdf:
    def test_returns_image_paths(
        self, sample_pdf: Path, output_dir: Path, images_result
    ):
        assert (
            images_result
        ), f"No images extracted from {sample_pdf.name}, but some expected."
        assert all(
            p.exists() for p in images_result
        ), "One or more output paths do not exist."

    def test_image_paths_correctly_formed(
        self, sample_pdf: Path, output_dir: Path, images_result
    ):
        pdf_stem = sample_pdf.stem
        for path in images_result:
            # Expecting: <pdf_stem>_page<num>_img<num>, e.g. APV002_page1_img1
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

    def test_raise_error_on_non_pdf_file(self, tmp_path: Path):
        fake_file = tmp_path / "not_a_pdf.txt"
        fake_file.write_text("This is not a PDF.")

        output_dir = tmp_path / "output"

        with pytest.raises(ValueError, match="not_a_pdf.txt"):
            extract_images_from_pdf(fake_file, output_dir)


class TestExtractImagesFromDir:
    def test_all_pdfs_are_processed(
        self, pdf_dir: Path, output_dir: Path, images_result_from_dir
    ):
        expected = sorted(
            p for p in pdf_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"
        )
        actual = sorted(images_result_from_dir.keys())
        assert expected == actual, f"Mismatch in processed PDFs: {expected} vs {actual}"

    def test_image_paths_exist(
        self, pdf_dir: Path, output_dir: Path, images_result_from_dir
    ):
        for pdf, images in images_result_from_dir.items():
            for path in images:
                assert path.exists(), f"{path} does not exist (from {pdf.name})"

    def test_skips_non_pdf_files(self, tmp_path: Path):
        # Create mixed files
        mixed_dir = tmp_path / "mixed"
        mixed_dir.mkdir()

        import pikepdf

        valid_pdf_path = mixed_dir / "valid.pdf"
        with pikepdf.new() as pdf:
            pdf.save(valid_pdf_path)
        (mixed_dir / "notes.txt").write_text("hello world")
        (mixed_dir / "image.png").write_bytes(b"\x89PNG...")

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        from pipeline.tasks.pdf_processing import extract_images_from_dir

        result = extract_images_from_dir(mixed_dir, output_dir)

        assert set(result.keys()) == {
            valid_pdf_path
        }, "Non-PDFs should not be processed"
