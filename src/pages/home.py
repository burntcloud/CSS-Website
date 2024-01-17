from dash import dcc, html, register_page, callback, State, Output, Input, get_asset_url
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

register_page(__name__, path="/")

lang_buttons = dbc.RadioItems(
    className="btn-group",
    inputClassName="btn-check",
    labelClassName="btn btn-outline-primary",
    options=[{"label": "Deutsch", "value": 1},
             {"label": "English", "value": 2}],
    value=1,
    style={"float": "right"}
)

layout = html.Div(
    children=[
        dbc.Container([
            dbc.Row(
                [dbc.Col(html.H1("CSS Quizpage", style={'font-size': '70px'})),
                 dbc.Col(lang_buttons)

                 ]
            ),
            dbc.Row(
                html.Img(src=get_asset_url('NS_Doku_Logo.png'), style={'width': '20%'})),
            dbc.Row(
                dbc.Card([
                    dbc.CardBody([
                        html.H2("Welcome to the Quiz!"),
                        # html.P("The framing of the quiz:",style={'font-size':'25px'}),
                        html.P("During National Socialism, especially during the Second World War, \
                           numerous people from the annexed territories were deported to the then \
                           German Reich for forced labor. The historian Ulrich Herbert described \
                           this as the \"most violently organized deportation operation of all time.\" \
                           Exploitation was omnipresent, \"without exception, everyone who experienced the \
                           war in Germany as a young person or adult had some form of contact with the \
                           foreign workers and prisoners of war.\" Despite the immediate proximity and \
                           the enormous number of people affected, the crime was almost completely suppressed \
                           after the end of the war. Responsibility was systematically concealed and compensation \
                           claims ignored for decades. It was not until the 1980s that a public debate began, \
                           which ultimately led to the establishment of the Foundation \"Remembrance, \
                           Responsibility and Future\" in 2000. Only then did minimal compensation begin \
                           to be provided to former forced laborers and their relatives. The historical \
                           sites of forced labor, such as the RAW here in Neuaubing, are important \
                           reminders of the crime today.", style={'font-size': '20px'}),
                        html.P("This quiz serves to remind of the crime of forced labor and \
                                  to educate about the circumstances and living conditions of the \
                                  people. Please bear in mind that these questions are based on \
                                  historical facts and refer to the reality of many people's suffering \
                                  and hardship during this time. The quiz is not intended to test your \
                                  prior knowledge, but to help raise awareness of the historical \
                                  reality.", style={'font-size': '20px'})
                    ])
                ])),
            dbc.Row(
                dcc.Link(
                    dbc.Button("Start Quiz",
                               style={'font-size': '20px', "background-color": "#348994", "border": "none"}),
                    href="/question", refresh=True))
        ])
    ]
)
