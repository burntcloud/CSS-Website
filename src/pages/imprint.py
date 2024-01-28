from dash import html, register_page, dcc, callback, Input, Output, State, get_asset_url
import dash_bootstrap_components as dbc

register_page(__name__, path="/imprint")

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


@callback(
    Output('imprint_header', 'children'),
    Output('imprint_text', 'children'),
    Input('url_imprint', 'pathname'),
    State('global_store', 'data'))
def load_header(pathname, data):
    language = data["language"]
    key = ""
    if language == "English":
        key = "Imprint"
    if language == "Deutsch":
        key = "Impressum"

    return data[key]['header'], data[key]['content']
