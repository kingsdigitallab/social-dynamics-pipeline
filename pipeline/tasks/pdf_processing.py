import logging
import time
from pathlib import Path
from typing import Dict, List

from pikepdf import (
    Pdf,
    PdfImage,
)
from pikepdf.exceptions import (
    HifiPrintImageNotTranscodableError,
    ImageDecompressionError,
    InvalidPdfImageError,
    UnsupportedImageTypeError,
)

from pipeline.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def extract_images_from_pdf(pdf_path: Path, output_dir: Path) -> list[Path]:
    """
    Extract images from a single PDF and save them to a directory.

    Validates the input file, iterates over all pages in the PDF, and extracts
    embedded images using PikePDF. Each image is saved to a file named with the
    pattern: <PDF_stem>_page<page_num>_img<image_num>. Images are saved in the
    specified output directory.

    Non-PDF files will raise a ValueError. Any unsupported or unreadable images
    are skipped with a logged error.

    Args:
        pdf_path (Path): Path to the input PDF file.
        output_dir (Path): Directory where extracted image files will be saved.

    Returns:
        list[Path]: A list of file paths pointing to the extracted images.
    """
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"File is not a PDF: {pdf_path}")

    logger.info("Starting extraction of images in PDF: %s", pdf_path)
    logger.info("Images will be output to: %s", output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    start_time = time.time()  # Total time start
    extracted_images = []
    pdf_name = pdf_path.stem

    doc = Pdf.open(pdf_path)
    total_images = 0

    for page_num, page in enumerate(doc.pages):
        images = page.images
        logger.debug("Page %d: Found %d images.", page_num + 1, len(images))

        for img_index, (_, raw_image) in enumerate(images.items()):
            image_start_time = time.time()  # Image time start

            try:
                pdf_image = PdfImage(raw_image)
                output_stem = (
                    Path(output_dir)
                    / f"{pdf_name}_page{page_num + 1}_img{img_index + 1}"
                )
                output_path = pdf_image.extract_to(fileprefix=str(output_stem))
                extracted_images.append(Path(output_path))

            except (
                UnsupportedImageTypeError,
                HifiPrintImageNotTranscodableError,
                InvalidPdfImageError,
                ImageDecompressionError,
            ) as e:
                logger.error(
                    "PikePDF cannot extract the image on page %d: %s", page_num + 1, e
                )
            except OSError as e:
                logger.error(
                    "Error writing image to file %s: %s", extracted_images[-1], e
                )
            except Exception as e:
                logger.error(
                    "Unexpected error processing image on page %d: %s", page_num + 1, e
                )

            image_end_time = time.time()  # Image time end
            total_images += 1

            logger.debug(
                "Saved: %s (Processing time: %.2f seconds)",
                extracted_images[-1],
                image_end_time - image_start_time,
            )

    # Total time end
    pdf_end_time = time.time()
    total_time = pdf_end_time - start_time

    logger.info(
        "Total: %d images in %.2f seconds.",
        total_images,
        total_time,
    )
    logger.info("Completed processing %s", pdf_path)

    return extracted_images


def extract_images_from_dir(dir_path: Path, output_dir: Path) -> dict[Path, list[Path]]:
    """
    Extract all images from all PDF files in a directory.

    Iterates over files in `dir_path`, extracts images from each valid PDF using
    `extract_images_from_pdf`, and saves them into subfolders within `output_dir`.
    Non-PDF files are skipped with a warning.

    Args:
        dir_path (Path): The directory containing PDF files to process.
        output_dir (Path): The directory where output images will be saved.

    Returns:
        dict[Path, list[Path]]: A mapping from each processed PDF file to a list of
        extracted image file paths.
    """
    logger.info("Starting batch extraction of images from folder: %s", dir_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    results: Dict[Path, List[Path]] = {}

    for file in sorted(dir_path.glob("*")):
        if not file.is_file():
            logger.debug("Skipping non-file: %s", file)
            continue
        try:
            images = extract_images_from_pdf(file, output_dir / file.stem)
            results[file] = images
        except ValueError as e:
            logger.warning("Skipping non-PDF %s: %s", file.name, e)

    total_time = time.time() - start_time
    logger.info(
        "Finished batch extraction from %s in %.2f seconds", dir_path, total_time
    )
    return results
