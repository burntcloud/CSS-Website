# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
from dash import dcc, html, register_page, callback, State, Output, Input, get_asset_url

# register question sub-page
register_page(__name__, path="/question")

# LAYOUT
# blueprint for the answer options, styled as radio buttons
answer_options = dbc.Container(
    dbc.RadioItems(
        options=[],
        value="",
        id='radio_input',
        # className="btn-group",  # all in one line
        inputClassName="btn-check",  # remove circles
        labelClassName="btn btn-outline-secondary btn-lg",  # make options look like buttons
        inline=True
    ), style={"padding-left": "0px"}, className="radio-group")

# blueprint for the question view layout, needs ids "header", "image", "description_text", "question_text" and
# "submit_button"
question_layout = html.Div(
    [
        dbc.Container([
            html.H1(children="", id="header", style={"text-align": "center"}),
            dbc.Card([html.Center(
                html.Div(id="image")),
                dbc.CardBody([
                    html.P(id="description_text", className="card-text", style={'font-size': '20px'}),
                    html.H4(id="question_text", style={'font-size': '20px', 'font-weight': 'bold'}),
                    answer_options,
                    dcc.Link(dbc.Button(id='submit_button', children="Submit",
                                        style={"margin-top": "30px", "fontSize": "20px", "background-color": "#348994",
                                               "border": "none"}), href="/answer", refresh=True)
                ])
            ])
        ],
        )
    ],
    id="question_layout"
)

layout = html.Div(children=[
    dcc.Location(id='url_question', refresh=False),
    question_layout,
])


# CALLBACKS
@callback(Output('image', 'children'),
          Output('image', 'style'),
          Input('url_question', 'pathname'),
          State('global_store', 'data'))
def load_image(pathname, data):
    """
    On page load, insert or delete the question's image and if necessary adapt size.

    parameters:
    - pathname (str): url.pathname, current location (not used, only to trigger the callback when the page loads)
    - data (dict): global_store.data, global memory

    return values:
    - (Optional([dbc.CardImg, html.P])): image.children, None if there is no image, otherwise it contains the
    answer image and the image description as html paragraph
    - (dict): image.style, dictionary with the image's css style

    """
    question_index = data["index"]
    language = data["language"]
    image_url = ""
    if "image" in data[language][question_index].keys():
        image_url = data[language][question_index]["image"]
    # image style (size, padding etc.) may be given as "image_style" in the json, if not use default
    default_style = {"width": "60%", "margin-top": "30px", "border-radius": "15px"}

    if "image_style" not in data[language][question_index].keys():
        style = default_style
    else:
        style = data[language][question_index]["image_style"]
    if image_url:
        img = dbc.CardImg(src=get_asset_url(image_url), top=True, style=style)
        image_description = data[language][question_index]["image_source_text"]
        img = [img, html.P(image_description)]
        # make image div visible
        show_image_style = {"display": "block"}
    else:
        img = None
        # hide image div to avoid unnecessary padding when there is no image
        show_image_style = {"display": "None"}
    return img, show_image_style


# on page load, update the description text
@callback(Output('description_text', 'children'),
          Output('submit_button', 'children'),
          Input('url_question', 'pathname'),
          State('global_store', 'data'))
def load_description_text(pathname, data):
    """
    On page load, update the description text (info text before the question). Also updated the text on the submit
    button with the correct language.

    parameters:
    - pathname (str): url.pathname, current location (not used, only to trigger the callback when the page loads)
    - data (dict): global_store.data, global memory

    return values:
    - (str): description_text.children, description text
    - (str): submit_button.children, text on the submit button
    """
    language = data["language"]
    if language == "Deutsch":
        button_text = "Abschicken"
    elif language == "English":
        button_text = "Submit"
    else:
        button_text = ""
    question_index = data["index"]
    description_text = data[language][question_index]["description_text"]
    return description_text, button_text


@callback(Output('question_text', 'children'),
          Input('url_question', 'pathname'),
          State('global_store', 'data'))
def load_question_text(pathname, data):
    """
    On page load, update the question text.

    parameters:
    - pathname (str): url.pathname, current location (not used, only to trigger the callback when the page loads)
    - data (dict): global_store.data, global memory

    return value:
    - (str): question_text.children, the question
    """
    language = data["language"]
    question_index = data["index"]
    question_text = data[language][question_index]["question_text"]
    return question_text


@callback(Output('radio_input', 'options'),
          Input('url_question', 'pathname'),
          State('global_store', 'data'))
def load_options(pathname, data):
    """
    On page load, update the answer options.

    parameters:
    - pathname (str): url.pathname, current location (not used, only to trigger the callback when the page loads)
    - data (dict): global_store.data, global memory

    return value.
    - list: list with either the option names as str or dicts of the answer option images as labels and their text descriptions as values
    """
    language = data["language"]
    question_index = data["index"]
    current_question = data[language][question_index]
    text_options = data[language][question_index]["options"]
    style = {"height": "170px"}
    # check if there are images
    if "option_images" in current_question.keys() and len(current_question["option_images"]) == len(text_options):
        img_options = [html.Img(src=get_asset_url(x), style=style) for x in current_question["option_images"]]
        labels = [html.P([img_options[i], html.P(text_options[i])]) for i in range(len(text_options))]
        options = [{"label": labels[i], "value": text_options[i]} for i in range(len(text_options))]
    else:
        options = text_options
    return options


@callback(Output('global_store', 'data', allow_duplicate=True),
          Input('radio_input', 'value'),
          State('global_store', 'data'),
          prevent_initial_call=True)
def update_store(radio_value, data):
    """
    When the radio input changes, remember the user's answer.

    parameters:
    - radio_value (str): radio_input.value, the option that the user has just chosen
    - data (dict): global_store.data, global memory

    return value
    - (dict): global memory containing the user's choice
    """
    language = data["language"]
    question_index = data["index"]
    options = data[language][question_index]["options"]
    for i, option in enumerate(options):
        if radio_value == option:
            data["user_choice"][question_index] = i
            break
    return data
