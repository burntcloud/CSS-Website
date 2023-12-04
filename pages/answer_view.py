from dash import html, register_page

register_page(__name__, path="/answer")

layout = html.Div(children=[
    html.H1(
        children="Test answer view",
        style={'textAlign': 'center', 'color': '#AAABBB'})
])
