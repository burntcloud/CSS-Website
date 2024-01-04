import dash
from dash import Dash, html, callback, State, Output, Input, dcc
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import json
import __main__ as main
main.__file__ = "main_file"


with open('questions.json', "r") as f:
    # load questions from json file and set current question index to 0
    questions = json.load(f)
    questions["index"] = 0


#app = Dash(external_stylesheets=[dbc.themes.SOLAR], use_pages=True, suppress_callback_exceptions=True)
app = Dash(external_stylesheets=[dbc.themes.SOLAR], use_pages=True)
server = app.server

app.layout = html.Div(children=[
    dash.page_container,
    dcc.Store(id="global_store", storage_type="session", data=questions),
])


if __name__ == '__main__':
    app.run(debug=True)
