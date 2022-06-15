# Dash libs
from dash import Dash, callback_context
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

# Latitudes centralizadas
CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474

# Import datasets
estados = pd.read_csv("dataset/dados_estaduais_covid_19.csv")
brasil = pd.read_csv("dataset/dados_brasil_covid_19.csv")

# Import json
mapa_br = json.load(open("dataset/brazil_geo.json", "r"))

# ***********************Intancia Dash**********************************
# Instaciando aplicacao
app = Dash("Dashboard Covid19", external_stylesheets=[dbc.themes.SLATE])

# Setando um dia especifico para coletar os dados
estados_ = estados[estados['data'] == '2022-06-13']
# Setando um Estado especifico
df_estado = estados[estados["estado"] == "PE"]
# Colunas para serem utilizadas no Dropdow
select_columns = {
    "casosAcumulado": "Casos Acumulados",
    "casosNovos": "Novos Casos",
    "obitosAcumulado": "Óbitos Totais",
    "obitosNovos": "Óbitos por dia"
}

# Contruindo a figura do grafico (MAPA)
fig = px.choropleth_mapbox(estados_, locations="estado", color="casosNovos", zoom=4,
                           geojson=mapa_br, color_continuous_scale="Redor", opacity=0.4,
                           center={"lat": -16.96, "lon": -47.79},
                           hover_data={"casosAcumulado": True,
                                       "casosNovos": True,
                                       "obitosNovos": True,
                                       "estado": True})

fig.update_layout(
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.layout.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
)

# Construindo o segundo Grafico (Casos x Dia x Estado)
fig2 = go.Figure(layout={"template": "plotly_dark"})
fig2.add_trace(go.Scatter(x=df_estado['data'], y=df_estado["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
)


# ***********************Layout Dash**********************************
# Layout da aplicacao
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            # Div para os componentes laterais do grafico
            html.Div([
                html.Img(id="logo", src=app.get_asset_url(
                    "logo_topo.png"), height=50),             # Foto logo
                html.H5("Evolução dos Casos de Covid-19"),    # Titulo pequeno
                dbc.Button("BRASIL", color="info",            # Botao
                           id="location-button", size="lg")
            ], style={}),
            html.P("Digite a data para resumir as informações.",  # Paragrafo
                   style={"margin-top": "40px"}),
            html.Div(
                id="div-test",
                children=[
                    dcc.DatePickerSingle(
                        id="date-picker",
                        min_date_allowed=brasil["data"].min(),
                        max_date_allowed=brasil["data"].max(),
                        initial_visible_month=brasil["data"].min(),
                        date=brasil["data"].max(),
                        display_format="MMMM D, YYYY",
                        style={"border": "0px solid black"}
                    )
                ]),
            # Criando uma nova linha para compor os  3 cards
            dbc.Row([
                # Col 1
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Recuperados"),
                            html.H3(style={"color": "#adfc92"},
                                    id="recuperados-text"),
                            html.Span("Em acompanhamento"),
                            html.H5(id="acompanhamento-text"),
                        ])
                    ], color="#242424", outline=True,
                             style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.25), 0 4px 20px 0 rgba(0, 0, 0, 0.29)",
                                    "color": "#FFFFFF"})
                ], md=4),
                # Col 2
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Casos confirmados"),
                            html.H3(style={"color": "#389fd6"},
                                    id="confirmados-text"),
                            html.Span("Novos casos na data"),
                            html.H5(id="novos-casos-text"),
                        ])
                    ], color="#242424", outline=True,
                             style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.25), 0 4px 20px 0 rgba(0, 0, 0, 0.29)",
                                    "color": "#FFFFFF"})
                ], md=4),
                # Col 3
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span("Óbitos confirmados"),
                            html.H3(style={"color": "#DF2935"},
                                    id="obitos-text"),
                            html.Span("Óbitos na data"),
                            html.H5(id="obitos-na-data-text"),
                        ])
                    ], color="#242424", outline=True,
                             style={"margin-top": "10px",
                                    "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.25), 0 4px 20px 0 rgba(0, 0, 0, 0.29)",
                                    "color": "#FFFFFF"})
                ], md=4),
            ]),

            # Div par organizar o DropDown
            html.Div([
                html.P("Selecione qual série de dados deseja visualizar:"),
                dcc.Dropdown(
                    id="location-dropdown",
                    options=[{"label": j, "value": i}
                             for i, j in select_columns.items()],
                    value="casosNovos",
                    style={"margin-top": "10px"}
                ),
                # Graph 1
                dcc.Graph(
                    id="line-graph",
                    figure=fig2,
                    config={'displayModeBar': False}
                )
            ]),
        ], md=5, style={"padding": "25px", "background-color": "#242424"}),
        dbc.Col([
            dcc.Loading(
                id="loading-1",
                type="default",
                children=[
                    dcc.Graph(
                     id="brasil_map",
                     figure=fig,
                     config={'displayModeBar': False},
                     style={"height": "100vh", "margin-right": "10px"}
                    )
                ]
            )
        ], md=7)
    ], class_name='g-0'), fluid=True
)

# *************************Deixando o Dash Interativo**************************************

# interatividade lidando como picker-date,


@app.callback(
    [
        Output("recuperados-text", "children"),
        Output("acompanhamento-text", "children"),
        Output("confirmados-text", "children"),
        Output("novos-casos-text", "children"),
        Output("obitos-text", "children"),
        Output("obitos-na-data-text", "children")
    ],
    [Input("date-picker", "date"), Input("location-button", "children")]
)
def display_status(date, location):
    if location == "BRASIL":
        df_data_on_date = brasil[brasil["data"] == date]
    else:
        df_data_on_date = estados[(estados["estado"] == location) & (
            estados['data'] == date)]

    recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna(
    ).values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".")
    acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna(
    ).values[0] else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",", ".")
    casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna(
    ).values[0] else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".")
    casos_novos = "-" if df_data_on_date["casosNovos"].isna(
    ).values[0] else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",", ".")
    obitos_acumulado = "-" if df_data_on_date["obitosAcumulado"].isna(
    ).values[0] else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".")
    obitos_novos = "-" if df_data_on_date["obitosNovos"].isna(
    ).values[0] else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",", ".")
    return (
        recuperados_novos,
        acompanhamentos_novos,
        casos_acumulados,
        casos_novos,
        obitos_acumulado,
        obitos_novos,
    )

# Interatividade lidando com o grafico line-graph


@app.callback(
    Output("line-graph", "figure"),
    [
        Input("location-dropdown", "value"),
        Input("location-button", "children")
    ]
)
def plot_line_graph(plot_type, location):
    if location == "BRASIL":
        df_data_on_location = brasil.copy()
    else:
        df_data_on_location = estados[estados["estado"] == location]

    bar_plots = ["casosNovos", "obitosNovos"]

    fig2 = go.Figure(layout={"template": "plotly_dark"})
    if plot_type in bar_plots:
        fig2.add_trace(
            go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(
            x=df_data_on_location["data"], y=df_data_on_location[plot_type]))

    fig2.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
    )
    return fig2

# Mais interatividade


@app.callback(
    Output("brasil_map", "figure"),
    [Input("date-picker", "date")]
)
def update_map(date):
    df_data_on_states = estados[estados["data"] == date]

    fig = px.choropleth_mapbox(df_data_on_states, locations="estado", geojson=mapa_br,
                               # https://www.google.com/maps/ -> right click -> get lat/lon
                               center={"lat": CENTER_LAT, "lon": CENTER_LON},
                               zoom=4, color="casosAcumulado", color_continuous_scale="Redor", opacity=0.55,
                               hover_data={"casosAcumulado": True, "casosNovos": True,
                                           "obitosNovos": True, "estado": False}
                               )

    fig.update_layout(paper_bgcolor="#242424", mapbox_style="carto-darkmatter", autosize=True,
                      margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    return fig


@app.callback(
    Output("location-button", "children"),
    [Input("brasil_map", "clickData"),
     Input("location-button", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if click_data is not None and changed_id != "location-button.n_clicks":
        state = click_data["points"][0]["location"]
        return "{}".format(state)

    else:
        return "BRASIL"


if __name__ == "__main__":
    app.run_server(debug=False)
