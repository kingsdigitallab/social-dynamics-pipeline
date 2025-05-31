from pathlib import Path
from typing import Sequence

from nicegui import ui

from pipeline.ui.config import settings

IMAGE_ROOT = settings.images_dir
URL_ROOT = settings.images_url_base
FOLDERS = sorted([f for f in IMAGE_ROOT.iterdir() if f.is_dir()])


class FolderNavigator:
    def __init__(self, folders: Sequence[Path]):
        self.folders: Sequence[Path] = folders
        self.index: int = 0

    @property
    def current(self) -> Path:
        return self.folders[self.index]

    def can_go_next(self) -> bool:
        return self.index < len(self.folders) - 1

    def can_go_previous(self) -> bool:
        return self.index > 0

    def next(self) -> None:
        if self.can_go_next():
            self.index += 1

    def previous(self) -> None:
        if self.can_go_previous():
            self.index -= 1


navigator = FolderNavigator(FOLDERS)


def render():
    """Render an image grid with folder navigation and image zoom overlay."""

    zoom_dialog = ui.dialog().classes("items-center justify-center")
    with zoom_dialog:
        zoomed_img = (
            ui.image()
            .classes("max-w-[90vw] max-h-[90vh] rounded shadow-lg")
            .on("click", lambda: zoom_dialog.close())
        )

    def show_zoom(img_url: str):
        zoomed_img.set_source(img_url)
        zoom_dialog.open()
        ui.run_javascript(f"navigator.clipboard.writeText('{img_url}')")
        ui.notify(f"Copied to clipboard: {img_url}", color="positive")

    def load_images():
        folder = navigator.current
        image_dir = folder
        image_url_base = f"{URL_ROOT}/{folder.name}"

        image_grid.clear()
        folder_label.set_text(f"📁 Folder: {folder.name}")

        for img_path in sorted(image_dir.glob("*.jpg")):
            thumb_name = f"{img_path.stem}_w150px{img_path.suffix}"
            thumb_url = f"{image_url_base}/thumbnails/{thumb_name}"
            full_url = f"{image_url_base}/{img_path.name}"
            with image_grid:
                with ui.column().classes("items-center"):
                    ui.image(thumb_url).classes("w-[150px] h-auto cursor-pointer").on(
                        "click", lambda p=full_url: show_zoom(p)
                    )

    def next_folder():
        if navigator.can_go_next():
            navigator.next()
            load_images()
        else:
            ui.notify("No more folders!", color="warning")

    def previous_folder():
        if navigator.can_go_previous():
            navigator.previous()
            load_images()
        else:
            ui.notify("Already at first folder!", color="warning")

    with ui.row().classes("items-center gap-4"):
        folder_label = ui.label()
        ui.button("◀ Previous", on_click=previous_folder)
        ui.button("Next ▶", on_click=next_folder)

    image_grid = ui.grid(columns=8).classes("mt-4 gap-4")
    load_images()
