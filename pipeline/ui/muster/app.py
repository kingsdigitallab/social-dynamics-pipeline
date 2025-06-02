from nicegui import app, ui

from pipeline.ui.config import settings
from pipeline.ui.muster.views.home import render as render_home
from pipeline.ui.muster.views.layout import layout


@ui.page("/", title="Roll Review Centre")
def home():
    with layout(
        title="Roll Review Centre",
        description="""Browse all available individuals and forms.
    Search and select forms for correction.""",
    ):
        render_home()


app.add_static_files(
    str(settings.images_url_base),
    str(settings.images_dir),
)
ui.run(title="Main App", port=8080)
