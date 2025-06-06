from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response
from nicegui import app, ui
from nicegui.client import Client
from nicegui.error import error_content
from sqlmodel import Session

from pipeline.database.init_db import engine
from pipeline.database.models import FormB102r
from pipeline.ui.config import settings
from pipeline.ui.muster.views.correct import render as render_correct
from pipeline.ui.muster.views.home import render as render_home
from pipeline.ui.muster.views.layout import layout


@app.exception_handler(RequestValidationError)
async def _exception_handler_422(
    request: Request, exception: RequestValidationError
) -> Response:
    """Generates custom error page when page parameter is invalid"""
    from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

    with Client(page(""), request=request) as client:
        error_content(HTTP_422_UNPROCESSABLE_ENTITY, exception)
    return client.build_response(request, HTTP_422_UNPROCESSABLE_ENTITY)


@ui.page("/", title="Roll Review Centre")
def home():
    with layout(
        title="Roll Review Centre",
        description="""Browse all available individuals and forms.
    Search and select forms for correction.""",
    ):
        render_home()


@ui.page("/correct/{form_id}", title="Form Correction Page")
def page(form_id: int):
    with Session(engine) as session:
        form = session.get(FormB102r, form_id)

    if not form:
        raise HTTPException(status_code=404, detail=f"Form {form_id} not found.")

    with layout(
        title="Form Correction Page",
        description="Review and correct the data for this form.",
    ):
        render_correct(form_id)


app.add_static_files(
    str(settings.images_url_base),
    str(settings.images_dir),
)
ui.run(title="Main App", port=8080)
