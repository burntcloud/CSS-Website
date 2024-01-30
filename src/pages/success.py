from dash import dcc, html, register_page, callback, State, Output, Input, get_asset_url
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import random

register_page(__name__, path="/success")

data = [['Sowjetunion', 10, 'BLR'], ['Polen', 8, 'POL'], ['Italien', 7, 'ITA'], ['Niederlande', 6, 'NLD'], ['Jugoslawien', 5, 'SRB'], ['Tschechoslowakei', 1, 'CZE'], ['Ungarn', 1, 'HUN'], ['Belgien', 1, 'BEL']]
df = pd.DataFrame(data, columns=['Country', 'Size', 'ISO3'])

fig = px.scatter_geo(df, locations="ISO3", color="Size",
                     hover_name="Country", size="Size",
                     hover_data={'Size': False, 'ISO3': False},
                     projection="natural earth", fitbounds="locations")
fig.update_geos(showocean=True, oceancolor="#1F434A")

fig.update_layout(height=300, margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor="#1F434A", paper_bgcolor="#1F434A")
fig.update_layout(showlegend=False)

layout = html.Div(
    children=[
        dcc.Location(id='success', refresh=False),
        dbc.Container([
            dbc.Row(
                # html.Img(src=get_asset_url('NS_Doku_Logo.png'), style={'width': '20%'})
            ),
            dbc.Row(
                dbc.Card([
                    dbc.CardBody(id="success_text")
                ])),
            dbc.Row(
                dcc.Link(
                    dbc.Button(id="back_button",
                               style={'font-size': '20px', "background-color": "#348994", "border": "none"}),
                    href="/", refresh=True))
        ])
    ]
)


@callback(Output('back_button', "children"),
          Output('success_text', "children"),
          Input("success", "href"),
          State("global_store", "data"))
def update_main_page(pathname, data):
    language = data["language"]
    graph = dcc.Graph(figure=fig)
    mixed = [graph]
    if language == "Deutsch":
        for paragraph in data["Fazit"]:
            mixed.append(html.P(paragraph))
        for link in data["Links"]:
            mixed.append(dbc.Row(html.A(href=link, children=link)))
        return "Zurück", mixed
    else:
        for paragraph in data["Conclusion"]:
            mixed.append(html.P(paragraph))
        for link in data["Links"]:
            mixed.append(dbc.Row(html.A(href=link, children=link)))
        return "Home", mixed
