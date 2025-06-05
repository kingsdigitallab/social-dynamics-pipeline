from nicegui import ui


def render(form_id):
    """Create the form editing page for a form specified by unique ID"""
    ui.label(f"This is the form for {form_id}")
