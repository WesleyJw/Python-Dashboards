from distutils.log import debug
from dash import Dash
from dash.html import Div, H1, H2, H3, P
from dash.dcc import Graph

# Instaciando aplicacao
app = Dash("Dashboard Covid19")

# Layout da aplicacao
app.layout = Div(
    H1("Covid 19: Brasil")

)

app.run_server(debug=True)
