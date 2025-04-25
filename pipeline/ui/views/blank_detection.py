import time
from pathlib import Path
from typing import Literal

from nicegui import run, ui
from nicegui.element import Element

from pipeline.ui.config import settings

# The real detection functions will be added here when ready.
DETECTION_METHODS = {
    "mean_pixel_density": "real_function_import_here",
    "edge_detection": "real_function_import_here",
    "vlm_infer": "real_function_import_here",
}

# Globals
detection_classification: dict[str, Literal["blank", "not_blank"]] = {}
checkboxes_by_path: dict[str, ui.checkbox] = {}
blank_image_grid: Element  # type: ignore[no-redef]
not_blank_image_grid: Element  # type: ignore[no-redef]


def detect_blanks(method: str, input_path: str, **kwargs):
    """Run blank detection using selected method and
    return detected blanks and non-blanks."""
    print(f"Running processing on {input_path} files with {method}")
    if settings.demo_mode:
        time.sleep(2)  # Simulate processing time
        blanks_ = [
            f"/images/test_pdf_1_page{i}_img1.jpg" for i in range(1, 3)
        ]  # Simulate blanks
        not_blanks_ = [
            f"/images/test_pdf_1_page{i}_img1.jpg" for i in range(3, 6)
        ]  # Simulate non-blanks
        return blanks_, not_blanks_

    # The real detection functions will be added here when ready.
    fn = DETECTION_METHODS.get(method)
    if not fn:
        raise ValueError(f"Unknown method: {method} with {kwargs}")
    # return fn(input_path, **kwargs)

    raise NotImplementedError(
        "Detection methods not yet implemented outside demo mode."
    )


def process_blanks(files: list[str], **kwargs):
    """Process reviewed blank files, e.g. move or rename them with provided options."""
    print(f"Running processing on {len(files)} files with args {kwargs}")
    if settings.demo_mode:
        time.sleep(1)  # Simulate processing time
        return files  # Simulate returning new filepaths of images moved/renamed

    # The real processing functions will be added here when ready.
    return files


def thumbnail_path(original_path: str) -> str:
    """Return the path to the thumbnail version of the given original image path."""
    if settings.demo_mode:
        orig_path = Path(original_path)
        return f"/images/thumbnails/{orig_path.stem}_w150px{orig_path.suffix}"

    # The real thumbnail function will be added here when ready.
    # return f"/images/thumbnails/{orig_path.stem}_thumbnail{orig_path.suffix}"
    return ""


def render():
    """Render the full NiceGUI interface with Detect, Check, and Process tabs."""

    zoom_dialog = ui.dialog().classes("items-center justify-center")
    with zoom_dialog:
        zoomed_image = ui.image().classes("max-w-[90vw] max-h-[90vh] rounded shadow-lg")
        ui.button(icon="close", on_click=zoom_dialog.close).props(
            'icon="close"'
        ).tooltip("Close").classes(
            "absolute top-2 right-2 z-10 bg-white text-black rounded-full shadow-md"
        )

    def thumbnail_with_checkbox(
        original_path: str, grid: ui.element, checked: bool
    ) -> None:
        """Render a thumbnail with an overlaid checkbox into the given grid."""
        thumb = thumbnail_path(original_path)

        def on_toggle():
            # Re-render both grids based on current checkbox state
            blank_image_grid.clear()
            not_blank_image_grid.clear()
            for path, checkbox in checkboxes_by_path.items():
                target_grid = (
                    blank_image_grid if checkbox.value else not_blank_image_grid
                )
                thumbnail_with_checkbox(path, target_grid, checkbox.value)

        with grid, ui.element("div").classes("relative w-[150px] h-[150px]"):
            ui.image(thumb).classes("w-full h-full object-contain cursor pointer").on(
                "click", lambda e: show_zoom(original_path)
            )
            cb = ui.checkbox(value=checked, on_change=on_toggle).classes(
                "absolute top-1 right-1 z-10"
            )
            checkboxes_by_path[original_path] = cb

    def show_zoom(original_path: str):
        """Display a zoomed-in version of the selected image in a dialog."""
        zoomed_image.set_source(original_path)
        zoom_dialog.open()

    def update_correction_summary_table():
        """Update the process tab with a summary table showing error rate stats."""
        correction_summary_container.clear()

        # Calculate stats
        total_blanks = sum(1 for v in detection_classification.values() if v == "blank")
        total_not_blanks = sum(
            1 for v in detection_classification.values() if v == "not_blank"
        )

        corrected_blanks = sum(
            1
            for path, original in detection_classification.items()
            if original == "blank" and not checkboxes_by_path[path].value
        )
        corrected_not_blanks = sum(
            1
            for path, original in detection_classification.items()
            if original == "not_blank" and checkboxes_by_path[path].value
        )

        def error_rate(corrected: int, total: int) -> str:
            return f"{(corrected / total * 100):.1f}%" if total > 0 else "0%"

        rows = [
            {
                "classification": "Blanks",
                "detected": total_blanks,
                "corrected": corrected_blanks,
                "percent": error_rate(corrected_blanks, total_blanks),
            },
            {
                "classification": "Not Blanks",
                "detected": total_not_blanks,
                "corrected": corrected_not_blanks,
                "percent": error_rate(corrected_not_blanks, total_not_blanks),
            },
        ]

        with correction_summary_container:
            ui.table(
                columns=[
                    {
                        "name": "classification",
                        "label": "Classification",
                        "field": "classification",
                    },
                    {"name": "detected", "label": "Detected", "field": "detected"},
                    {
                        "name": "corrected",
                        "label": "Corrected",
                        "field": "corrected",
                    },
                    {"name": "percent", "label": "Error %", "field": "percent"},
                ],
                rows=rows,
                row_key="classification",
            ).classes("w-full").props("dense bordered")

    def update_tab(selected_tab):
        """Trigger updates to tab content based on selected tab."""
        if selected_tab.value == "3. Process":
            update_correction_summary_table()

    with ui.tabs(on_change=update_tab) as steps:
        step_1_detect = ui.tab("1. Detect")
        step_2_check = ui.tab("2. Check")
        step_3_process = ui.tab("3. Process")

    with ui.tab_panels(steps, value=step_1_detect, animated=False).classes("w-full"):
        # Step 1: Detection tab
        with ui.tab_panel(step_1_detect):
            ui.label(
                "Detect blank forms using the specified detection method "
                "and check the results before processing."
            )
            dir_path = ui.input(
                label="Filepath of directory with images to process",
                placeholder="Please enter full path",
            ).classes("w-1/2")

            detection_method = ui.select(
                options={
                    "mean_pixel_density": "Mean Pixel Density",
                    "edge_detection": "Edge Detection",
                    "vlm_infer": "VLM Inference",
                },
                label="Detection method",
                value="mean_pixel_density",
                on_change=lambda e: (
                    setattr(
                        mean_pixel_input, "visible", e.value == "mean_pixel_density"
                    ),
                    setattr(edge_input, "visible", e.value == "edge_detection"),
                    setattr(vlm_input, "visible", e.value == "vlm_infer"),
                ),
            ).classes("w-1/4")

            # Inputs for different methods
            mean_pixel_input = (
                ui.input(label="Threshold (0–255)")
                .classes("w-1/4")
                .props("type=number")
            )
            edge_input = (
                ui.input(label="Minimum number of edges")
                .classes("w-64")
                .props("type=number")
            )
            vlm_input = ui.textarea(
                label='Prompt to find blanks: must return either "True" or "False"',
                placeholder="e.g. Is this form blank? Answer with a single word, "
                "either 'True or 'False'.",
            ).classes("w-full")

            detection_args = {
                "mean_pixel_density": lambda: {
                    "threshold": (
                        int(mean_pixel_input.value) if mean_pixel_input.value else 128
                    )
                },
                "edge_detection": lambda: {
                    "edge_min": int(edge_input.value) if edge_input.value else 10
                },
                "vlm_infer": lambda: {
                    "prompt": vlm_input.value
                    or "Is this form blank? Answer only with one word: True or False."
                },
            }

            # Initially hide those not selected
            edge_input.visible = False
            vlm_input.visible = False

            async def run_detection() -> None:
                """Run the selected detection method and populate Check tab grids."""
                global detection_classification, checkboxes_by_path

                detect_button.disable()
                reset_button.disable()
                dir_path.disable()
                detection_method.disable()
                detect_spinner.visible = True

                ui.notify("Starting blank detection...")
                log_output_box.push(
                    f"Running blank detection using: {detection_method.value}"
                )
                extra_args = detection_args[detection_method.value]()
                blanks, not_blanks = await run.cpu_bound(
                    detect_blanks,
                    detection_method.value,
                    dir_path.value,
                    **extra_args,
                )

                detection_classification.clear()
                checkboxes_by_path.clear()
                blank_image_grid.clear()
                not_blank_image_grid.clear()

                for path in blanks:
                    detection_classification[path] = "blank"
                    thumbnail_with_checkbox(path, blank_image_grid, checked=True)

                for path in not_blanks:
                    detection_classification[path] = "not_blank"
                    thumbnail_with_checkbox(path, not_blank_image_grid, checked=False)

                detect_spinner.visible = False
                dir_path.enable()
                detection_method.enable()
                detect_button.enable()
                reset_button.enable()

                ui.notify(
                    f"Detection complete! Found {len(blanks)} blanks, "
                    f"{len(not_blanks)} non-blanks.",
                    close_button="OK",
                    type="positive",
                    position="center",
                )
                log_output_box.push(
                    f"Detection complete! Found {len(blanks)} blanks, "
                    f"{len(not_blanks)} non-blanks."
                )

                blanks.clear()
                not_blanks.clear()

            def reset_detection():
                """Clear all current detection results and reset the UI."""
                global checkboxes_by_path
                checkboxes_by_path.clear()
                blank_image_grid.clear()
                not_blank_image_grid.clear()
                log_output_box.clear()

            with ui.row():
                detect_button = ui.button(
                    "Detect blanks",
                    icon="play_arrow",
                    color="green",
                    on_click=run_detection,
                )
                # stop_button = ui.button("Stop", icon="stop", color="white",
                #                          on_click=reset_detection)
                reset_button = ui.button(
                    "Reset", icon="refresh", color="white", on_click=reset_detection
                )
                detect_spinner = (
                    ui.spinner("dots", size="lg").props("color=primary").classes("mt-0")
                )
                detect_spinner.visible = False

                log_output_box = ui.log().classes("w-full h-30")

        # Step 2: Check tab
        with ui.tab_panel(step_2_check):
            with ui.tabs() as outputs:
                blank_output = ui.tab("Blank")
                not_blank_output = ui.tab("Not Blank")

            with ui.tab_panels(outputs, value=blank_output, animated=False).classes(
                "w-full"
            ):
                with ui.tab_panel(blank_output):
                    ui.label(
                        "Check if these images are blanks. "
                        "UNTICK any images that are NOT blanks."
                    )
                    global blank_image_grid
                    blank_image_grid = ui.grid(columns=8)

                with ui.tab_panel(not_blank_output):
                    ui.label(
                        "Check if these images are not blanks. "
                        "TICK any images that ARE blanks."
                    )
                    global not_blank_image_grid
                    not_blank_image_grid = ui.grid(columns=8)

        # Step 3: Process tab
        with ui.tab_panel(step_3_process):
            correction_summary_container = ui.column().classes("mt-4")
            ui.label(
                "Process blanks to complete the batch. "
                "Make sure you have checked the images before proceeding!"
            )
            with ui.row():
                move_checkbox = ui.checkbox("Move", value=True)
                add_suffix_checkbox = ui.checkbox("Add suffix", value=True)

            output_dir = (
                ui.input(
                    label="New directory name where images should be moved, "
                    "within whatever directory they are currently in",
                    placeholder='Defaults to "/blanks"',
                )
                .classes("w-1/2")
                .bind_visibility_from(move_checkbox, "value")
            )

            file_suffix = (
                ui.input(
                    label="Filename suffix to add for blank images",
                    placeholder='Defaults to "_blank"',
                )
                .classes("w-1/2")
                .bind_visibility_from(add_suffix_checkbox, "value")
            )

            process_args = {
                "move": move_checkbox.value,
                "output_dir": output_dir.value or "blanks",
                "rename": add_suffix_checkbox.value,
                "suffix": file_suffix.value or "_blank",
            }

            async def run_process() -> None:
                """Apply processing steps to confirmed blanks and log the results."""
                global checkboxes_by_path, detection_classification

                move_checkbox.disable()
                add_suffix_checkbox.disable()
                process_button.disable()
                output_dir.disable()
                file_suffix.disable()
                process_spinner.visible = True

                ui.notify("Starting batch processing of blanks...")
                log_process_box.push(
                    f"Running batch processing of blanks: {process_args}"
                )

                confirmed_blanks = [
                    path for path, cb in checkboxes_by_path.items() if cb.value
                ]

                new_filepaths = await run.cpu_bound(
                    process_blanks, confirmed_blanks, **process_args
                )

                ui.notify(
                    f"Batch processing complete! "
                    f"Processed {len(new_filepaths)} blanks.",
                    close_button="OK",
                    type="positive",
                    position="center",
                )
                log_process_box.push(
                    f"Batch processing complete! Processed {len(new_filepaths)} blanks."
                )
                log_process_box.push(f"{new_filepaths}")

                move_checkbox.enable()
                add_suffix_checkbox.enable()
                process_button.enable()
                output_dir.enable()
                file_suffix.enable()
                process_spinner.visible = False

            with ui.row():
                process_button = ui.button(
                    "Process batch",
                    icon="play_arrow",
                    color="green",
                    on_click=run_process,
                )
                # stop_button = ui.button("Stop", icon="stop", color="white",
                #                          on_click=reset_detection)
                process_spinner = (
                    ui.spinner("dots", size="lg").props("color=primary").classes("mt-0")
                )
                process_spinner.visible = False

            log_process_box = ui.log().classes("w-full h-30")
