import dash_bootstrap_components as dbc
from dash import html, register_page, dcc, callback, Input, Output, State

# register the imprint sub-page
register_page(__name__, path="/imprint")

# LAYOUT
layout = dbc.Container([
    dcc.Location(id='url_imprint', refresh=False),
    dbc.Row(
        [html.H1(
            id="imprint_header"
        )],
        style={"textAlign": "center"}
    ),
    dbc.Row(
        [html.P(
            id="imprint_text"
        )],
    )
])


# CALLBACKS
@callback(
    Output('imprint_header', 'children'),
    Output('imprint_text', 'children'),
    Input('url_imprint', 'pathname'),
    State('global_store', 'data'))
def load_header(pathname, data):
    """
    When the page loads, update all texts depending on the chosen language.

    parameters:
    - pathname (str): url.pathname, current location (not used, only to trigger the callback when the page loads)
    - data (dict): global_store.data, global memory

    return values:
    - (str): imprint_header.children, title of the page
    - (str): imprint_text.children, imprint text
    """
    language = data["language"]
    key = ""
    if language == "English":
        key = "Imprint"
    if language == "Deutsch":
        key = "Impressum"

    return data[key]['header'], data[key]['content']
