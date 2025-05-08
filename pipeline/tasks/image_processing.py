import logging
import time
from pathlib import Path
from typing import Optional

from PIL import Image, UnidentifiedImageError
from PIL.Image import Resampling

from pipeline.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

VALID_SUFFIXES = {".jpg", ".jpeg", ".png", ".tiff"}


def resize_image(
    img_path: Path,
    output_dir: Path,
    width: Optional[int] = None,
    height: Optional[int] = None,
) -> Path:
    """
    Resize an image and save it to the specified output directory with suffixes.

    Opens the image at `input_path` and resizes it based on either the provided
    `width`, `height`, or both. If only one dimension is specified, the other is
    calculated to preserve the original aspect ratio. If both dimensions are given,
    the image is resized to fit *within* the given width and height,
    preserving aspect ratio.

    Resized image is saved to `output_dir` with a modified filename that includes
    suffixes indicating the resized dimensions.

    Args:
        img_path (Path): Path to the original image file.
        output_dir (Path): Directory where the resized image will be saved.
        width (Optional[int]): Target width in pixels. Optional if height is provided.
        height (Optional[int]): Target height in pixels. Optional if width is provided.

    Returns:
        Path: Path to the resized image file.

    Raises:
        ValueError: If neither `width` nor `height` is provided.
    """
    if width is None and height is None:
        raise ValueError("Specify one of width or height.")

    if img_path.suffix.lower() not in VALID_SUFFIXES:
        raise ValueError(f"File is not a supported image type: {img_path}")

    start_time = time.time()

    logger.info("Starting resizing of image: %s", img_path)
    logger.info("Image will be output to: %s", output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(img_path) as img:
        orig_width, orig_height = img.size
        if width and height:
            # Scale to fit within the box maintaining aspect ratio
            width_ratio = width / orig_width
            height_ratio = height / orig_height
            scale = min(width_ratio, height_ratio)
            new_size = (int(orig_width * scale), int(orig_height * scale))
            suffix = f"_w{width}px_h{height}px"
        elif width:
            scale = width / orig_width
            new_size = (width, int(orig_height * scale))
            suffix = f"_w{width}px"
        elif height:
            scale = height / orig_height
            new_size = (int(orig_width * scale), height)
            suffix = f"_h{height}px"

        output_name = f"{img_path.stem}{suffix}{img_path.suffix}"
        output_path = output_dir / output_name

        resized = img.resize(new_size, Resampling.LANCZOS)
        resized.save(output_path)

    total_time = time.time() - start_time
    logger.info("Completed processing %s in %.2f seconds", output_path, total_time)

    return output_path


def resize_images_from_dir(
    dir_path: Path,
    output_dir: Path,
    width: Optional[int] = None,
    height: Optional[int] = None,
) -> dict[Path, list[Path]]:
    """
    Resize all image files in a directory and save them to an output folder.

    Iterates through the directory, resizes supported image files using the
    `resize_image` function, and stores the resized images in the output
    directory. Each image is renamed automatically with dimension suffixes.

    Args:
        dir_path (Path): Directory containing image files to resize.
        output_dir (Path): Directory where resized images will be saved.
        width (Optional[int]): Target width in pixels.
        height (Optional[int]): Target height in pixels.

    Returns:
        dict[Path, list[Path]]: Mapping from original image file to list of resized
        paths.
    """
    logger.info("Starting batch resizing of images from folder: %s", dir_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    result: dict[Path, list[Path]] = {}

    for file in sorted(dir_path.iterdir()):
        if not file.is_file() or file.suffix.lower() not in VALID_SUFFIXES:
            logger.debug("Skipping non-image file: %s", file.name)
            continue

        try:
            resized_path = resize_image(file, output_dir, width=width, height=height)
            result[file] = [resized_path]
        except (UnidentifiedImageError, OSError) as e:
            logger.warning("Failed to process %s: %s", file.name, e)

    total_time = time.time() - start_time
    logger.info("Finished batch resizing from %s in %.2f seconds", dir_path, total_time)

    return result
