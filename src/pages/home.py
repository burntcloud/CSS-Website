from dash import dcc, html, register_page, callback, State, Output, Input, get_asset_url
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

register_page(__name__, path="/")

lang_buttons = dbc.RadioItems(
    id="lang_buttons",
    className="btn-group",
    inputClassName="btn-check",
    labelClassName="btn btn-outline-primary",
    options=[{"label": "Deutsch", "value": "Deutsch"},
             {"label": "English", "value": "English"}],
    value="Deutsch",
    style={"float": "right"}
)

layout = html.Div(
    children=[
        dbc.Container([
            dbc.Row(
                [dbc.Col(html.H1("CSS Quizpage", style={'font-size': '70px'})),
                 dbc.Col(lang_buttons)

                 ]
            ),
            dbc.Row(
                # html.Img(src=get_asset_url('NS_Doku_Logo.png'), style={'width': '20%'})
            ),
            dbc.Row(
                dbc.Card([
                    dbc.CardBody(id="intro_card")
                ])),
            dbc.Row(
                dcc.Link(
                    dbc.Button("Start Quiz", id="start_button",
                               style={'font-size': '20px', "background-color": "#348994", "border": "none"}),
                    href="/question", refresh=True))
        ])
    ]
)


# for button update callback input output etc

@callback(Output('global_store', 'data', allow_duplicate=True),
          Output('intro_card', 'children'),
          Output('start_button', 'children'),
          Input('lang_buttons', 'value'),
          State('global_store', 'data'),
          prevent_initial_call=True)
def update_store(value, data):
    data["language"] = value
    if value == "English":
        children = [html.H2(data["Introduction"]["header"])]
        for x in data["Introduction"]["content"]:
            children.append(html.P(x))
        children2 = "Start Quiz"
    if value == "Deutsch":
        children = [html.H2(data["Einführung"]["header"])]
        for x in data["Einführung"]["content"]:
            children.append(html.P(x))
        children2 = "Quiz starten"
    return data, children, children2
