import time
from pathlib import Path
from typing import Annotated, Optional

import typer

from pipeline.logging_config import setup_logging
from pipeline.tasks.db_import_b102r import import_all_in_dir
from pipeline.tasks.image_processing import resize_image, resize_images_from_dir
from pipeline.tasks.pdf_processing import (
    extract_images_from_dir,
    extract_images_from_pdf,
)

setup_logging()
VALID_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
THUMBNAIL_WIDTH = 150

app = typer.Typer()

r"""
Example usage:

$ python -m pipeline extract-images --pdf-path path/to/file.pdf \
    --output-dir output/ --log-level INFO
$ python -m pipeline thumbnail-images --img-path path/to/img.jpg \
    --output-dir output/thumbnails --log-level INFO
$ python -m pipeline import-b102r --input-dir path/to/dir \
    --log-level INFO
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


@app.command("thumbnail-images")
def thumbnail_images(
    img_path: Annotated[
        Path,
        typer.Option(
            "--img-path", "-p", help="Path to the image file or directory of images."
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Directory where the resized images will be saved.",
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
    Generate 150px-wide thumbnails from an image file or all image files in a folder.

    This command takes either a single image file or a directory of images and
    resizes them to thumbnails (150px wide). Resized images are saved to the specified
    output directory, with filenames indicating their new size.

    If a directory is passed, all supported image files are processed in turn, and a
    summary is shown at the end. Use the --log-level option to control verbosity.
    Defaults to WARNING.
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

    if img_path.is_dir():
        results = resize_images_from_dir(img_path, output_dir, width=THUMBNAIL_WIDTH)
        total_images = sum(len(paths) for paths in results.values())
        total_time = time.time() - start_time
        typer.echo(
            typer.style(
                f"Resized {total_images} thumbnails from {len(results)} "
                f"images into {output_dir} in {total_time:.1f} seconds",
                fg=typer.colors.GREEN,
                bold=True,
            )
        )
    elif img_path.is_file():
        result = resize_image(img_path, output_dir, width=THUMBNAIL_WIDTH)
        total_time = time.time() - start_time
        typer.echo(
            typer.style(
                f"Thumbnail created in {total_time:.1f} seconds: {result}",
                fg=typer.colors.GREEN,
                bold=True,
            )
        )
    else:
        typer.echo(
            typer.style(
                "Error: --img-path must be a valid file or directory.",
                fg=typer.colors.RED,
                bold=True,
            ),
            err=True,
        )
        raise typer.Exit(code=1)


@app.command()
def extract_and_thumbnail():
    """Extract images from a PDF and create thumbnails for them in one step."""
    raise NotImplementedError


@app.command("resize-images")
def resize_images(
    img_path: Annotated[
        Path,
        typer.Option(
            "--img-path", "-p", help="Path to the image file or directory of images."
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir", "-o", help="Directory where resized images will be saved."
        ),
    ],
    width: Annotated[
        Optional[int],
        typer.Option("--width", "-w", help="Target width in pixels."),
    ] = None,
    height: Annotated[
        Optional[int],
        typer.Option("--height", "-h", help="Target height in pixels."),
    ] = None,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            "-l",
            help="Set logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
            case_sensitive=False,
        ),
    ] = "WARNING",
):
    """
    Resize image(s) to a specified width and/or height while maintaining aspect ratio.

    Takes either a single image file or a directory of image files and resizes them,
    saving the outputs to the specified directory. Filenames are suffixed with the
    target dimensions. If both width and height are given, images are resized to fit
    within those bounds while preserving the aspect ratio.

    Use --log-level to control verbosity. Defaults to WARNING.
    """
    log_level = log_level.upper()
    if log_level not in VALID_LOG_LEVELS:
        typer.echo(
            typer.style(
                f"Invalid log level: {log_level}. "
                f"Choose from: DEBUG, INFO, WARNING, ERROR, CRITICAL.",
                fg=typer.colors.RED,
                bold=True,
            ),
            err=True,
        )
        raise typer.Exit(code=1)

    if width is None and height is None:
        typer.echo(
            typer.style(
                "You must provide at least one of --width or --height.",
                fg=typer.colors.RED,
                bold=True,
            ),
            err=True,
        )
        raise typer.Exit(code=1)

    setup_logging(log_level)
    start_time = time.time()

    if img_path.is_dir():
        results = resize_images_from_dir(
            img_path, output_dir, width=width, height=height
        )
        total_images = sum(len(paths) for paths in results.values())
        total_time = time.time() - start_time
        typer.echo(
            typer.style(
                f"Resized {total_images} images from {len(results)} source files "
                f"into {output_dir} in {total_time:.1f} seconds",
                fg=typer.colors.GREEN,
                bold=True,
            )
        )
    elif img_path.is_file():
        result = resize_image(img_path, output_dir, width=width, height=height)
        total_time = time.time() - start_time
        typer.echo(
            typer.style(
                f"Resized image in {total_time:.1f} seconds: {result}",
                fg=typer.colors.GREEN,
                bold=True,
            )
        )
    else:
        typer.echo(
            typer.style(
                "Error: --img-path must be a valid file or directory.",
                fg=typer.colors.RED,
                bold=True,
            ),
            err=True,
        )
        raise typer.Exit(code=1)


@app.command("import-b102r")
def import_b102r(
    input_dir: Annotated[
        Path,
        typer.Option(
            "--input-dir",
            "-i",
            help="Directory containing B102r JSON files to import.",
        ),
    ],
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            "-l",
            help="Set the logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL.",
            case_sensitive=False,
        ),
    ] = "WARNING",
):
    """
    Import all B102r-form JSON files from a directory into the database.

    This command loads raw data extracted from forms into the database for review.

    Use the --log-level option to control verbosity. Defaults to WARNING.
    """
    log_level = log_level.upper()

    if log_level not in VALID_LOG_LEVELS:
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

    if not input_dir.exists() or not input_dir.is_dir():
        typer.echo(
            typer.style(
                f"Error: {input_dir} is not a valid directory.",
                fg=typer.colors.RED,
                bold=True,
            ),
            err=True,
        )
        raise typer.Exit(code=1)

    num_imported = import_all_in_dir(input_dir)

    elapsed = time.time() - start_time
    typer.echo(
        typer.style(
            f"Successfully imported {num_imported} B102r forms from {input_dir} "
            f"in {elapsed:.1f} seconds.",
            fg=typer.colors.GREEN,
            bold=True,
        )
    )


if __name__ == "__main__":
    app()
