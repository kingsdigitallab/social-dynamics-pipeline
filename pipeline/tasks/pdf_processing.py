import logging
import time
from pathlib import Path

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
    output_dir.mkdir(parents=True, exist_ok=True)
    start_time = time.time()  # Total time start
    logger.info("Starting extraction of images in PDF: %s", pdf_path)
    logger.info("Images will be output to: %s", output_dir)
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
