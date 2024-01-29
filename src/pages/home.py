# -*- coding: utf-8 -*-
from dash import dcc, html, register_page, callback, State, Output, Input, get_asset_url
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import random

register_page(__name__, path="/")


layout = html.Div(
    children=[
        dcc.Location(id='home', refresh=False),
        dbc.Container([
            dbc.Row(
                # html.Img(src=get_asset_url('NS_Doku_Logo.png'), style={'width': '20%'})
            ),
            dbc.Row(
                dbc.Card([
                    dbc.CardBody(id="intro_card")
                ])),
            dbc.Row(
                dcc.Link(
                    dbc.Button("Start Quiz", id="start_button",
                               style={'font-size': '20px', "background-color": "#348994", "border": "none"}),
                    href="/question", refresh=True))
        ])
    ]
)


# for button update callback input output etc
@callback(Output('intro_card', 'children'),
          Output('start_button', 'children'),
          Input('home', 'pathname'),
          State('global_store', 'data'))
def update_text(pathname, data):
    language = data['language']
    if language == "English":
        children = [html.H2(data["Introduction"]["header"])]
        for x in data["Introduction"]["content"]:
            children.append(html.P(x))
        children2 = "Start Quiz"
    if language == "Deutsch":
        children = [html.H2(data["Einführung"]["header"])]
        for x in data["Einführung"]["content"]:
            children.append(html.P(x))
        children2 = "Quiz starten"
    return children, children2


# sample one question per position randomly and store the new list in data[language] for each language
@callback(Output('global_store', "data"),
          Input("home", "pathname"),
          State("global_store", "data"))
def prepare_question_list(pathname, data):
    language_keywords = data["language_keywords"]
    first_language = language_keywords[0]
    positions = list(set([q['position'] for q in data["all_questions"][first_language]]))
    chosen_ids = []
    all_questions = data["all_questions"][first_language]
    # step 1: get one id for each position
    for position in positions:
        ids = [q['id'] for q in all_questions if q['position'] == position]
        chosen_ids.append(ids[random.randint(0, len(ids)-1)])
    # step 2: filter the question lists for every language to contain only chosen ids
    for language in language_keywords:
        question_list = data["all_questions"][language]
        question_list = [q for q in question_list if q["id"] in chosen_ids]
        data[language] = sorted(question_list, key=lambda q: q['position'])
    return data
