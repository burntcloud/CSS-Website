import dash
from dash import Dash, html, callback, State, Output, Input, dcc, callback_context
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import json
import __main__ as main
import random

main.__file__ = "main_file"


with open('questions.json', "r") as f:
    # load questions from json file and set current question index to 0
    questions = json.load(f)

# store all questions from the json in all_questions to sample randomly from them
languages = ["Deutsch", "English"]
questions["all_questions"] = {x: questions[x] for x in languages}
questions["index"] = 0
questions["language"] = languages[0]
questions["language_keywords"] = languages

app = Dash(external_stylesheets=[dbc.themes.SOLAR], use_pages=True, meta_tags=[{'name': 'viewport',
                                                                                'content': 'width=device-width, '
                                                                                           'initial-scale=1.0, '
                                                                                           'maximum-scale=1.2, '
                                                                                           'minimum-scale=0.5,'}])
server = app.server

footer = html.Footer(
    dbc.Container(
        dbc.Row([
            dbc.Col(html.A(href="/", children="Home", id="home_link")),
            dbc.Col(html.A(href="/privacy", children="Privacy Policy", id="privacy_link")),
            dbc.Col(html.A(href="/imprint", children="Imprint", id="imprint_link"))
        ], justify="evenly")
    )
)

progress_bar = dbc.Progress(id="progress")

lang_buttons = dbc.RadioItems(
    id="lang_buttons",
    className="btn-group",
    inputClassName="btn-check",
    labelClassName="btn btn-outline-primary",
    options=[{"label": "Deutsch", "value": "Deutsch"},
             {"label": "English", "value": "English"}],
    style={"float": "right"},
    value=None
)

header = dbc.Container([
    dbc.Row([
        dbc.Col(
            dcc.Link(
                html.H1("", style={'font-size': '70px'}, id="page_title"),
                href="/",
                style={"textDecoration": "none"}
            )
        ),
        dbc.Col(lang_buttons)
    ])
])

app.layout = html.Div(children=[
    dcc.Location(id="url"),
    dcc.Store(id="global_store", storage_type="session", data=questions),
    header,
    progress_bar,
    dash.page_container,
    footer
])


# update the progress bar,
@callback(Output('progress', 'value'),
          Output('progress', 'label'),
          Input('url', 'pathname'),
          State('global_store', 'data'))
def load_progress(pathname, data):
    question_index = data["index"]
    language = data["language"]
    max_id = len(data[language]) - 1
    progress_num = min((question_index/(max_id+1))*100, 100)
    label = f"{progress_num} %" if progress_num >= 5 else ""
    # return "Question " + str(data["Questions"][question_index]["id"])
    return progress_num, label


@callback(Output('home_link', "children"),
          Output('privacy_link', "children"),
          Output('imprint_link', "children"),
          Output("page_title", "children"),
          Input("url", "href"),
          State("global_store", "data"))
def update_main_page(pathname, data):
    if data["language"] == "Deutsch":
        return "Startseite", "Datenschutzerklärung", "Impressum", "CSS Quizz"
    else:
        return "Home", "Privacy", "Imprint", "CSS Quiz"


# callback to
# 1. change the language and reload the page (if triggered by language button change)
# 2. change the value of the language button to the old value after a page reload (if triggered by page reload)
# Needs to be in one callback to avoid infinite loop
# _pages_location.pathname contains the current page url, needed for refreshing the page
@callback(Output('global_store', 'data', allow_duplicate=True),
          Output('url', "href", allow_duplicate=True),
          Output('lang_buttons', "value"),
          Input("lang_buttons", "value"),
          Input("url", "href"),
          State('_pages_location', 'pathname'),
          State("global_store", "data"),
          prevent_initial_call=True)
def change_language(value, pathname, current_page, data):
    changed_inputs = [x["prop_id"] for x in callback_context.triggered]
    if "url.href" in changed_inputs:
        return dash.no_update, dash.no_update, data['language']
    if "lang_buttons.value" in changed_inputs:
        data["language"] = value
        return data, current_page, dash.no_update
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, port=8051)
