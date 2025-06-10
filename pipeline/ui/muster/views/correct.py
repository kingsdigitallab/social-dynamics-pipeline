import copy
from collections import namedtuple
from datetime import date
from typing import Optional

from nicegui import ui
from sqlmodel import Session

from pipeline.database.helpers.form_b102r import get_form, save_form_with_log
from pipeline.database.init_db import engine
from pipeline.database.models import FormB102r
from pipeline.ui.muster.views.css import correct_css

# Current form global
frm: FormB102r | None = None
# Copy of form to compare for auditing on save
original_frm: FormB102r | None = None


def load_form(form_id: int):
    global frm, original_frm
    with Session(engine) as session:
        frm = get_form(session, form_id)
        original_frm = copy.deepcopy(frm)


def render(form_id: int):
    """Create the form editing page for a form specified by unique ID"""

    correct_css()
    load_form(form_id)
    print(frm)

    with ui.row().classes("w-full items-center justify-between"):
        ui.html(f"<h3 class='text-xl font-bold my-4'>ID: {form_id}</h2>")
        ui.label("Form Type: B102").classes("text-bold")
    ui.separator()

    Field = namedtuple("Field", ["label", "db_field", "type"])

    fields_list = {
        1: Field("1. Surname", "lastname", "text"),
        2: Field("2. Christian Names", "firstname", "text"),
        3: Field("3. Army Number", "army_number", "text"),
        4: Field("4. Regiment or Corps", "regiment_or_corp", "text"),
        5: Field("5. Nature of Engagement", "engagement", "text"),
        6: Field("6. Date of Joining / Enlistment", "date_of_enlistment", "text"),
        7: Field("7. Date of Birth", "dob", "text"),
        8: Field("Date of Birth", "dob_date", "date"),
        9: Field("8. Nationality", "nationality", "text"),
        10: Field("9. Religion", "religion", "text"),
        11: Field("10. Industry Group", "industry_group", "text"),
        12: Field("11. Occupational Classification", "occupation", "text"),
        13: Field("12. Cause of Becoming Non-Effective", "non_effective_cause", "text"),
        14: Field("13. Single or Married", "marital_status", "text"),
        15: Field("14. Home Town and Country (U.K.) or Country", "hometown", "text"),
        16: Field("A. Rank", "rank", "text"),
        17: Field("B. Service Trade and Classification", "service_trade", "text"),
        18: Field("C. Medical Category", "medical_category", "text"),
        19: Field("19. Location", "location", "text"),
    }

    async def validate_ddmmyyyy(value: str) -> Optional[str]:
        """Validate date strings for date input fields,
        handling 2-digit and 4-digit years."""
        try:
            day, month, year = map(int, value.split("/"))

            # @TODO Validate single-digit years correctly
            if 0 <= year <= 49:  # 2-digit years
                year = 1900 + year  # Early C20th
            elif 50 <= year <= 99:
                year = 1800 + year  # Late C19th
            elif 1800 <= year <= 1950:  # Valid 4-digit year
                pass
            else:
                return "Invalid year. Must be between 1800 and 1950."
            date(year, month, day)  # Validate the date
            return None

        except (AttributeError, ValueError, TypeError) as e:
            print(e)
            return "Invalid date format. Use DD/MM/YY or DD/MM/YYYY."

    @ui.refreshable
    def create_inputs(fields: dict[int, list[Field]], form: FormB102r) -> None:
        """Create a series of inputs based on a model."""
        ordered_fields: list = sorted(fields.items())

        for field in ordered_fields:
            label, field_name, field_type = (
                field[1].label,
                field[1].db_field,
                field[1].type,
            )
            if field_type == "text":
                ui.input(label=label).bind_value(form, field_name).props(
                    "outlined hide-bottom-space"
                )
            if field_type == "date":
                with ui.input(
                    "Date of Birth",
                    placeholder="Pick date",
                    validation=validate_ddmmyyyy,
                ).props("outlined hide-bottom-space") as date_input:
                    with ui.menu().props("no-parent-event") as menu:
                        with (
                            ui.date(mask="DD/MM/YYYY")
                            .bind_value(date_input)
                            .props(
                                '''default-year-month=1910/01
                                :options="date => date <= '1945/01/01'"'''
                            )
                        ):
                            with ui.row().classes("justify-end"):
                                ui.button("Close", on_click=menu.close).props("flat")
                    with date_input.add_slot("append"):
                        ui.icon("edit_calendar").on("click", menu.open).classes(
                            "cursor-pointer"
                        )

    def save_changes() -> None:
        assert frm is not None, "Expected frm to be loaded"
        assert original_frm is not None, "Expected original_frm to be loaded"

        with Session(engine) as session:
            save_form_with_log(
                session,
                updated_form=frm,
                original_form=original_frm,
                change_reason="muster",
            )
        ui.notify("Changes saved", color="positive", position="center")

    def discard_changes() -> None:
        """Discard all changes made by user and reload all fields from the database."""
        load_form(frm.id)  # type: ignore
        create_inputs.refresh(fields_list, frm)

    def confirm_discard() -> None:
        confirm_discard_dialog.close()
        discard_changes()

    # Confirm discard dialog to ensure the user really means it
    confirm_discard_dialog = ui.dialog()

    with confirm_discard_dialog:
        with ui.card().classes("w-80"):
            ui.label("Are you sure you want to discard all changes?")
            with ui.row().classes("justify-end gap-2"):
                ui.button("Cancel", on_click=confirm_discard_dialog.close)
                ui.button(
                    "Discard",
                    color="warning",
                    icon="delete_forever",
                    on_click=lambda: (confirm_discard()),
                )

    with ui.row().classes("w-full justify-between no-wrap"):
        # Left column: fields
        with ui.scroll_area().classes("w-1/4 h-[60vh] border"):
            with ui.column().classes("w-full"):
                with ui.row().classes("w-full justify-between no-wrap"):
                    # Text fields
                    with ui.column().classes("full"):
                        assert frm is not None
                        create_inputs(fields_list, frm)

        # Right column: image
        with ui.column().classes("w-3/4"):
            assert frm is not None
            img = str(frm.form_image)
            with ui.element("div").classes("w-full max-h-[60vh] overflow-x-hidden"):
                ui.image(f"/images/{img}").classes("w-full h-full object-contain")

            with ui.row().classes("w-full justify-between"):
                with ui.button(
                    "Discard",
                    icon="delete_forever",
                    on_click=lambda: confirm_discard_dialog.open(),
                ).props("color=warning"):
                    ui.tooltip("Discard all changes")
                with ui.button(
                    "Save",
                    icon="save",
                    on_click=lambda: save_changes(),
                ).props("color=primary"):
                    ui.tooltip("Save all changes")
