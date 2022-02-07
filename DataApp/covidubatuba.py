#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
from dash import Dash
from dash.html import Div, P, H3, H5, H6, Img, Span
from dash.dcc import Graph,Dropdown,RadioItems,DatePickerSingle
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# In[2]:


raw = pd.read_csv("webapp_raw.csv")
raw.datetime = pd.to_datetime(raw.datetime)
asf = pd.read_csv("webapp_as_freq.csv")
asf.datetime = pd.to_datetime(asf.datetime)
imp = pd.read_csv("webapp_imputed.csv")
imp.datetime = pd.to_datetime(imp.datetime)

# In[3]:


app = Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])
server = app.server

fig = go.Figure(layout={"template":"plotly_dark"})
fig.add_trace(go.Scatter(x=raw["datetime"], y=raw["positive"]))
fig.update_layout(
    paper_bgcolor="#002b36",
    plot_bgcolor="#002b36",
    autosize=True,
    height=250,
    width=900,
    margin=dict(l=10, r=10, b=10, t=10),
    xaxis = dict(
        tickmode='array', tickvals=['2021-01-01','2021-04-02','2021-07-09','2021-06-03'],
        ticktext=['Ano-Novo','Sexta-Santa','Rev-Const','Corpus-Christi'],
        tickangle=-45,
        gridcolor="#1f5954"
        ),
    yaxis=dict(gridcolor="#1f5954")
    )

app.layout = dbc.Container( className="container",
    children=[
        Div(children=[
            dbc.Row([
                dbc.Col([
                    Img(id="logo", src=app.get_asset_url("bandeira.png"), height=50, 
                    style={"margin-left":"30px","margin-top":"30px"})],xs=1),

                dbc.Col([
                    H3("Covid-19, Ubatuba-SP.", id="titulo")], xs=7,
                    style={"margin-left":"35px","margin-top":"20px"}),

                dbc.Col([
                    RadioItems(
                        id="language",
                        options=[
                            {"label":"Port.","value":"por"},
                            {"label":"Eng.","value":"eng"}
                            ], value="por", style={"margin-top":"45px"},
                            labelStyle={"display":"inline-block","margin-left":"5px"}
                            )
                            ],xs=2)
                            ]),
                    
            dbc.Row([
                dbc.Col([
                    P("Informe uma data:", id="data"),
                    Div(
                        className="div-for-dropdown",
                        id="div-test",
                        children=[
                            DatePickerSingle(
                                id="date-picker",
                                min_date_allowed=asf["datetime"].min(),
                                max_date_allowed=asf["datetime"].max(),
                                initial_visible_month=asf["datetime"].min(),
                                date="2021-01-10",
                                display_format="DD/MM/Y",
                                )
                        ]),
                    P("** Valores a mais, em relação à atualização anterior.",style={"color": "#fff394"},id="frase")
                ],align='center',xs=3,sm=3,md=3,lg=3,xl=3,xxl=3),
                dbc.Col([dbc.Card([
                    dbc.CardBody([
                        Span("Casos recuperados",className="card-text", id="recup"),
                        H3(style={"color": "#29ffb1"},id="casos-recuperados-text"),
                        Span("Em acompanhamento", className="card-text",id="acom"),
                        H5(id="em-acompanhamento-text"),
                    ])
                ], color="#002b36",
                    style={
                        "box-shadow":"0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                        "color": "white"
                    })],align="center",xs=3,sm=3,md=3,lg=3,xl=3,xxl=3),
                    
                dbc.Col([dbc.Card([
                    dbc.CardBody([
                        Span("Casos confirmados",className="card-text",id="conf"),
                        H3(style={"color": "#ffbb29"},id="casos-confirmados-text"),
                        Span("** Novos casos",className="card-text",style={"color": "#fff394"},id="novo"),
                        H5(id="novos-casos-text",style={"color": "#ffbb29"}),
                    ])
                ], color="#002b36",
                    style={
                        "box-shadow":"0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                        "color": "white"
                    })],align="center",xs=3,sm=3,md=3,lg=3,xl=3,xxl=3),
                dbc.Col([dbc.Card([
                    dbc.CardBody([
                        Span("Óbitos confirmados", className="card-text",id="obit"),
                        H3(style={"color": "#ff29cd"}, id="obitos-text"),
                        Span("** Novos óbitos",className="card-text",style={"color": "#fff394"},id="novo_obit"),
                        H5(id="obitos-na-data-text",style={"color": "#ff29cd"}),
                    ])
                ], color="#002b36",
                    style={
                        "box-shadow":"0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                        "color": "white"
                    })],align="center", xs=3,sm=3,md=3,lg=3,xl=3,xxl=3)
            ],style={"margin-top":"40px"}, justify="evenly"),
            
            
            dbc.Row([
                dbc.Col([
                    RadioItems(
                        id = "radio2",
                        options = [
                            {"label":"Marcar Feriados","value":"fe"},
                            {"label":"Marcar Dias Faltantes","value":"df"},
                            {"label":"Sem Marcação","value":"sm"}
                        ], value = "fe",style = {"margin-top":"10px"}
                    )
                ],align="center",xs=3,sm=3,md=3,lg=3,xl=3),

                dbc.Col([
                    RadioItems(
                        id = "radio",
                        options = [
                            {"label":"Com Imputação De Dias Faltantes","value":"imp"},
                            {"label":"Sem Imputação ","value":"raw"}
                        ], value="imp",
                        style={"margin-top":"15px"}
                    )
                ],align="center",xs=4,sm=4,md=4,lg=4,xl=4),

                dbc.Col([
                    P("Selecione que tipo de dado deseja visualizar:",id = "frase2"),
                    Dropdown(
                        id = "drop",
                        options = [
                            {"label":"Casos Confirmados Por Dia","value":"conf_dia"},
                            {"label":"Sínd.Resp.Grave Por Dia","value":"sars_dia"},
                            {"label":"Notificações","value":"notf_acu"},
                            {"label":"Confirmados","value":"conf_acu"},
                            {"label":"Sexo Dos Pacientes Confirmados","value":"sex_acu"},
                            {"label":"Óbitos","value":"obt_acu"}
                        ], 
                        value="conf_dia"
                    )
                ],align="center",xs=5,sm=5,md=5,lg=5,xl=5)
            ], justify="evenly"),


            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        Graph(
                            id ='graph',
                            config= dict(
                                responsive=True,
                                displayModeBar = False,
                                locale= "en-US"
                            ),
                            figure = fig,
                        )
                    ],color="#002b36",
                    style={
                        "box-shadow":"0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                        "margin-top":"10px",
                        "color": "white"
                    })
                ])
            ],justify="center")
        ]
           )
    ]
)


@app.callback(
    [
    Output("titulo","children"),
    Output("frase","children"),
    Output("data","children"),
    Output("date-picker","display_format"),
    Output("recup","children"),
    Output("conf","children"),
    Output("novo","children"),
    Output("acom","children"),
    Output("obit","children"),
    Output("novo_obit","children"),
    Output("frase2","children"),
    Output("drop","options"),
    Output("radio","options"),
    Output("radio2","options"),
    Output("graph","config")
    ],
    Input("language","value")
)
def switch_language(value):
    if value == "por":
        t = "Covid-19, Ubatuba-SP"
        f = "** Valores a mais, em relação à atualização anterior."
        d = "Informe uma data:"
        dpf = "DD/MM/Y"
        r = "Casos recuperados"
        c = "Casos confirmados"
        n = "** Novos casos"
        a = "Em acompanhamento"
        o = "Óbitos confirmados"
        no = "** Novos óbitos"
        f2 = "Selecione que tipo de dados deseja visualizar:"
        dr = [
            {"label":"Casos Confirmados Por Dia","value":"conf_dia"},
            {"label":"Sínd.Resp.Grave Por Dia","value":"sars_dia"},
            {"label":"Notificações","value":"notf_acu"},
            {"label":"Confirmados","value":"conf_acu"},
            {"label":"Sexo Dos Pacientes Confirmados","value":"sex_acu"},
            {"label":"Óbitos","value":"obt_acu"}
            ]
        r1 = [
            {"label":"Com Imputação De Dias Faltantes","value":"imp"},
            {"label":"Sem Imputação","value":"raw"}
        ]
        r2 = [
            {"label":"Marcar Feriados","value":"fe"},
            {"label":"Marcar Dias Faltantes","value":"df"},
            {"label":"Marcar Meses","value":"sm"}
        ]
        co = dict(
            responsive=True,
            displayModeBar = False,
            locale = "pt-BR"
            )
    else:
        t = "Ubatuba, SP, Brazil. Covid-19"
        f = "** Values more than in the previous update."
        d = "Enter a date:"
        dpf = "MMMM D, YYYY"
        r = "Recovered cases"
        c = "Confirmed cases"
        n = "** New cases"
        a = "Under observation"
        o = "Confirmed decease"
        no = "** New deceased"
        f2 = "Select what type of data you want to visualize:"
        dr = [
            {"label":"Cases Per Day","value":"conf_dia"},
            {"label":"SARS Per Day","value":"sars_dia"},
            {"label":"Notifications","value":"notf_acu"},
            {"label":"Confirmed","value":"conf_acu"},
            {"label":"Confirmed Patient's gender","value":"sex_acu"},
            {"label":"Deaths","value":"obt_acu"}
            ]
        r1 = [
            {"label":"With Missing Days Imputation","value":"imp"},
            {"label":"Without Imputation","value":"raw"}
        ]
        r2 = [
            {"label":"Mark Holidays","value":"fe"},
            {"label":"Mark Missing Days","value":"df"},
            {"label":"Mark Months","value":"sm"}
        ]
        co = dict(
            responsive=True,
            displayModeBar = False,
            locale = "en-US"
            )

    return(
        t,
        f,
        d,
        dpf,
        r,
        c,
        n,
        a,
        o,
        no,
        f2,
        dr,
        r1,
        r2,
        co
    )
           
@app.callback(
    [
    Output("casos-recuperados-text", "children"),
    Output("em-acompanhamento-text", "children"),
    Output("casos-confirmados-text", "children"),
    Output("novos-casos-text", "children"),
    Output("obitos-text", "children"),
    Output("obitos-na-data-text", "children"),
    ],
    Input("date-picker", "date")
)
def pick_a_date(date):
    
    df_data_on_date = asf[asf["datetime"] == date]

    recuperados_acumulado = "-" if df_data_on_date["healed"].isna().values[0] else f'{int(df_data_on_date["healed"].values[0]):,}'.replace(",", ".")  
    acompanhamento = "-" if df_data_on_date["under_obs"].isna().values[0]  else f'{int(df_data_on_date["under_obs"].values[0]):,}'.replace(",", ".")  
    casos_acumulado = "-" if df_data_on_date["positive"].isna().values[0]  else f'{int(df_data_on_date["positive"].values[0]):,}'.replace(",", ".")  
    casos_novos = "-" if df_data_on_date["positive_s"].isna().values[0]  else f'{int(df_data_on_date["positive_s"].values[0]):,}'.replace(",", ".")  
    obitos_acumulado = "-" if df_data_on_date["death"].isna().values[0]  else f'{int(df_data_on_date["death"].values[0]):,}'.replace(",", ".")  
    obitos_novos = "-" if df_data_on_date["death_s"].isna().values[0]  else f'{int(df_data_on_date["death_s"].values[0]):,}'.replace(",", ".")  
    data_nova = df_data_on_date.iloc[0,0].strftime("%d/%m/%Y")
    return (
            recuperados_acumulado, 
            acompanhamento, 
            casos_acumulado, 
            casos_novos, 
            obitos_acumulado, 
            obitos_novos
            )

@app.callback(
    Output("radio2","value"),
    Input("drop","value")
)
def change_labels(value):
    if value not in ["conf_dia","sars_dia"]:
        return "sm"
    else:
        return "fe"

@app.callback(
    Output("radio","value"),
    Input("drop","value")
)
def change_labels_2(value):
    if value not in ["conf_dia","sars_dia"]:
        return "raw"
    else:
        return "imp"


@app.callback(
    Output("graph", "figure"),
    [
    Input("drop", "value"),
    Input("radio", "value"),
    Input("radio2","value"),
    Input("language","value")
    ]
)
def my_callback(value1, value2, value3, value4):
    
    graph = go.Figure(layout={"template":"plotly_dark"})
    
    if value2 == "imp":
        df = imp
    elif value2 == "raw":
        df = raw
        
    if value1 == "notf_acu":
        if value4 =="por":
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["mild"],name="Leve",line_color="#29ffb1"))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["sars"],name="Grave",line_color="#ff29cd",line=dict(dash="dashdot")))
        else:
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["mild"],name="Mild",line_color="#29ffb1"))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["sars"],name="Severe",line_color="#ff29cd",line=dict(dash="dashdot")))

    if value1 == "conf_acu":
        if value4 =="por":
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["positive"],name="Confir.",line_color="#ffbb29"))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["healed"],name="Recup.",line_color="#29ffb1",line=dict(dash="dashdot")))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["death"],name="Óbitos",line_color="#ff29cd"))
        else:
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["positive"],name="Confir.",line_color="#ffbb29"))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["healed"],name="Recov.",line_color="#29ffb1",line=dict(dash="dashdot")))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["death"],name="Deaths",line_color="#ff29cd"))

    if value1 == "sex_acu":
        graph.add_trace(go.Scatter(x=df["datetime"], y=df["fem"],name="Fem.",line_color="#ccd0ff"))
        graph.add_trace(go.Scatter(x=df["datetime"], y=df["masc"],name="Masc.",line_color="#666a94"))

    if value1 == "conf_dia":
        if value4 == "por":
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["positive_s"],name="Casos No Dia"))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["positive_m"],name="Média De 7 Dias",line_color="#33f8ff"))
        else:
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["positive_s"],name="Cases At The Day"))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["positive_m"],name="7 Day Mean",line_color="#33f8ff"))

    if value1 == "sars_dia":
        if value4 =="por":
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["sars_s"],name="Casos No Dia"))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["sars_m"],name="Média De 7 Dias",line_color="#33f8ff"))
        else:
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["sars_s"],name="Cases At The Day"))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["sars_m"],name="7 Day Mean",line_color="#33f8ff"))

    if value1 == "obt_acu":
        if value4 =="por":
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["sars"],name="Grave",line_color="#ff29cd",line=dict(dash="dashdot")))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["death"],name="Óbito",line_color="#ff29cd"))
        else:
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["sars"],name="Severe",line_color="#ff29cd",line=dict(dash="dashdot")))
            graph.add_trace(go.Scatter(x=df["datetime"], y=df["death"],name="Death",line_color="#ff29cd"))

    if value3 == "sm":
        graph.update_layout(
            paper_bgcolor="#002b36",
            plot_bgcolor="#002b36",
            autosize=True,
            height=250,
            width=900,
            margin=dict(l=10, r=10, b=10, t=10),
            xaxis=dict(gridcolor="#1f5954"),
            yaxis=dict(gridcolor="#1f5954")
        )

    elif value3 == "fe":
        if value4 == "por":
            graph.update_layout(
                paper_bgcolor="#002b36",
                plot_bgcolor="#002b36",
                autosize=True,
                height=250,
                width=900,
                margin=dict(l=10, r=10, b=10, t=10),
                xaxis = dict(
                    tickmode='array', tickvals=['2021-01-01','2021-04-02','2021-07-09','2021-06-03'],
                    ticktext=['Ano-Novo','Sexta-Santa','Rev-Const','Corpus-Christi'],
                    tickangle=-45,
                    gridcolor="#1f5954"
                    ),
                yaxis=dict(gridcolor="#1f5954")
                )
        else:
            graph.update_layout(
                paper_bgcolor="#002b36",
                plot_bgcolor="#002b36",
                autosize=True,
                height=250,
                width=900,
                margin=dict(l=10, r=10, b=10, t=10),
                xaxis = dict(
                    tickmode='array', tickvals=['2021-01-01','2021-04-02','2021-07-09','2021-06-03'],
                    ticktext=["New Year","Good Friday","1932 SP Rev.","Corpus-Christi"],
                    tickangle=-45,
                    gridcolor="#1f5954"
                    ),
                yaxis=dict(gridcolor="#1f5954")
                )

    else:
        graph.update_layout(
            paper_bgcolor="#002b36",
            plot_bgcolor="#002b36",
            autosize=True,
            height=250,
            width=900,
            margin=dict(l=10, r=10, b=10, t=10),
            xaxis = dict(
                tickmode='array', tickvals=asf[asf["positive"].isnull()]["datetime"],
                tickangle=-90,
                gridcolor="#1f5954"
                ),
            yaxis=dict(gridcolor="#1f5954")
            )

    return graph 

if __name__ == "__main__":
    app.run_server(debug=True)





# %%
