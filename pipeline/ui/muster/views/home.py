from typing import Any

from nicegui import ui
from sqlmodel import Session, select

from pipeline.database.init_db import engine
from pipeline.database.models import FormB102r, Individual


def render():
    """Create the Roll Review Centre (homepage correction dashboard)"""

    ui.add_head_html(
        """
    <style>
    /* */
    .database-table thead tr {
        background-color: var(--q-primary);
        color: white;
    }
    .q-tab {
        border-top-left-radius: 0.5rem !important;
        border-top-right-radius: 0.5rem !important;
    }
    /* Unselected tabs */
    .q-tab:not(.q-tab--active) {
        background-color: #e5e7eb; /* Tailwind gray-200 */
        color: #1f2937; /* Tailwind gray-800 for text */
        transition: background-color 0.2s ease;
    }

    /* Optional hover effect for unselected tabs */
    .q-tab:not(.q-tab--active):hover {
        background-color: #d1d5db; /* Tailwind gray-300 */
    }
    /* Tab content area background */
    .q-tab-panel {
        background-color: var(--q-primary);
        color: white;
        border-radius: 0 0 0.5rem 0.5rem;
    }
    </style>
    """
    )

    # ----------------
    # Helper functions
    # ----------------

    column_defaults = {"align": "left"}

    def get_individuals() -> list[Individual]:
        with Session(engine) as session:
            indivs = session.exec(select(Individual)).all()
            # Sort by numeric part of PDF ID
            return sorted(
                indivs,
                key=lambda ind: (
                    int(ind.pdf_id.removeprefix("APV"))
                    if ind.pdf_id and ind.pdf_id.startswith("APV")
                    else 0
                ),
            )

    def get_forms() -> list[FormB102r]:
        with Session(engine) as session:
            frms = session.exec(select(FormB102r)).all()
            return sorted(
                frms,
                key=lambda fm: fm.lastname or "",
            )

    async def start_form_correction():
        selected_rows: list[dict[str, Any]] = form_table.selected
        if not selected_rows:
            ui.notify("Pick a form to correct.", position="center")
        else:
            row: dict[str, Any] = selected_rows[0]  # type: ignore
            form_id = row.get("id")
            ui.navigate.to("/correct/%d" % form_id)

    def update_form_table():
        frms = get_forms()

        columns = [
            {
                "name": "form_type",
                "label": "Form Type",
                "field": "form_type",
                "sortable": True,
            },
            {
                "name": "lastname",
                "label": "Last Name",
                "field": "lastname",
                "sortable": True,
            },
            {
                "name": "firstname",
                "label": "First Name",
                "field": "firstname",
                "sortable": True,
            },
            {"name": "dob", "label": "Date of Birth", "field": "dob", "sortable": True},
            {
                "name": "army_number",
                "label": "Army Number",
                "field": "army_number",
                "sortable": True,
            },
        ]

        rows = [
            {
                "id": form.id,
                "form_type": form.form_type or "",
                "lastname": form.lastname or "",
                "firstname": form.firstname or "",
                "dob": form.dob or "",
                "army_number": form.army_number or "",
            }
            for form in frms
        ]

        return (
            ui.table(
                columns=columns,
                rows=rows,
                column_defaults=column_defaults,
                row_key="id",
                selection="single",
                on_select=lambda e: ui.notify(f"selected: {e.selection}"),
            )
            .classes("w-full database-table")
            .props("bordered hide-bottom")
        )

    def update_individual_table():
        indivs = get_individuals()

        columns = [
            {"name": "pdf_id", "label": "PDF ID", "field": "pdf_id", "sortable": True},
            {
                "name": "lastname",
                "label": "Last Name",
                "field": "lastname",
                "sortable": True,
            },
            {
                "name": "firstname",
                "label": "First Name",
                "field": "firstname",
                "sortable": True,
            },
            {"name": "dob", "label": "Date of Birth", "field": "dob", "sortable": True},
            {
                "name": "army_number",
                "label": "Army Number",
                "field": "army_number",
                "sortable": True,
            },
            {
                "name": "num_forms",
                "label": "# Forms",
                "field": "num_forms",
                "sortable": True,
            },
        ]

        rows = [
            {
                "pdf_id": person.pdf_id or "",
                "lastname": person.lastname or "",
                "firstname": person.firstname or "",
                "dob": person.dob.isoformat() if person.dob else "",
                "army_number": person.army_number or "",
                "num_forms": person.army_number or "",
            }
            for person in indivs
        ]

        return (
            ui.table(
                columns=columns,
                rows=rows,
                column_defaults=column_defaults,
                row_key="id",
            )
            .classes("w-full database-table")
            .props("bordered")
        )

    # ---------------
    # Search bar
    # ---------------
    with ui.row().classes("w-full items-center gap-4"):
        ui.input(placeholder="Search").classes("w-1/2 flex-grow").props(
            "outlined clearable dense debounce=500"
        )
        with ui.button("Search", icon="search"):
            ui.tooltip("Search for individuals")

        ui.separator().props("vertical").classes("h-16")

        with ui.button("Filter", icon="filter_alt"):
            ui.tooltip("Open the filter panel")

    # ---------------
    # Tabs
    # ---------------
    with (
        ui.tabs()
        .classes("w-full -mb-4")  # -mb-4 closes the gap between tab and tab panel
        .props(
            "active-color=blue-1 active-bg-color=primary indicator-color=primary "
            "align=left inline-label no-caps"
        ) as tabs
    ):
        individuals = ui.tab(name="individuals", label="Individuals", icon="groups")
        forms = ui.tab(name="frms", label="Forms", icon="view_list")
    with ui.tab_panels(tabs, value=forms).classes("w-full"):

        # Individuals tab
        with ui.tab_panel(individuals):
            ui.label("1403 Individuals")

            with ui.column().classes("w-full"):
                update_individual_table()

        # Forms tab
        with ui.tab_panel(forms):
            ui.label("3672 Forms")

            with ui.column().classes("w-full"):
                form_table = update_form_table()

            with ui.row().classes("w-full items-center gap-4"):
                with (
                    ui.button(
                        "Start",
                        icon="play_arrow",
                        on_click=start_form_correction,
                    )
                    .classes("ml-auto")
                    .props("color=secondary")
                ):
                    ui.tooltip("Start correction of selected form")
