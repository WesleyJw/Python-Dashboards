from dash import Dash
from dash import html, dcc

# Instaciando aplicacao
app = Dash("Dashboard Covid19")

# Layout da aplicacao
app.layout = html.Div(
    html.H1("Covid 19: Brasil")

)

app.run_server(debug=True)
