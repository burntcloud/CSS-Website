from dash import dcc, html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/question")

card = dbc.Card([
    dbc.CardBody([
        html.H4("Was ist dein Lieblingsessen?", className="card-title"),
        html.P(
            dcc.RadioItems(options=['Pizza', 'Spagetti', 'Sushi'], value='Pizza', id='radio-input'), className="card-text"),
            html.Button(id='submit-button-state', children="Submit"),
            html.Div(id='output-div', children="", style={"margin-left": "15px"})
        ],
            id='card'
        ),
],
    style={"width": "18rem"},
)

layout = html.Div(children=[
    html.H1(
        children="Test Question",
        style={'textAlign': 'center', 'color': '#AAABBB'}
    ),
    card
])


