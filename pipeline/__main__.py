from pathlib import Path

import typer

from pipeline.tasks.image_processing import thumbnail
from pipeline.tasks.pdf_processing import extract_images_from_pdf

app = typer.Typer()

r"""
Example usage:

$ python -m pipeline extract-images --pdf-path path/to/file.pdf --output-dir output/
$ python -m pipeline thumbnail --image-path output/file_img_0.jpg \
    --output-dir output/thumbnails/
$ python -m pipeline extract-and-thumbnail --pdf-path path/to/file.pdf \
    --image-dir output/
"""


@app.command()
def extract_images(
    pdf_path: str = typer.Option(
        ..., "--pdf-path", "-p", help="Path to the PDF file to extract images from."
    ),
    output_dir: str = typer.Option(
        ...,
        "--output-dir",
        "-o",
        help="Directory where the extracted images will be saved.",
    ),
):
    """Extract images from a PDF file."""
    result = extract_images_from_pdf(Path(pdf_path), Path(output_dir))
    for p in result:
        print(f"Extracted: {p}")


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
    thumb = thumbnail(Path(image_path), Path(output_dir))
    print(f"Created thumbnail: {thumb}")


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
    image_paths = extract_images_from_pdf(Path(pdf_path), Path(image_dir))
    thumb_dir = Path(image_dir) / "thumbnails"
    for path in image_paths:
        thumbnail(path, thumb_dir)
    print("Done.")


if __name__ == "__main__":
    app()
