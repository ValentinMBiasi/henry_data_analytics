import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go

df_internet = pd.read_csv('df_internet.csv', parse_dates=True, index_col='datetime')
df_inflacion = pd.read_csv('df_inflacion.csv', parse_dates=True, index_col='d')
df_ingresos = pd.read_csv('df_ingresos.csv', parse_dates=True, index_col='datetime')
df_crecimiento_real = pd.read_csv('df_crecimiento_real.csv', parse_dates=True, index_col='datetime', names=['datetime', 'Crecimiento real por trimestre'])
df_crecimiento_real_total = pd.read_csv('df_crecimiento_real_total.csv', parse_dates=True, index_col='datetime', names=['datetime', 'Crecimiento real total'])

st.set_page_config(layout="wide")

page = st.sidebar.selectbox('Escoja la página:', ['Dashboard','Internet', 'Ingresos'])


if page == 'Dashboard':
   st.header("Dashboard")

   geography = st.selectbox("Escoja geografía:", df_internet.columns)

   cols = st.columns(4)

# KPI 1: Aumento de 2% en el acceso a Internet por provincia cada 100 hogares
   ultimo_registro = df_internet.iloc[-1][geography]
   penultimo_registro = df_internet.iloc[-2][geography]

   cambio_porcentual = (ultimo_registro - penultimo_registro) / penultimo_registro

   objetivo = 0.02

   indicator = go.Indicator(
    title={'text': 'Acceso a Internet cada 100 hogares'},
    mode = "number+delta",
    value = ultimo_registro,
    delta={'reference': penultimo_registro, 'relative': True, 'valueformat': '.2%'})
   
   fig = go.Figure(data=[indicator])
   fig.add_annotation(
        text=f'Objetivo: Aumento de {objetivo:.0%}',
        showarrow=False,
        xanchor='center',
        yshift=70,
        font={'size': 20, 'color': '#00FF00' if cambio_porcentual >= objetivo else '#FF0000'}
    )

   fig.update_layout(height=200, width=200, margin=dict(t=0, b=0, l=0, r=0))
   cols[0].plotly_chart(fig, use_container_width=True)

   indicator = go.Indicator(
    mode = "number+delta",
    value = 0)
   fig = go.Figure(data=[indicator])
   fig.update_layout(height=200, width=200, margin=dict(t=0, b=0, l=0, r=0))
   cols[1].plotly_chart(fig, use_container_width=True)

   indicator = go.Indicator(
    mode = "number+delta",
    value = 0)
   fig = go.Figure(data=[indicator])
   fig.update_layout(height=200, width=200, margin=dict(t=0, b=0, l=0, r=0))
   cols[2].plotly_chart(fig, use_container_width=True)

   indicator = go.Indicator(
    mode = "number+delta",
    value = 0)
   fig = go.Figure(data=[indicator])
   fig.update_layout(height=200, width=200, margin=dict(t=0, b=0, l=0, r=0))
   cols[3].plotly_chart(fig, use_container_width=True)


# Acceso a internet, grafico de lineas

   fig = px.line(df_internet[geography], title = 'Acceso a Internet cada 100 hogares: ' + geography)
   fig.update_layout(showlegend=False, xaxis_title='Año y trimestre', yaxis_title='Acceso a Internet cada 100 hogares')
   st.plotly_chart(fig, use_container_width = True)

#Grafico de barras, crecimiento real total por internet

   bar = go.Bar(
    x=df_crecimiento_real.index,
    y=df_crecimiento_real['Crecimiento real por trimestre'],
    marker = dict(color = ['rgba(63, 195, 128, 1)' if x > 0 else 'rgba(219, 10, 91, 1)' for x in df_crecimiento_real['Crecimiento real por trimestre']], 
                 line = dict(color='rgb(0,0,0)',width=1.5)),
   text=df_crecimiento_real,
        textposition='outside'
)
   fig = go.Figure(data=[bar])
   fig.update_layout(title='Crecimiento real a nivel Nación de ingresos por Internet fijo (quitando inflación, expresado en %)', xaxis_title='Año y trimestre', yaxis_title='Crecimiento real (%)')
   st.plotly_chart(fig, use_container_width = True)


   #Grafico de barras, crecimiento real total telecomunicaciones

   bar = go.Bar(
    x=df_crecimiento_real_total.index,
    y=df_crecimiento_real_total['Crecimiento real total'],
    marker = dict(color = ['rgba(63, 195, 128, 1)' if x > 0 else 'rgba(219, 10, 91, 1)' for x in df_crecimiento_real_total['Crecimiento real total']], 
                 line = dict(color='rgb(0,0,0)',width=1.5)),
   text=df_crecimiento_real_total,
        textposition='outside'
)
   fig = go.Figure(data=[bar])
   fig.update_layout(title='Crecimiento real a nivel Nación de ingresos de Telecomunicaciones (quitando inflación, expresado en %)', xaxis_title='Año y trimestre', yaxis_title='Crecimiento real (%)')
   st.plotly_chart(fig, use_container_width = True)


elif page == 'Internet':
  ## Continents
  st.header("Acceso a Internet")

  options = st.multiselect('Escoja los gráficos deseados:', ['Data', 'Trend', 'Seasonality', 'Residuals'], ['Data', 'Trend'])

  col1,col2 = st.columns(2)

  #Col 1
  geography = col1.selectbox("Escoja geografía:", df_internet.columns, key=1)
  decompose = sm.tsa.seasonal_decompose(df_internet[geography])
  figs = []
  for option in options:
    if option == 'Data':
        figs.append(px.line(decompose.observed, title = geography + ' ' + option))
    elif option == 'Trend':
        figs.append(px.line(decompose.trend, title = geography + ' ' + option))
    elif option == 'Seasonality':
        figs.append(px.line(decompose.seasonal, title = geography + ' ' + option))
    elif option == 'Residuals':
        figs.append(px.line(decompose.resid, title = geography + ' ' + option))
  
  for fig in figs:
     fig.update_layout(showlegend=False)
     col1.plotly_chart(fig, use_container_width = True)

  #Col 2
  geography2 = col2.selectbox("Escoja geografía:", df_internet.columns, key=2)
  decompose = sm.tsa.seasonal_decompose(df_internet[geography2])
  figs = []
  for option in options:
    if option == 'Data':
        figs.append(px.line(decompose.observed, title = geography2 + ' ' + option))
    elif option == 'Trend':
        figs.append(px.line(decompose.trend, title = geography2 + ' ' + option))
    elif option == 'Seasonality':
        figs.append(px.line(decompose.seasonal, title = geography2 + ' ' + option))
    elif option == 'Residuals':
        figs.append(px.line(decompose.resid, title = geography2 + ' ' + option))
  
  for fig in figs:
     fig.update_layout(showlegend=False)
     col2.plotly_chart(fig, use_container_width = True)

elif page == 'Ingresos':
   fig = px.line(df_crecimiento_real, title = 'Crecimiento real (quitando inflación) de ingresos por Internet fijo (%)')
   fig.update_layout(showlegend=False)
   st.plotly_chart(fig, use_container_width = True)
#    col1,col2 = st.columns(2)
#    fig = px.line(df_inflacion['Inflacion trimestral'].dropna(), title = 'Inflación acumulada por trimestre (%)')
#    fig.update_layout(showlegend=False)
#    col1.plotly_chart(fig, use_container_width = True)

#    fig = px.line((df_ingresos.pct_change() * 100), title = 'Variación trimestral de ingresos por Internet fijo (%)')
#    fig.update_layout(showlegend=False)
#    col2.plotly_chart(fig, use_container_width = True)
   

elif page == 'Telefonía':
  ## Countries
  st.header("Acceso a telefonia")
  clist = df_internet.columns
  country = st.selectbox("Select a country:",clist)
  col1, col2 = st.columns(2)
  fig = px.line(df_internet[country], title = country)
 
  col1.plotly_chart(fig,use_container_width = True)
  fig = px.line(df_internet[country], title = country)
  
  col2.plotly_chart(fig,use_container_width = True)

