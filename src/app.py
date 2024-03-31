# -*- coding: utf-8 -*-
import __main__ as main
import json

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, callback, State, Output, Input, dcc, callback_context
from dash.exceptions import PreventUpdate

main.__file__ = "main_file"

# preparations before starting the app
with open('questions.json', "r") as f:
    # load questions from json file and set current question index to 0
    questions = json.load(f)

# store all questions from the json in all_questions to sample randomly from them
languages = ["Deutsch", "English"]
questions["all_questions"] = {x: questions[x] for x in languages}
questions["index"] = 0
questions["language"] = languages[0]
questions["language_keywords"] = languages
questions["user_choice"] = {}

# initialize the Dash app
app = Dash(external_stylesheets=[dbc.themes.SOLAR], use_pages=True, meta_tags=[{'name': 'viewport',
                                                                                'content': 'width=device-width, '
                                                                                           'initial-scale=1.0, '
                                                                                           'maximum-scale=1.2, '
                                                                                           'minimum-scale=0.5,'}])
server = app.server

# LAYOUT
# define main layout for all subpages: header, progress bar and footer
footer = html.Footer(
    dbc.Container(
        dbc.Row([
            dbc.Col(html.A(href="/", children="Home", id="home_link")),
            dbc.Col(html.A(href="/privacy", children="Privacy Policy", id="privacy_link")),
            dbc.Col(html.A(href="/imprint", children="Imprint", id="imprint_link"))
        ], justify="evenly")
    )
)

progress_bar = dbc.Progress(id="progress", label="test")

# two buttons to change the language, radio items designed as buttons
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
                html.H1("", style={'font-size': '60px'}, id="page_title"),
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


# CALLBACKS
@callback(Output('progress', 'value'),
          Input('url', 'pathname'),
          State('global_store', 'data'))
def load_progress(pathname, data):
    """
    Update the progress bar.

    parameters:
    - pathname (str): url.pathname, current location
    - data (dict): global_store.data, global memory

    return values:
    - (int): progress.value, new state of the progress bar
    """
    if pathname == "/":
        data["index"] = 0
        data["user_choice"] = {}
    question_index = data["index"]
    language = data["language"]
    max_id = len(data[language]) - 1
    progress_num = min((question_index / (max_id + 1)) * 100, 100)
    return progress_num


@callback(Output("home_link", "children"),
          Output("privacy_link", "children"),
          Output("imprint_link", "children"),
          Output("page_title", "children"),
          Input("url", "href"),
          State("global_store", "data"))
def update_main_page(pathname, data):
    """
    When the page loads, update all texts to the current language.

    parameters:
    - pathname (str): url.href, url of the current location (not used, only as trigger of the callback)
    - data (dict): global_store.data, current global memory

    return values:
    - (str): text of the home link
    - (str): text of the privacy policy link
    - (str): text of the imprint link
    - (str): text of the website title / logo in the top left corner
    """
    if data["language"] == "Deutsch":
        return "Startseite", "Datenschutzerklärung", "Impressum", "Erinnern an Zwangsarbeit - Quiz"
    else:
        return "Home", "Privacy", "Imprint", "Remembering Forced Labor - Quiz"


@callback(Output('global_store', 'data', allow_duplicate=True),
          Output('url', "href", allow_duplicate=True),
          Output('lang_buttons', "value"),
          Input("lang_buttons", "value"),
          Input("url", "href"),
          State('_pages_location', 'pathname'),
          State("global_store", "data"),
          prevent_initial_call=True)
def change_language(value, pathname, current_page, data):
    """
    callback to
        1. change the language and reload the page (if triggered by language button change)
        2. change the value of the language button to the old value after a page reload (if triggered by page reload)
    Needs to be in one callback to avoid infinite loop

    parameters:
    - value (str): lang_buttons.value, value of the currently selected language button, either "English" or "Deutsch"
    - pathname (str): url.href, url of the current location (not used, only as trigger of the callback)
    - current_page: (str): _pages_location.pathname, the current page url, needed for refreshing the page
    - data (dict): global_store.data, current global memory

    return values:
    - (dict): global_store.data, global memory with updated language
    - (str): url.href, name of the current page, returning it causes the page to reload
    - (str): lang_buttons.value, state of the language buttons, either "English" or "Deutsch"
    """
    changed_inputs = [x["prop_id"] for x in callback_context.triggered]
    if "url.href" in changed_inputs:
        # page is loaded, only change the value of the language buttons
        return dash.no_update, dash.no_update, data['language']
    if "lang_buttons.value" in changed_inputs:
        # user clicked the language buttons, reload the current page
        data["language"] = value
        return data, current_page, dash.no_update
    else:
        # this should not happen
        raise PreventUpdate


# start the app
if __name__ == '__main__':
    app.run(debug=True)
