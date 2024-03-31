import dash_bootstrap_components as dbc
from dash import html, register_page, dcc, callback, Input, Output, State

# register privacy sub-page
register_page(__name__, path="/privacy")

# LAYOUT
layout = dbc.Container([
    dcc.Location(id='url_privacy', refresh=False),
    dbc.Row(
        [html.H1(
            "Privacy Policy",
            id="policy_header"
        )],
        style={"textAlign": "center"}
    ),
    dbc.Row(
        [html.P(
            "We do not store any data and so on.......",
            id="policy_text"
        )],
    )
])


# CALLBACKS
@callback(
    Output('policy_header', 'children'),
    Output('policy_text', 'children'),
    Input('url_privacy', 'pathname'),
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
        key = "Privacy Policy"
    if language == "Deutsch":
        key = "Datenschutz"

    return data[key]['header'], data[key]['content']
