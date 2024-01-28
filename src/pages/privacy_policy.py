from dash import html, register_page, dcc, callback, Input, Output, State, get_asset_url
import dash_bootstrap_components as dbc

register_page(__name__, path="/privacy")

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


@callback(
    Output('policy_header', 'children'),
    Output('policy_text', 'children'),
    Input('url_privacy', 'pathname'),
    State('global_store', 'data'))
def load_header(pathname, data):
    language = data["language"]
    key = ""
    if language == "English":
        key = "Privacy Policy"
    if language == "Deutsch":
        key = "Datenschutz"

    return data[key]['header'], data[key]['content']
