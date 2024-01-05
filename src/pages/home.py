from dash import dcc, html, register_page, callback, State, Output, Input, get_asset_url
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc


register_page(__name__, path="/")

layout = html.Div([
    html.H1("Home Page"),
    #dcc.Link(dbc.Button(dbc.Card([dbc.CardImg(src=get_asset_url('workinghours.png'), top=True), dbc.CardBody("start quiz")], className="border-0 bg-transparent", inverse=True, style={"width": "18rem"}), id="start_quiz_button", outline=True, color="light"), href="/question", refresh=True)
    dcc.Link(dbc.Button("start quiz"), href="/question", refresh=True)
])
