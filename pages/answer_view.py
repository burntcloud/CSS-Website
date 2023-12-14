from dash import html, register_page, dcc, callback, Input, Output, State

register_page(__name__, path="/answer")

layout = html.Div(children=[
    dcc.Location(id='url_answer', refresh=False),
    html.H1(
        children="Test answer view",
        style={'textAlign': 'center', 'color': '#AAABBB'}),
    html.P(id="answer_text"),
    dcc.Link(html.Button("Next", id='next_button'), id="next_button_link", href="/question", refresh=True),
])


# When page is loaded, choose correct answer text, update the question index in the global store
# and if you run out of questions, let the next button redirect to home
# any '$' in the answer text is replaced by the user's answer
@callback(Output('answer_text', 'children'),
          Output('global_store', 'data'),
          Output('next_button_link', 'href'),
          Input('url_answer', 'pathname'),
          State('global_store', 'data'))
def load_answer(pathname, data):
    # find current question index, load the corresponding answer text, increase question index
    question_index = data["index"]
    answer = data["Questions"][question_index]["answer_text"]
    if '$' in answer:
        user_choice = data["user_choice"]
        answer = answer.replace('$', user_choice)
    data["index"] += 1
    if data["index"] >= len(data["Questions"]):
        data["index"] = 0
        return answer, data, "/"
    return answer, data, "/question"
