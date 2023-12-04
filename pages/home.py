from dash import dcc, html, register_page

register_page(__name__, path="/")

layout = html.Div([
    html.H1("Home Page"),
    dcc.Link(html.Button("start quiz"), href="/question", refresh=True)
])
