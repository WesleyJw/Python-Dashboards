# Dash libs
from dash import Dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Graph libs
import plotly.express as px
import plotly.graph_objects as go

# Statistics libs
import numpy as np
import pandas as pd
import json

# Import datasets
estados = pd.read_csv("dataset/dados_estaduais_covid_19.csv")
brasil = pd.read_csv("dataset/dados_brasil_covid_19.csv")

# Import json
mapa_br = json.load(open("dataset/brazil_geo.json", "r"))

# ***********************Intancia Dash**********************************
# Instaciando aplicacao
app = Dash("Dashboard Covid19", external_stylesheets=[dbc.themes.CYBORG])

# Setando um dia especifico para coletar os dados
estados_ = estados[estados['data'] == '2022-06-13']

# Contruindo a figura do grafico
fig = px.choropleth_mapbox(estados_, locations="estado", color="casosNovos",
                           geojson=mapa_br, color_continuous_scale="Redor", opacity=0.4,
                           center={"lat": -16.96, "lon": -47.79},
                           hover_data={"casosAcumulado": True,
                                       "casosNovos": True,
                                       "obitosNovos": True,
                                       "estado": True})

fig.update_layout(
    mapbox_style="carto-darkmatter"
)

# ***********************Layout Dash**********************************
# Layout da aplicacao
app.layout = dbc.Container(
    html.H1("Covid 19: Brasil"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="brasil_map",
                figure=fig
            )
        ])
    ])


)

app.run_server(debug=True)
