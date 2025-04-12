import tempfile
from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas

PAGE_WIDTH, PAGE_HEIGHT = A5
JPEG_SIZE = (int(PAGE_WIDTH), int(PAGE_HEIGHT))  # Full-page image

# 5 distinct but readable colors
COLORS = ["gray", "blue", "green", "purple", "brown"]


def create_dummy_jpeg(path: Path, color: str, size=JPEG_SIZE):
    img = Image.new("RGB", size, color=color)
    img.save(path, format="JPEG")


def embed_image_page(pdf_canvas, image_path: Path):
    pdf_canvas.drawImage(str(image_path), 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)


def generate_test_pdfs(output_dir: Path, num_pdfs=5, pages_per_pdf=5):
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        for i in range(num_pdfs):
            color = COLORS[i % len(COLORS)]
            jpeg_path = tmpdir_path / f"image_{i+1}.jpg"
            create_dummy_jpeg(jpeg_path, color=color)

            pdf_path = output_dir / f"test_pdf_{i+1}.pdf"
            pdf = canvas.Canvas(str(pdf_path), pagesize=A5)

            for _ in range(pages_per_pdf):
                embed_image_page(pdf, jpeg_path)
                pdf.showPage()

            pdf.save()
            print(f"Generated {pdf_path} with color '{color}'")


if __name__ == "__main__":
    generate_test_pdfs(Path("public/pdfs"))
