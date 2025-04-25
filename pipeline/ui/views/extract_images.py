from pathlib import Path

from nicegui import run, ui

from pipeline.tasks.pdf_processing import extract_images_from_pdf


def render():
    pdf_input = ui.input(label="Path to PDF file").classes("w-full")
    outdir_input = ui.input(label="Output directory").classes("w-full")

    async def run_extraction():
        """Run PDF image extraction."""
        if not pdf_input.value:
            ui.notify(
                "Please enter a PDF file path.", color="warning", position="center"
            )
            return

        pdf_path = Path(pdf_input.value)
        output_dir = Path(outdir_input.value)

        if not pdf_path.exists():
            ui.notify(
                f"PDF path does not exist: {pdf_path}",
                color="negative",
                position="center",
            )
            return
        if not pdf_path.suffix.lower() == ".pdf":
            ui.notify(f"Not a PDF file: {pdf_path}", color="warning", position="center")
            return

        output_dir.mkdir(parents=True, exist_ok=True)

        # Disable inputs and show spinner
        pdf_input.disable()
        outdir_input.disable()
        extract_button.disable()
        reset_button.disable()
        spinner.visible = True

        images = await run.io_bound(extract_images_from_pdf, pdf_path, output_dir)

        # Re-enable inputs and hide spinner
        spinner.visible = False
        extract_button.enable()
        reset_button.enable()
        pdf_input.enable()
        outdir_input.enable()

        ui.notify(
            f"Extracted {len(images)} images to {output_dir}",
            close_button="OK",
            type="positive",
            position="center",
        )
        log_output_box.push(
            f"Extraction complete! Found {len(images)} images in {pdf_path}."
        )

    def reset_detection():
        """Clear all current detection results and reset the UI to a clean state."""
        log_output_box.clear()

    with ui.row():
        extract_button = ui.button(
            "Extract images",
            icon="play_arrow",
            color="green",
            on_click=run_extraction,
        )
        reset_button = ui.button(
            "Reset", icon="refresh", color="white", on_click=reset_detection
        )
        spinner = ui.spinner("dots", size="lg").props("color=primary").classes("mt-0")
        spinner.visible = False

        log_output_box = ui.log().classes("w-full h-30")
