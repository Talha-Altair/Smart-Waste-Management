
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from firebase import firebase
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=3000,key='dashrefresh')

def dataset():
    fb_app = firebase.FirebaseApplication('https://swms-bin-default-rtdb.firebaseio.com/', None)
    result = fb_app.get('/', None)
    data = pd.DataFrame(result)
    data.dropna(inplace= True)
    data['Date'] = data['Bin2'].str[:18]
    data['Date']= pd.to_datetime(data['Date'])
    data['bin'] = data['Bin2'].str[19:21].astype(int)
    data['temp'] = pd.to_numeric(data['Bin2'].str[22:27],errors='coerce').astype(float)
    data['humidty'] = pd.to_numeric(data['Bin2'].str[28:],errors='coerce').astype(float)

    data = data[['Date','bin','temp','humidty']]
    data.columns = ['Date','BinLevel','Temperature','Humidity']

 

    return data

    #data.to_csv("D:/Final Year Project/smart-waste-management-system-in-cities-/Web application/BinData.csv")

def dataetl():
    data = dataset()
    current = data.tail(1)

    def graph(x):
        st.write("The current level of the dustbin in house:001 is")
        st.subheader("House No: 001 - BIN 1")

        
       
        fig1 = px.bar(current,x='Date',y='BinLevel',color_discrete_sequence=[x])
        fig1.update(layout_yaxis_range = [0,101])
        st.plotly_chart(fig1, use_container_width=True)
    val = current['BinLevel'].all()

    if val>=85:
        x ='red'
        graph(x)

    if val in range(50,84):
        x ='yellow'
        graph(x)
    if val<50:
        graph(x ='green')

def table():
    data = dataset()

    table_values = data.tail().reset_index(drop = True)
    st.table(table_values)

def dustbindata():
    data = dataset()
    st.subheader('Overall Bin Level')
    fig2 = px.line(data, x='Date',y='BinLevel', title ='Overall Bin Level ')
    fig3 = px.scatter(data, x='Date',y='BinLevel', title ='Overall Bin Level ',color_discrete_sequence=['red'])
    fig4 = go.Figure(data=fig2.data + fig3.data)
    st.plotly_chart(fig4, use_container_width=True)
    


    st.subheader("Temperature and Humidity of Bin1")
    col1,col2 = st.columns(2)
    fig5 = px.scatter(data, x='Date',y='Temperature',color = 'Temperature')
    fig6 = px.scatter(data, x='Date',y='Humidity',color = 'Humidity')
    col1.plotly_chart(fig5, use_container_width=True)
    col2.plotly_chart(fig6, use_container_width=True)


    lineplt1  = px.line(data, x='Date',y='Temperature', color_discrete_sequence=['red'])
    lineplt2  = px.line(data, x='Date',y='Humidity', color_discrete_sequence=['blue'])
    lineplot  = go.Figure(data=lineplt1.data + lineplt2.data)
    st.plotly_chart(lineplot, use_container_width=True)




    

def location():
    st.text('Live Data of the Dustbin from house is 12.88092504916983, 80.01798407637298')
    st.image('bin/house.png')