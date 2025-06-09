import copy

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

    text_fields = {
        1: ["1. Surname", "lastname"],
        2: ["2. Christian Names", "firstname"],
        3: ["3. Army Number", "army_number"],
        4: ["4. Regiment or Corps", "regiment_or_corp"],
        5: ["5. Nature of Engagement", "engagement"],
        6: ["6. Date of Joining / Enlistment", "date_of_enlistment"],
        7: ["7. Date of Birth", "dob"],
        8: ["8. Nationality", "nationality"],
        9: ["9. Religion", "religion"],
        10: ["10. Industry Group", "industry_group"],
        11: ["11. Occupational Classification", "occupation"],
        12: ["12. Cause of Becoming Non-Effective", "non_effective_cause"],
        13: ["13. Single or Married", "marital_status"],
        14: ["14. Home Town and Country (U.K.) or Country", "hometown"],
        15: ["A. Rank", "rank"],
        16: ["B. Service Trade and Classification", "service_trade"],
        17: ["C. Medical Category", "medical_category"],
        18: ["19. Location", "location"],
    }

    # lookup_fields = {
    #     1: ["1. Surname", "lastname"],
    #     2: ["2. Christian Names", "firstname"],
    #     3: ["3. Army Number", "army_number"],
    #     4: ["4. Regiment or Corps", "regiment_or_corp"],
    #     5: ["5. Nature of Engagement", "engagement"],
    #     6: ["6. Date of Joining / Enlistment", "date_of_enlistment"],
    #     7: ["7. Date of Birth", "dob"],
    #     8: ["8. Nationality", "nationality"],
    #     9: ["9. Religion", "religion"],
    #     10: ["10. Industry Group", "industry_group"],
    #     11: ["11. Occupational Classification", "occupation"],
    #     12: ["12. Cause of Becoming Non-Effective", "non_effective_cause"],
    #     13: ["13. Single or Married", "marital_status"],
    #     14: ["14. Home Town and Country (U.K.) or Country", "hometown"],
    #     15: ["A. Rank", "rank"],
    #     16: ["B. Service Trade and Classification", "service_trade"],
    #     17: ["C. Medical Category", "medical_category"],
    #     18: ["19. Location", "location"],
    # }

    @ui.refreshable
    def create_inputs(
        fields: dict[int, list[str]], form: FormB102r, field_type: str = "text"
    ) -> None:
        """Create a series of inputs based on a model. Default input type is 'text'"""
        ordered_fields: list = sorted(fields.items())
        if field_type == "text":
            for field in ordered_fields:
                label, field_name = field[1][0], field[1][1]
                ui.input(label=label).bind_value(form, field_name).props(
                    "outlined hide-bottom-space"
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
        create_inputs.refresh(text_fields, frm)

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
                        create_inputs(text_fields, frm)
                    # Lookup fields
                    # with ui.column().classes("w-1/2"):
                    #     create_inputs(lookup_fields, frm, field_type="lookup")

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
