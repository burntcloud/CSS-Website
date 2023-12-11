import dash
from dash import Dash, html, callback, State, Output, Input
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.SOLAR], use_pages=True)

# load layout of home page
app.layout = html.Div(children=[
    dash.page_container
])


@callback(Output('card', 'children'),
          Input('submit-button-state', 'n_clicks'),
          State('radio-input', 'value'),
          State('card', 'children'))
def show_answer(n_clicks, radio_input, children):
    if n_clicks is None:
        raise PreventUpdate
    children[-1] = html.Div([f'Ich mag auch supergerne {radio_input}', html.Button(children="Next", id="next")])
    return children


if __name__ == '__main__':
    app.run(debug=True)
