from dash import dcc, html, register_page, callback, State, Output, Input, get_asset_url
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

register_page(__name__, path="/question")

# blueprint for the answer options, styled as radio buttons
answer_options = dbc.Container(dbc.RadioItems(
    options=[],
    value="",
    id='radio_input',
    className="btn-group",  # all in one line
    inputClassName="btn-check",  # remove circles
    labelClassName="btn btn-outline-primary",  # make options look like buttons
), style={"padding-left": "0px"}, className="radio-group")

# blueprint for the question view layout, needs ids "header", "image", "description_text", "question_text" and "submit_button"
question_layout = html.Div(
    children=[
        dbc.Container([
            html.H1(children="", id="header", style={"text-align": "center"}),
            dbc.Card([html.Center(
                html.Div(id="image")),
                dbc.CardBody([
                    html.P(id="description_text", className="card-text"),
                    html.H4(id="question_text"),
                    answer_options,
                    dcc.Link(dbc.Button(id='submit_button', children="Submit", style={"margin-top": "30px"}), href="/answer", refresh=True)
                ])
            ])],
            )
    ],
    id="question_layout"
)

layout = html.Div(children=[
    dcc.Location(id='url_question', refresh=False),
    question_layout,
])


# on page load, update the number in the header
@callback(Output('header', 'children'),
          Input('url_question', 'pathname'),
          State('global_store', 'data'))
def load_header(pathname, data):
    question_index = data["index"]
    return "Question " + str(data["Questions"][question_index]["id"])


# on page load, insert or delete the question's image and if necessary adapt size
@callback(Output('image', 'children'),
          Output('image', 'style'),
          Input('url_question', 'pathname'),
          State('global_store', 'data'))
def load_image(pathname, data):
    question_index = data["index"]
    image_url = ""
    if "image" in data["Questions"][question_index].keys():
        image_url = data["Questions"][question_index]["image"]
    # image style (size, padding etc.) may be given as "image_style" in the json, if not use default
    default_style = {"width": "60%", "margin-top": "30px", "border-radius": "15px"}
    if "image_style" not in data["Questions"][question_index].keys():
        style = default_style
    else:
        style = data["Questions"][question_index]["image_style"]
    if image_url:
        img = dbc.CardImg(src=get_asset_url(image_url), top=True, style=style)
        # make image div visible
        show_image_style = {"display": "block"}
    else:
        img = None
        # hide image div to avoid unnecessary padding when there is no image
        show_image_style = {"display": "None"}
    return img, show_image_style


# on page load, update the description text
@callback(Output('description_text', 'children'),
          Input('url_question', 'pathname'),
          State('global_store', 'data'))
def load_description_text(pathname, data):
    question_index = data["index"]
    description_text = data["Questions"][question_index]["description_text"]
    return description_text


# on page load, update the question text
@callback(Output('question_text', 'children'),
          Input('url_question', 'pathname'),
          State('global_store', 'data'))
def load_question_text(pathname, data):
    question_index = data["index"]
    question_text = data["Questions"][question_index]["question_text"]
    return question_text


# on page load, update the answer options
@callback(Output('radio_input', 'options'),
          Input('url_question', 'pathname'),
          State('global_store', 'data'))
def load_options(pathname, data):
    question_index = data["index"]
    current_question = data["Questions"][question_index]
    text_options = data["Questions"][question_index]["options"]
    style = {"height": "170px"}
    # check if there are images
    # TODO: make buttons with image and text
    # TODO: Layout is messed up for mobile
    if "option_images" in current_question.keys() and len(current_question["option_images"]) == len(text_options):
        img_options = [html.Img(src=get_asset_url(x), style=style) for x in current_question["option_images"]]
        options = [{"label": img_options[i], "value": text_options[i]} for i in range(len(text_options))]
    else:
        options = text_options
    return options


# When the radio input changes, remember the user's answer
@callback(Output('global_store', 'data', allow_duplicate=True),
          Input('radio_input', 'value'),
          State('global_store', 'data'),
          prevent_initial_call=True)
def update_store(radio_value, data):
    data["user_choice"] = radio_value
    return data
