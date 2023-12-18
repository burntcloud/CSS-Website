from dash import dcc, html, register_page, callback, State, Output, Input
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

register_page(__name__, path="/question")
question_1 = {"hhhh": "hhh"}

card = dbc.Card([
    dbc.CardBody([
        html.H4("Default Question?", id="question_field", className="card-title"),
        html.P(
            dcc.RadioItems(options=[], value="", id='radio_input'),
            id="radio_items",
            className="card-text",
        ),
        dcc.Link(dbc.Button(id='submit_button', children="Submit"), href="/answer", refresh=True),
        html.Div(id='output_div', children="", style={"margin-left": "15px"})
    ],
        id='card'
    ),
],
    style={"width": "18rem"},
)

layout = html.Div(children=[
    dcc.Location(id='url_question', refresh=False),
    html.H1(
        children="Test Question",
        style={'textAlign': 'center', 'color': '#AAABBB'}
    ),
    card
])


# When loading the page, the location element triggers this callback
# It finds the current index in the global store and loads the corresponding question
@callback(Output('question_field', 'children'),
          Output('radio_items', 'children'),
          Input('url_question', 'pathname'),
          State('global_store', 'data'))
def load_question(pathname, data):
    question_index = data["index"]
    question = data["Questions"][question_index]["question_text"]
    options = data["Questions"][question_index]["options"]
    radio_items = dcc.RadioItems(options=options, value=options[0], id='radio_input')
    return question, radio_items


# When the radio input changes, remember the user's answer
@callback(Output('global_store', 'data', allow_duplicate=True),
          Input('radio_input', 'value'),
          State('global_store', 'data'),
          prevent_initial_call=True)
def update_store(radio_value, data):
    data["user_choice"] = radio_value
    return data
