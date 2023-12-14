from dash import dcc, html, register_page, callback, State, Output, Input
from dash.exceptions import PreventUpdate

register_page(__name__, path="/")

layout = html.Div([
    html.H1("Home Page"),
    dcc.Link(html.Button("start quiz", id="start_quiz_button"), href="/question", refresh=True)
])
