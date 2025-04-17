import time
from pathlib import Path
from typing import Annotated

import typer

from pipeline.logging_config import setup_logging
from pipeline.tasks.pdf_processing import (
    extract_images_from_dir,
    extract_images_from_pdf,
)

setup_logging()
VALID_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

app = typer.Typer()

r"""
Example usage:

$ python -m pipeline extract-images --pdf-path path/to/file.pdf \
    --output-dir output/ --log-level INFO
$ python -m pipeline thumbnail-images --img-path path/to/img.jpg \
    --output-dir output/thumbnails --log-level INFO
$ python -m pipeline extract-and-thumbnail --pdf-path path/to/file.pdf \
    --output-dir output/ --log-level INFO
"""


@app.command()
def extract_images(
    pdf_path: Annotated[
        Path,
        typer.Option(
            "--pdf-path", "-p", help="Path to the PDF file or directory of PDFs."
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Directory where the extracted images will be saved.",
        ),
    ],
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            "-l",
            help="Set the logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
            case_sensitive=False,
        ),
    ] = "WARNING",
):
    """
    Extract embedded images from a PDF file or all PDFs in a folder.

    This command takes either a single PDF file or a directory of PDFs and extracts
    all embedded images using pikepdf. Images are saved to the specified output
    directory.

    If a directory is passed, each PDF is processed in turn, and a summary is shown
    at the end. Use the --log-level option to control verbosity. Defaults to WARNING.
    """
    log_level = log_level.upper()

    if log_level.upper() not in VALID_LOG_LEVELS:
        typer.echo(
            typer.style(
                f"Invalid log level: {log_level}. Choose from: DEBUG, INFO, "
                f"WARNING, ERROR, CRITICAL.",
                fg=typer.colors.RED,
                bold=True,
            ),
            err=True,
        )
        raise typer.Exit(code=1)

    setup_logging(log_level)

    start_time = time.time()

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if pdf_path.is_dir():
        results = extract_images_from_dir(pdf_path, output_dir)
        total_pdfs = len(results)
        total_images = sum(len(imgs) for imgs in results.values())
        total_time = time.time() - start_time
        typer.echo(
            typer.style(
                f"Extracted {total_images} images from {total_pdfs} PDFs "
                f"into {output_dir} in {total_time:.1f} seconds",
                fg=typer.colors.GREEN,
                bold=True,
            )
        )
    elif pdf_path.is_file():
        images = extract_images_from_pdf(pdf_path, output_dir)
        total_time = time.time() - start_time
        typer.echo(
            typer.style(
                f"Extracted {len(images)} images to {output_dir} in "
                f"{total_time:.1f} seconds",
                fg=typer.colors.GREEN,
                bold=True,
            )
        )
    else:
        typer.echo(
            typer.style(
                "Error: --pdf-path must be a valid file or directory.",
                fg=typer.colors.RED,
                bold=True,
            ),
            err=True,
        )
        raise typer.Exit(code=1)


@app.command()
def thumbnail_images(
    image_path: str = typer.Option(
        ...,
        "--image-path",
        "-i",
        help="Path to the image file to create a thumbnail from.",
    ),
    output_dir: str = typer.Option(
        ..., "--output-dir", "-o", help="Directory where the thumbnail will be saved."
    ),
):
    """Create a thumbnail for an image."""
    # thumb = thumbnail(Path(image_path), Path(output_dir))
    # print(f"Created thumbnail: {thumb}")
    raise NotImplementedError


@app.command()
def extract_and_thumbnail_images(
    pdf_path: str = typer.Option(
        ..., "--pdf-path", "-p", help="Path to the PDF file to extract images from."
    ),
    image_dir: str = typer.Option(
        ...,
        "--image-dir",
        "-d",
        help="Directory where the images and thumbnails will be saved.",
    ),
):
    """Extract images from a PDF and create thumbnails for them."""
    # image_paths = extract_images_from_pdf(Path(pdf_path), Path(image_dir))
    # thumb_dir = Path(image_dir) / "thumbnails"
    # for path in image_paths:
    #     thumbnail(path, thumb_dir)
    # print("Done.")
    raise NotImplementedError


if __name__ == "__main__":
    app()
