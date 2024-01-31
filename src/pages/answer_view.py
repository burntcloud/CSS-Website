from dash import html, register_page, dcc, callback, Input, Output, State, get_asset_url
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

register_page(__name__, path="/answer")

# Blueprint for the answer view layout, needs ids "header", "image", "description_text", "question_text" and "submit_button"
answer_layout = html.Div(
    children=[
        dbc.Container([
            dbc.Card([html.Center(
                html.Div(id="answer_image")),
                dbc.CardBody([
                    html.P(id="answer_text", style={'font-size': '24px'}),
                    # html.Div(id="answer_image"),
                    # dcc.Link(dbc.Button("Next", id='next_button',
                    #                    style={"margin-top": "30px", "fontSize": "20px", "background-color": "#348994",
                    #                          "border": "none"}), id="next_button_link", href="/question",
                    #         refresh=True),
                    dbc.Button("Next", id='next_button',
                               style={"margin-top": "30px", "fontSize": "20px", "background-color": "#348994",
                                      "border": "none"})
                ])
            ])],
        )
    ],
    id="answer_layout"
)

layout = html.Div(children=[
    dcc.Location(id='url_answer', refresh=False),
    answer_layout,
])


# on page load, insert or delete the answer's image and if necessary adapt size
@callback(Output('answer_image', 'children'),
          Output('answer_image', 'style'),
          Input('url_answer', 'pathname'),
          State('global_store', 'data'))
def load_image(pathname, data):
    language = data["language"]
    question_index = data["index"]
    answer_image_url = ""
    if "answer_image" in data[language][question_index].keys():
        answer_image_url = data[language][question_index]["answer_image"]
    # image style (size, padding etc.) may be given as "image_style" in the json, if not use default
    default_style = {"width": "70%", "margin-top": "30px", "border-radius": "15px"}
    if "answer_image_style" not in data[language][question_index].keys():
        style = default_style
    else:
        style = data[language][question_index]["answer_image_style"]
    if answer_image_url:
        img = dbc.CardImg(src=get_asset_url(answer_image_url), top=True, style=style)
        image_description = data[language][question_index]["answer_image_source_text"]
        img = [img, html.P(image_description)]
        # make image div visible
        show_image_style = {"display": "block"}
    else:
        img = None
        # hide image div to avoid unnecessary padding when there is no image
        show_image_style = {"display": "None"}
    return img, show_image_style


# on page load, load the answer text
@callback(Output('answer_text', 'children'),
          Output('next_button', 'children'),
          Input('url_answer', 'pathname'),
          State('global_store', 'data'))
def load_answer(pathname, data):
    language = data["language"]

    # find current question index, load the corresponding answer text, increase question index
    question_index = data["index"]
    answer = data[language][question_index]["answer_text"]
    if str(question_index) in data["user_choice"].keys():
        user_choice_index = data["user_choice"][str(question_index)]
        user_choice = data[language][question_index]["options"][user_choice_index]
    else:
        user_choice = ""
    if '$' in answer:
        answer = answer.replace('$', user_choice)
    if language == "Deutsch":
        button_text = "Nächste Frage"
        your_answer = html.P(html.B("Angegebene Antwort: " + user_choice))
    elif language == "English":
        button_text = "Next"
        your_answer = html.P(html.B("Your answer: " + user_choice))

    answer_list = [your_answer]
    for paragraph in answer:
        answer_list.append(html.P(paragraph))
    return answer_list, button_text


# When the next button is pressed, update the global store index
@callback(Output('global_store', 'data', allow_duplicate=True),
          Output('url', "href"),
          Input("next_button", "n_clicks"),
          State("global_store", "data"),
          prevent_initial_call=True)
def increase_question_index(n_clicks, data):
    if not n_clicks:
        raise PreventUpdate
    data["index"] += 1
    n_questions = len(data[data["language"]])
    redirect = "/question"
    if data["index"] >= n_questions:
        data["index"] = 0
        redirect = "/success"
        data["user_choice"] = {}
    return data, redirect
