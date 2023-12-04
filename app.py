from dash import Dash, dcc, html, callback, State, Output, Input
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.SOLAR])

markdown_text = '''
### Markdown

This is a very simple way to do [links](http://commonmark.org/)!
'''

card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Was ist dein Lieblingsessen?", className="card-title"),
                html.P(
                    dcc.RadioItems(options=['Pizza', 'Spagetti', 'Sushi'], value='Pizza', id='radio-input'),
                    className="card-text",
                ),
                html.Button(id='submit-button-state', children='Submit'),
                html.Div(id='output-div', children="", style={"margin-left": "15px"})
            ]
        ),
    ],
    style={"width": "18rem"},
)

app.layout = html.Div(children=[
    html.H1(
        children="Test Webpage",
        style={'textAlign': 'center', 'color': '#AAABBB'}
    ),
    #dcc.Markdown(children=markdown_text),
    #html.Label("Was ist dein Lieblingsessen?"),
    #dcc.RadioItems(options=['Pizza', 'Spagetti', 'Sushi'], value='Pizza', id='radio-input'),
    #html.Button(id='submit-button-state', children='Submit'),
    #html.Div(id='output-div', children="", style={"margin-left": "15px"}),
    card
])


@callback(Output('output-div', 'children'),
          Input('submit-button-state', 'n_clicks'),
          State('radio-input', 'value'))
def update_output(n_clicks, radio_input):
    if n_clicks is None:
        raise PreventUpdate
    return html.Div([f'Ich mag auch gerne {radio_input}', html.Button(children="Next")])


if __name__ == '__main__':
    app.run(debug=True)
