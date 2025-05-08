from pathlib import Path

import pytest
from PIL import Image

from pipeline.tasks.image_processing import resize_image, resize_images_from_dir

TARGET_DIMENSION = 150


# Returns a single image from the test data folder for testing
@pytest.fixture(scope="module")
def sample_image(image_dir: Path):
    for img in sorted(image_dir.iterdir()):
        if img.suffix.lower() in {".jpg", ".jpeg", ".png", ".tiff"}:
            return img
    pytest.skip(f"No image files found in {image_dir}")


@pytest.fixture(scope="module")
def output_img_dir(output_dir: Path) -> Path:
    path = output_dir / "resized"
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.fixture(scope="module")
def output_img_tmp(tmp_path: Path) -> Path:
    return tmp_path / "resized.jpg"


# Resizes images from a folder of images only once for some tests to save time
@pytest.fixture(scope="module")
def resized_result_from_dir(
    image_dir: Path, output_img_dir: Path
) -> dict[Path, list[Path]]:
    output_img_dir.mkdir(parents=True, exist_ok=True)
    return resize_images_from_dir(image_dir, output_img_dir, width=TARGET_DIMENSION)


class TestResizeImageFromFile:
    def test_resize_image_to_specified_width(
        self, sample_image: Path, output_img_dir: Path
    ):
        result = resize_image(sample_image, output_img_dir, width=TARGET_DIMENSION)

        assert result.exists(), f"Output file was not created: {result}"
        with Image.open(result) as img:
            assert (
                img.width == TARGET_DIMENSION
            ), f"Expected width {TARGET_DIMENSION}, got {img.width}"

    def test_resize_image_to_specified_height(
        self, sample_image: Path, output_img_dir: Path
    ):
        result = resize_image(sample_image, output_img_dir, height=TARGET_DIMENSION)

        assert result.exists(), f"Output file was not created: {result}"
        with Image.open(result) as img:
            assert (
                img.height == TARGET_DIMENSION
            ), f"Expected height {TARGET_DIMENSION}, got {img.height}"

    def test_resize_image_fits_within_dimensions_preserves_aspect_ratio(
        self, sample_image: Path, output_img_dir: Path
    ):
        max_width, max_height = 200, 100

        result = resize_image(
            sample_image, output_img_dir, width=max_width, height=max_height
        )
        assert result.exists(), f"Output file was not created: {result}"

        with Image.open(sample_image) as original, Image.open(result) as resized:
            orig_ratio = original.width / original.height
            resized_ratio = resized.width / resized.height

            # Check that dimensions are within bounds
            assert (
                resized.width <= max_width
            ), f"Width {resized.width} exceeds max {max_width}"
            assert (
                resized.height <= max_height
            ), f"Height {resized.height} exceeds max {max_height}"

            # Check that aspect ratio was preserved within a tolerance
            assert abs(resized_ratio - orig_ratio) < 0.1, (
                f"Aspect ratio changed: expected ~{orig_ratio:.2f}, "
                f"got {resized_ratio:.2f}"
            )

    def test_filename_has_width_suffix(self, sample_image: Path, output_img_dir: Path):
        width = 150
        result = resize_image(sample_image, output_img_dir, width=width)
        expected_suffix = f"_w{width}px{sample_image.suffix}"
        assert result.name.endswith(
            expected_suffix
        ), f"Expected filename suffix '{expected_suffix}', got '{result.name}'"

    def test_filename_has_height_suffix(self, sample_image: Path, output_img_dir: Path):
        height = 100
        result = resize_image(sample_image, output_img_dir, height=height)
        expected_suffix = f"_h{height}px{sample_image.suffix}"
        assert result.name.endswith(
            expected_suffix
        ), f"Expected filename suffix '{expected_suffix}', got '{result.name}'"

    def test_filename_has_both_suffixes(self, sample_image: Path, output_img_dir: Path):
        width, height = 150, 100
        result = resize_image(sample_image, output_img_dir, width=width, height=height)
        expected_suffix = f"_w{width}px_h{height}px{sample_image.suffix}"
        assert result.name.endswith(
            expected_suffix
        ), f"Expected filename suffix '{expected_suffix}', got '{result.name}'"

    def test_raises_if_no_dimensions_given(self, sample_image: Path, tmp_path: Path):
        with pytest.raises(ValueError, match="Specify one of width or height."):
            resize_image(sample_image, tmp_path, width=None, height=None)


class TestResizeImagesFromDir:
    def test_all_images_are_processed(
        self, image_dir: Path, output_img_dir: Path, resized_result_from_dir
    ):
        expected = sorted(
            p
            for p in image_dir.iterdir()
            if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".tiff"}
        )
        actual = sorted(resized_result_from_dir.keys())
        assert (
            expected == actual
        ), f"Mismatch in processed images: {expected} vs {actual}"

    def test_resized_images_exist(
        self, image_dir: Path, output_img_dir: Path, resized_result_from_dir
    ):
        for original, resized_list in resized_result_from_dir.items():
            for resized in resized_list:
                assert (
                    resized.exists()
                ), f"{resized} was not created from {original.name}"

    def test_skips_non_image_files(self, tmp_path: Path):
        mixed_dir = tmp_path / "mixed"
        mixed_dir.mkdir()

        from PIL import Image

        valid_image = mixed_dir / "valid.jpg"
        Image.new("RGB", (100, 100)).save(valid_image)

        # Invalid files
        (mixed_dir / "notes.txt").write_text("this is not an image")
        (mixed_dir / "data.csv").write_text("id,value\n1,42")

        output_dir = tmp_path / "resized"
        output_dir.mkdir()

        result = resize_images_from_dir(mixed_dir, output_dir, width=150)

        assert set(result.keys()) == {valid_image}, "Non-image files should be skipped"
