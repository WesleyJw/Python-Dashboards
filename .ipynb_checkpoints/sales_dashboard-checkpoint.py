#%%
# INTRODUÇÃO AO DASH

import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# https://www.kaggle.com/kyanyoga/sample-sales-data
df = pd.read_csv('sales_data_sample.csv',encoding = 'latin-1')
df.head()
# %%
# global_df = df[df['COUNTRY'] == 'Spain']
global_df = df.copy()



# %%
global_df['Data_Pedido'] = pd.to_datetime(global_df['ORDERDATE'])
global_df['Ano'] = global_df['Data_Pedido'].dt.year
global_df['Mes'] = global_df['Data_Pedido'].dt.month_name()

# %%
global_df.isnull().sum()

# %%
drop_cols  = ['ADDRESSLINE1', 'ADDRESSLINE2', 'POSTALCODE', 'TERRITORY', 'PHONE', 'CONTACTFIRSTNAME', 'CONTACTLASTNAME', 'CUSTOMERNAME', 'ORDERNUMBER']
global_df = global_df.drop(drop_cols, axis = 1)
# global_df = global_df.groupby('STATE').count()
# global_df.head()
# %%
global_df.isnull().sum()

global_pais_ano_status_df = global_df.groupby(['COUNTRY','Ano','STATUS'])[['SALES']].mean()
global_pais_ano_status_df.reset_index(inplace=True)    

# %%
global_pais_ano_status_PRODUCTLINE_df = global_df.groupby(['COUNTRY','Ano','STATUS', 'PRODUCTLINE', 'DEALSIZE'])[['SALES']].mean()
global_pais_ano_status_PRODUCTLINE_df.reset_index(inplace=True)    

sales_data_df = global_df.groupby(['COUNTRY','Data_Pedido', 'DEALSIZE'])[['SALES']].mean()
sales_data_df.reset_index(inplace=True)    

df = global_pais_ano_status_PRODUCTLINE_df.copy()

colors = {
    'background': '#1e434a',
    'text': '#7FDBFF'
}
# %%


#https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.SOLAR],
                                        # Para responsibilidade para mobile layout
                                        meta_tags=[
                                                    {'name': 'viewport',
                                                    'content': 'width=device-width, initial-scale=1.0'}
                                                    ]
                                        
                                                  )
# dbc.Container é como se fosse um DIV porém facilita qnd tiver usando bootstrap 
app.layout = dbc.Container([
    # 1 Row para tituli
    # 1 row para dropdown +  os primeiros grafico
    # 1 Row para o checkbox +  os outros  grafico

    dbc.Row([
        # VERIFICAR NO CSS CHEAT SHEET TXT CENTER
        dbc.Col( html.H1('Dashboard de Vendas',                     # text-primary add cor azul no texto
                    className = 'text-center text-primary, display-2 shadow' , ),  # mb-4 cria espaço entre a row do titulo e a row abaixo,
                        width = 10 )  ,                             # representa o numero de colunas  que posso usar no texto               
        dbc.Col([

                dbc.Card(
                    [
                        dbc.CardImg(
                            src="assets/Robô-Minerador_metade-final_fundo-preto.jpg", 
                            top = True,
                            bottom=False),

                        dbc.CardBody(
                            html.P("Minerando dados!",
                                className="card text-white bg-primary text-center")
                        ),
                        
                         dbc.CardLink('Minerando Dados Youtube webPage', href = 'https://www.youtube.com/channel/UCZ8gRCp3vixlGVAtplCDd5Q',
                                                    target = '_blank', className = 'text-center' ),
                    ],
                    style={"width": "17rem"},
                                
                )

            ], width = {'size':2, 'order':2 })
    ]),
     
    # dbc.Row([
    #     dbc.Col([

    #         dcc.Dropdown(id = 'dropdown-1',
    #                             multi = False,
    #                             value = 'Classic Cars',
    #                             options = [
    #                                 {'label': x , 'value': x}
    #                                 for x in df['PRODUCTLINE'].unique()
    #                                ] ),

    #         dcc.Graph(id = 'bar-fig', figure = {})
    #     ], width = {'size':4, 'order':1 }),

    #     dbc.Col([

    #         dcc.Dropdown(id = 'dropdown-2',
    #                     multi = True,
    #                     value = ['USA'],
    #                     options = [
    #                         {'label': x , 'value': x}
    #                         for x in sales_data_df['COUNTRY'].unique()
    #                         ] ),

    #         dcc.Graph(id = 'line-fig2', figure = {})    

    #         ],width = {'size':4, 'order':2 }),

            
    #     dbc.Col([

    #         dcc.Dropdown(id="pie-dropdown",
    #                 options=[
    #                     {"label": "STATUS", "value": 'STATUS'},
    #                     {"label": "COUNTRY", "value": 'COUNTRY'},
    #                     {"label": "DEALSIZE", "value": 'DEALSIZE'},
    #                     {"label": "ANO", "value": 'Ano'}],
    #                 multi=False,
    #                 value='Ano',
    #                 style={'width': "60%"}, className="text-center"
    #                 ), 

    #         dcc.Graph(id = 'pie-chart', figure = {})    

    #         ], width = {'size':4, 'order':3 }),

    # ]),

    # dbc.Row([

    #     dbc.Col([
    #         html.P('Escolha o tamanho do produto',
    #         style = { 'textDecoration': 'underline'}),
    #         dcc.Checklist(id = 'minha-ckecklist', value = ['Small'],
    #         options = [     {'label': x , 'value': x}
    #                         for x in sales_data_df['DEALSIZE'].unique() 
    #                  ],
    #         labelClassName='mr-3 text-secondary'),

        
    #     dcc.Graph(id = 'histograma', figure = {})

    #     ], width = {'size':6, 'order':2 }),

    #     dbc.Col([
          
    #     html.H1(id = 'output_title', children = [], style={'text-align': 'center'}  ),

    #     dcc.Dropdown(id="ano_selecionado",
    #                 options=[
    #                     {"label": "Ano: 2003", "value": 2003},
    #                     {"label": "Ano: 2004", "value": 2004},
    #                     {"label": "Ano: 2005", "value": 2005}],
    #                 multi=False,
    #                 value=2003,
    #                 style={'width': "60%"},className="text-center"
    #                 ), 

    #     dcc.Graph(id='mapa_de_vendas', figure={})


    #     ], width = {'size':6, 'order':3 })
    # ], align="center")  # Vertical: start, center, end),



],fluid = True)


# Line chart - Single
# @app.callback(
#     Output('bar-fig', 'figure'),
#     Input('dropdown-1', 'value')
# )
# def update_graph(produto_selecionado):
#     dff = df[df['PRODUCTLINE']==produto_selecionado]
#     figln = px.bar(dff, x='SALES', y='COUNTRY', 
#                     orientation = 'h',
#                     color_discrete_sequence = ['#33a5ee'])

#     figln.update_xaxes(showgrid=False)
#     figln.update_yaxes(showgrid=False)

    
#     figln.update_layout(
#         plot_bgcolor=colors['background'],
#         paper_bgcolor=colors['background'],
#         font_color=colors['text']
#                         )   
#     return figln


# # Line chart - multiple
# @app.callback(
#     Output('line-fig2', 'figure'),
#     Input('dropdown-2', 'value')
# )
# def update_graph(ano_selecionado):
#     dff = sales_data_df[sales_data_df['COUNTRY'].isin(ano_selecionado)]
#     figln2 = px.line(dff, x='Data_Pedido', y='SALES', color='COUNTRY',
#                          color_discrete_sequence = ['#33a5ee'])

#     figln2.update_xaxes(showgrid=False)
#     figln2.update_yaxes(gridcolor = '#839496')

#     figln2.update_layout(
#         plot_bgcolor=colors['background'],
#         paper_bgcolor=colors['background'],
#         font_color=colors['text']
#                         )                          
#     return figln2

# # Pie chart - multiple
# @app.callback(
#     Output('pie-chart', 'figure'),
#     Input('pie-dropdown', 'value')
# )
# def muda_piechart(ano_selecionado):
#     pie_chart = px.pie(global_df, names = ano_selecionado, hole =.3)
#                         #  color_discrete_sequence = ['#33a5ee'])

#     pie_chart.update_xaxes(showgrid=False)
#     pie_chart.update_yaxes(gridcolor = '#839496')

#     pie_chart.update_layout(
#         plot_bgcolor=colors['background'],
#         paper_bgcolor=colors['background'],
#         font_color=colors['text']
#                         )                          
#     return pie_chart

# # Histogram
# @app.callback(
#     Output('histograma', 'figure'),
#     Input('minha-ckecklist', 'value')
# )
# def update_graph(tamanho_selecionado):
#     dff = global_df[global_df['DEALSIZE'].isin(tamanho_selecionado)]
#     # dff = sales_data_df[sales_data_df['Data_Pedido']=='2005-05-06']
#     # dff = global_df.groupby('COUNTRY').mean()
#     fighist = px.histogram(dff, x='COUNTRY', y='SALES', 
#                          color_discrete_sequence = ['#33a5ee'])
    
#     fighist.update_xaxes(showgrid=False)
#     fighist.update_yaxes(showgrid=False)
    
#     fighist.update_layout(
#         plot_bgcolor=colors['background'],
#         paper_bgcolor=colors['background'],
#         font_color=colors['text']
#                         )   
#     return fighist




# @app.callback(
#     # [Output(component_id='output_container', component_property='children'),
#     [Output(component_id='output_title', component_property='children'),
#     Output(component_id='mapa_de_vendas', component_property='figure')],
#     [Input(component_id='ano_selecionado', component_property='value')]
# )
# def update_graph(ano_selecionado):

#     title = "Mapa de Vendas nos EUA no ano de {}".format(ano_selecionado)

#     df_ = global_df.copy()
#     df_ = df_[df_['COUNTRY']== 'USA']
#     df_ = df_[df_["Ano"] == ano_selecionado]
#     df_ = df_[df_["STATUS"] == "Shipped"]

#     # # Plotly Express
#     fig = px.choropleth(
#         data_frame=df_,
#         locationmode= 'USA-states',
#         locations= 'STATE',
#         scope="usa",
#         color='SALES',
#         hover_data = ['STATE', 'SALES'],
#         color_continuous_scale=px.colors.sequential.YlOrRd,
#         template='plotly_dark'
        
#     )

#     fig.update_layout(
#         plot_bgcolor=colors['background'],
#         paper_bgcolor=colors['background'],
#         font_color=colors['text']
#                         )  

#     return  title, fig  

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)


# %%
