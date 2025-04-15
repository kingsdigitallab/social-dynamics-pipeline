import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from nicegui import ui

from pipeline.tasks.pdf_processing import extract_images_from_pdf

executor = ThreadPoolExecutor()

ui.label("Extract Images from PDF").classes("text-h5")

pdf_input = ui.input(label="Path to PDF file").classes("w-full")
outdir_input = ui.input(label="Output directory").classes("w-full")
spinner = ui.spinner(size="lg").props("color=primary").classes("q-mt-md")
spinner.visible = False


async def run_extraction():
    if not pdf_input.value:
        ui.notify("Please enter a PDF file path.", color="warning")
        return

    pdf_path = Path(pdf_input.value)
    output_dir = Path(outdir_input.value)

    if not pdf_path.exists():
        ui.notify(f"PDF path does not exist: {pdf_path}", color="negative")
        return
    if not pdf_path.suffix.lower() == ".pdf":
        ui.notify(f"Not a PDF file: {pdf_path}", color="warning")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # Disable inputs and show spinner
    pdf_input.disable()
    outdir_input.disable()
    spinner.visible = True

    images = await asyncio.get_event_loop().run_in_executor(
        executor, functools.partial(extract_images_from_pdf, pdf_path, output_dir)
    )

    # Re-enable inputs and hide spinner
    spinner.visible = False
    pdf_input.enable()
    outdir_input.enable()

    ui.notify(f"Extracted {len(images)} images to {output_dir}", color="positive")


ui.button("Extract", on_click=run_extraction).classes("mt-4")

ui.run()
