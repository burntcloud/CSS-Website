from dash import html, register_page, dcc, callback, Input, Output, State, get_asset_url
import dash_bootstrap_components as dbc

register_page(__name__, path="/answer")

# Blueprint for the answer view layout, needs ids "header", "image", "description_text", "question_text" and "submit_button"
answer_layout = html.Div(
    children=[
        dbc.Container([
            html.H1(children="Answer View", style={"text-align": "center"}),
            dbc.Card([html.Center(
                html.Div(id="answer_image")),
                dbc.CardBody([
                    html.P(id="answer_text",style={'font-size': '20px'}),
                    #html.Div(id="answer_image"),
                    dcc.Link(dbc.Button("Next", id='next_button',style={"margin-top": "30px", "fontSize": "20px","background-color": "#348994", "border": "none"}), id="next_button_link", href="/question", refresh=True)
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
        # make image div visible
        show_image_style = {"display": "block"}
    else:
        img = None
        # hide image div to avoid unnecessary padding when there is no image
        show_image_style = {"display": "None"}
    return img, show_image_style


# on page load, load the answer text
@callback(Output('answer_text', 'children'),
          Input('url_answer', 'pathname'),
          State('global_store', 'data'))
def load_answer(pathname, data):
    language = data["language"]
    # find current question index, load the corresponding answer text, increase question index
    question_index = data["index"]
    answer = data[language][question_index]["answer_text"]
    if '$' in answer:
        user_choice = data["user_choice"]
        answer = answer.replace('$', user_choice)
    your_answer = html.P(html.B("Your answer: " + data["user_choice"]))
    answer = html.P([your_answer, answer])
    return answer


# When page is loaded, update the question index in the global store
# and if you run out of questions, let the next button redirect to home
@callback(Output('global_store', 'data'),
          Output('next_button_link', 'href'),
          Input('url_answer', 'pathname'),
          State('global_store', 'data'))
def load_answer(pathname, data):
    language = data["language"]
    # find current question index, load the corresponding answer text, increase question index
    question_index = data["index"]
    data["index"] += 1
    if data["index"] >= len(data[language]):
        data["index"] = 0
        return data, "/"
    return data, "/question"
