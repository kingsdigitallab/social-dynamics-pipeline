from nicegui import ui
from sqlmodel import Session

from pipeline.database.helpers.form_b102r import get_form
from pipeline.database.init_db import engine
from pipeline.database.models import FormB102r
from pipeline.ui.muster.views.css import correct_css


def render(form_id: int):
    """Create the form editing page for a form specified by unique ID"""

    correct_css()

    with ui.row().classes("w-full items-center justify-between"):
        ui.html(f"<h3 class='text-xl font-bold my-4'>PDF: {form_id}</h2>")
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

    def create_inputs(
        fields: dict[int, list[str]], form: FormB102r, field_type: str = "text"
    ) -> None:
        ordered_fields: list = sorted(fields.items())
        if field_type == "text":
            for field in ordered_fields:
                label, field_name = field[1][0], field[1][1]
                field_label = ui.label(label)
                ui.input().bind_value(form, field_name).props(
                    "outlined hide-bottom-space stack-label"
                ).on(
                    "focus", lambda label=field_label: label.style("font-weight: bold;")
                ).on(
                    "blur",
                    lambda label=field_label: label.style("font-weight: normal;"),
                )

    with Session(engine) as session:
        frm = get_form(session, form_id)
        print(frm)

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
                # with ui.page_sticky(position="top-right", expand=False):
                #     ui.label("Sticky")
                #     ui.image("/images/APV002231437_page22_img1.jpg").props(
                #         ":width='250'"
                #     )

                assert frm is not None
                img = str(frm.form_image)
                ui.image(f"/images/{img}")
