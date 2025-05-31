from contextlib import contextmanager

from nicegui import ui


@contextmanager
def layout(title: str):
    ui.html(f'<h2 class="text-2xl font-bold my-4">{title}</h2>')
    ui.separator()

    yield

    with ui.footer().style("background-color: #3874c8"):
        ui.label("")
