from contextlib import contextmanager

from nicegui import html, ui


@contextmanager
def layout(title: str):
    with (
        ui.left_drawer(fixed=False)
        .style("background-color: #ebf1fa")
        .props("bordered") as left_drawer
    ):
        ui.link("📁️ Browse Images", "/browse-images").classes("text-xl")
        ui.link("🖼️ Extract Images", "/extract-images").classes("text-xl")
        ui.link("📄 Blank Detection (Demo)", "/blank-detection").classes("text-xl")
        # ui.link("📝 Form Classification", "/form-classification").classes("text-xl")
        ui.link("🔎 Browse Database", "/browse-database").classes("text-xl")

    with (
        ui.header(elevated=True)
        .style("background-color: #3874c8")
        .classes("items-left")
    ):
        ui.button(on_click=lambda: left_drawer.toggle(), icon="menu").props(
            "flat color=white"
        )
        html.h1("🛠📂️ Social Dynamics Pipeline").classes("text-2xl font-bold m-0").on(
            "click", lambda: ui.navigate.to("/")
        )

    ui.html(f'<h2 class="text-2xl font-bold my-4">{title}</h2>')
    ui.separator()

    yield

    with ui.footer().style("background-color: #3874c8"):
        ui.label("")
