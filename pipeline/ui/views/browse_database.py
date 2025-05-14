from nicegui import ui
from sqlmodel import Session, select

from pipeline.database.init_db import engine
from pipeline.database.models import Individual

ITEMS_PER_PAGE = 25


def render():
    """
    Render a page that lists all individuals from the database
    and shows associated form data when an individual is clicked.
    """

    ui.label("Individuals").classes("text-xl font-bold mb-4")

    page_state = {"current": 1}
    with ui.row().classes("items-center justify-between mt-4"):
        ui.button("◀ Previous", on_click=lambda: change_page(-1))
        ui.label().bind_text_from(page_state, "current")
        ui.button("Next ▶", on_click=lambda: change_page(1))

    table_container = ui.column().classes("w-full")

    form_dialog = ui.dialog().props("maximized")
    with form_dialog:
        ui.column().classes("p-4")

    def get_paginated_individuals(page: int) -> list[Individual]:
        offset = (page - 1) * ITEMS_PER_PAGE
        with Session(engine) as session:
            individuals = session.exec(
                select(Individual).offset(offset).limit(ITEMS_PER_PAGE)
            ).all()
            # Sort by numeric part of PDF ID
            return sorted(
                individuals,
                key=lambda ind: (
                    int(ind.pdf_id.removeprefix("APV"))
                    if ind.pdf_id and ind.pdf_id.startswith("APV")
                    else 0
                ),
            )

    def show_form_data(individual_id: int):
        with Session(engine) as session:
            individual = session.get(Individual, individual_id)

            if not individual or not individual.b102rs:
                ui.notify("No B102r forms found for this individual.", color="warning")
                return

            # only show first for now
            form = individual.b102rs[0]  # type: ignore

            form_dialog.clear()

            with form_dialog:

                with ui.row().classes("w-full items-start").style("flex-wrap: nowrap"):
                    # Table of fields
                    with ui.column().classes("w-2/5"):
                        columns = [
                            {"name": "field", "label": "Field", "field": "field"},
                            {"name": "value", "label": "Raw Value", "field": "value"},
                        ]
                        rows = []
                        for key in form.model_fields.keys():
                            if key.endswith("_raw"):
                                value = getattr(form, key)
                                rows.append({"field": key, "value": value or ""})
                        ui.table(columns=columns, rows=rows).classes("w-full").props(
                            "dense bordered"
                        )

                    # Image display
                    with ui.column().classes("w-3/5 items-center"):
                        if form.form_image:
                            folder = form.form_image.split("_")[0]
                            image_url = f"/images/{folder}/{form.form_image}"
                            # ui.label(image_url)
                            ui.image(image_url).classes(
                                "w-[100%] h-auto object-contain rounded shadow"
                            )
                        else:
                            ui.label("No image available").classes("text-gray-500")

            form_dialog.open()

    def update_table():
        table_container.clear()

        individuals = get_paginated_individuals(page_state["current"])

        columns = [
            {"name": "id", "label": "ID", "field": "id"},
            {"name": "pdf_id", "label": "PDF ID", "field": "pdf_id"},
            {"name": "lastname", "label": "Last Name", "field": "lastname"},
            {"name": "firstname", "label": "First Name", "field": "firstname"},
            {"name": "dob", "label": "Date of Birth", "field": "dob"},
            {"name": "army_number", "label": "Army Number", "field": "army_number"},
        ]

        rows = [
            {
                "id": person.id,
                "pdf_id": person.pdf_id or "",
                "lastname": person.lastname or "",
                "firstname": person.firstname or "",
                "dob": person.dob.isoformat() if person.dob else "",
                "army_number": person.army_number or "",
            }
            for person in individuals
        ]

        with table_container:
            (
                ui.table(
                    columns=columns,
                    rows=rows,
                    row_key="id",
                    selection="single",
                    on_select=lambda e: show_form_data(e.selection[0]["id"]),
                )
                .classes("w-full")
                .props("dense bordered")
            )

    def change_page(delta: int):
        page_state["current"] += delta
        if page_state["current"] < 1:
            page_state["current"] = 1
        update_table()

    update_table()
