from nicegui import app, ui

from pipeline.ui.config import settings
from pipeline.ui.muster.views.layout import layout


@ui.page("/", title="Home")
def home():
    with layout("Home"):
        ui.label("Coming soon...")
        # content here


app.add_static_files(
    str(settings.images_url_base),
    str(settings.images_dir),
)
ui.run(title="Main App", port=8080)
