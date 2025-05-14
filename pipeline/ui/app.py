from config import settings
from nicegui import app, ui

from pipeline.ui.views.blank_detection import render as render_blank_detection
from pipeline.ui.views.browse_database import render as render_browse_database
from pipeline.ui.views.browse_images import render as render_browse_images
from pipeline.ui.views.extract_images import render as render_extract_images
from pipeline.ui.views.form_classification import render as render_form_classification
from pipeline.ui.views.layout import layout


@ui.page("/", title="Home")
def home():
    with layout("Home"):
        ui.label("Coming soon...")
        # content here


@ui.page("/browse-images", title="Browse Images")
def browse_images_page():
    with layout(""):
        render_browse_images()


@ui.page("/extract-images", title="Extract Images from PDF")
def extract_images_page():
    with layout("Extract Images from PDF"):
        render_extract_images()


@ui.page("/blank-detection", title="Blank Page Detection")
def blank_detection_page():
    with layout("Blank Page Detection"):
        zoom_dialog = ui.dialog().classes("items-center justify-center")
        with zoom_dialog:
            zoomed_image = ui.image().classes(
                "max-w-[90vw] max-h-[90vh] rounded shadow-lg"
            )
            ui.button(icon="close", on_click=zoom_dialog.close).props(
                'icon="close"'
            ).tooltip("Close").classes(
                "absolute top-2 right-2 z-10 bg-white text-black rounded-full shadow-md"
            )

        def show_zoom(original_path: str):
            """Display a zoomed-in version of the selected image in a dialog."""
            zoomed_image.set_source(original_path)
            zoom_dialog.open()

        render_blank_detection()


@ui.page("/form-classification", title="Form Type Classification")
def form_classification_page():
    with layout("Form Type Classification"):
        render_form_classification()


@ui.page("/browse-database", title="Browse Database")
def browse_database_page():
    with layout("Browse Database"):
        render_browse_database()


app.add_static_files(
    str(settings.images_url_base),
    str(settings.images_dir),
)
ui.run()
