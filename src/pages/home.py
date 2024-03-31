# -*- coding: utf-8 -*-
import random

import dash_bootstrap_components as dbc
from dash import dcc, html, register_page, callback, State, Output, Input
from dash.exceptions import PreventUpdate

# register sub page home
register_page(__name__, path="/")

# LAYOUT
layout = html.Div(
    children=[
        dcc.Location(id='home', refresh=False),
        dbc.Container([
            dbc.Row(
                # html.Img(src=get_asset_url('NS_Doku_Logo.png'), style={'width': '20%'})
            ),
            dbc.Row(
                dbc.Card([
                    dbc.CardBody(id="intro_card", style={'font-size': '22px'})
                ])),
            dbc.Row(
                dcc.Link(
                    dbc.Button("Start Quiz", id="start_button",
                               style={'font-size': '20px', "background-color": "#348994", "border": "none"}),
                    href="/question", refresh=True))
        ])
    ]
)


# CALLBACKS
@callback(Output('intro_card', 'children'),
          Output('start_button', 'children'),
          Input('home', 'pathname'),
          State('global_store', 'data'))
def update_text(pathname, data):
    """
    When the page loads, load the introduction text and the text on the start button in the correct language.

    parameters:
    - pathname (str): url.pathname, current location (not used, only to trigger the callback when the page loads)
    - data (dict): global_store.data, global memory

    return values:
    - (list(html.P()): list of html paragraphs of the introduction text
    - (str): text on the start quiz button
    """
    language = data['language']
    if language == "English":
        children = [html.H2(data["Introduction"]["header"])]
        for x in data["Introduction"]["content"]:
            children.append(html.P(x))
        children2 = "Start Quiz"
    elif language == "Deutsch":
        children = [html.H2(data["Einführung"]["header"])]
        for x in data["Einführung"]["content"]:
            children.append(html.P(x))
        children2 = "Quiz starten"
    else:
        raise PreventUpdate
    return children, children2


# sample one question per position randomly and store the new list in data[language] for each language
@callback(Output('global_store', "data"),
          Input("home", "pathname"),
          State("global_store", "data"))
def prepare_question_list(pathname, data):
    """
    Prepare the quiz run by sampling one question per position randomly and storing the new question list in data[language]
    for each language

    parameters:
    - pathname (str): url.pathname, current location (not used, only to trigger the callback when the page loads)
    - data (dict): global_store.data, global memory

    return values:
    - (dict): global_store.data, the updated global memory with the questions list for this quiz run
    """
    language_keywords = data["language_keywords"]
    data["index"] = 0
    data["user_choice"] = {}
    first_language = language_keywords[0]
    positions = list(set([q['position'] for q in data["all_questions"][first_language]]))
    chosen_ids = []
    all_questions = data["all_questions"][first_language]
    # step 1: get one id for each position
    for position in positions:
        ids = [q['id'] for q in all_questions if q['position'] == position]
        chosen_ids.append(ids[random.randint(0, len(ids) - 1)])
    # step 2: filter the question lists for every language to contain only chosen ids
    for language in language_keywords:
        question_list = data["all_questions"][language]
        question_list = [q for q in question_list if q["id"] in chosen_ids]
        data[language] = sorted(question_list, key=lambda q: q['position'])
    return data
