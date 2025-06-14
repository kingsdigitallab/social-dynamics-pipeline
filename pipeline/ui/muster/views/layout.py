from contextlib import contextmanager

from nicegui import html, ui

from pipeline.ui.muster.views.css import layout_css


@contextmanager
def layout(title: str, description: str):
    layout_css()

    with ui.header(elevated=True).classes("q-primary"):
        with ui.row().classes("w-full items-center justify-between"):
            html.h1("🪪 Muster 🇬🇧 British Army WWII Forms").classes(
                "text-2xl font-bold m-0 cursor-pointer"
            ).on("click", lambda: ui.navigate.to("/"))

            # Right-aligned dark mode toggle
            with ui.row().classes("items-center gap-2 q-toggle--light"):
                dark = ui.dark_mode()
                ui.switch("Dark mode").bind_value(dark).classes("dark-toggle")

    ui.html(f'<h2 class="text-2xl font-bold my-4">{title}</h2>')
    ui.label(f"{description}")
    ui.separator()

    yield

    with ui.footer().style("background-color: #3874c8"):
        ui.label("")
