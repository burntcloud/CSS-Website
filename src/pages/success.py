from dash import dcc, html, register_page, callback, State, Output, Input, get_asset_url
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import random

register_page(__name__, path="/success")

layout = html.Div(
    children=[
        dcc.Location(id='success', refresh=False),
        dbc.Container([
            dbc.Row(
                # html.Img(src=get_asset_url('NS_Doku_Logo.png'), style={'width': '20%'})
            ),
            dbc.Row(
                dbc.Card([
                    dbc.CardBody(id="success_text")
                ])),
            dbc.Row(
                dcc.Link(
                    dbc.Button(id="back_button",
                               style={'font-size': '20px', "background-color": "#348994", "border": "none"}),
                    href="/", refresh=True))
        ])
    ]
)


@callback(Output('back_button', "children"),
          Output('success_text', "children"),
          Input("success", "href"),
          State("global_store", "data"))
def update_main_page(pathname, data):
    language = data["language"]
    if language == "Deutsch":
        return "Zurück", data["Fazit"]
    else:
        return "Home", data["Conclusion"]
