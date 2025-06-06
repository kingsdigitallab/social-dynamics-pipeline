from nicegui import ui


def layout_css():
    ui.add_css(
        """
    /* Prevents toggle disappearing when dark mode is on */
    .dark-toggle .q-toggle__track {
        background-color: #ccc !important;
    }
    .dark-toggle .q-toggle__thumb {
        color: #444 !important;
    }
    """
    )


def home_css():
    ui.add_css(
        """
    /* Round corners of tabs */
    .q-tab {
        border-top-left-radius: 0.5rem !important;
        border-top-right-radius: 0.5rem !important;
    }
    /* Unselected tabs are greyed out */
    .q-tab:not(.q-tab--active) {
        background-color: #e5e7eb; /* Tailwind gray-200 */
        color: #1f2937; /* Tailwind gray-800 for text */
        transition: background-color 0.2s ease;
    }
    /* Tab content area background */
    .q-tab-panel {
        background-color: var(--q-primary);
        color: white;
        border-radius: 0 0 0.5rem 0.5rem;
    }
    /* Form header is same colour as tab content area */
    .database-table thead tr {
        background-color: var(--q-primary);
        color: white;
    }
    /* */
    .database-table tr.selected {
        background-color: lightgray;
    }
    """
    )


def correct_css():
    ui.add_css(
        """
    """
    )
