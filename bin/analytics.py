import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import random
import streamlit.components.v1 as components

from sklearn.neighbors import DistanceMetric
from math import radians


import warnings
warnings.simplefilter('ignore')


def data_manipulation():

    df = pd.read_csv('bin/coordinates.csv')
    dates = pd.date_range(start = '2/1/2022',periods = 70)
    bindata = pd.DataFrame([])
    dataset = pd.DataFrame([])
    for values in dates:
         for i in range(50):
             bindata['Date'] = values
             bindata['Latitude'] = df['Latitute']
             bindata['Longitude'] = df['Longitude ']
             bindata['Bin_Number'] = df['Bin_Number']
             bindata['Bin_value'] = [random.randint(25,100) for x in range(50)]
         dataset = dataset.append(bindata)
        
    dataset.reset_index(inplace=True, drop =True)
    dataset['Date'] = pd.to_datetime(dataset['Date'])

    conditions = [
        (dataset['Bin_Number'] <= 10),
        (dataset['Bin_Number'] > 10) & (dataset['Bin_Number'] <= 20),
        (dataset['Bin_Number'] > 20) & (dataset['Bin_Number'] <= 30),
        (dataset['Bin_Number'] > 30) & (dataset['Bin_Number'] <= 40),
        (dataset['Bin_Number'] > 40)
        ]

    values = [1,2,3,4,5]

    dataset['bin_cate'] = np.select(conditions, values)

    dataset.reset_index(inplace=True, drop = True)

    #dataset.to_csv('finaldata.csv')

   
    
def analytics():

    #data_manipulation()
   

    st.write("Select the Cluster you want to view")
    cluster_value = st.selectbox('Cluster',[1,2,3,4,5])



    dataset = pd.read_csv('bin/finaldata.csv')
    dataset = dataset[['Date','Bin_Number','Bin_value','bin_cate']]
   


    if cluster_value == 1:
            temp_data = dataset[dataset['bin_cate']==1]
            temp_data.reset_index(inplace=True,drop = True)
            
    if cluster_value == 2:
            temp_data = dataset[dataset['bin_cate']==2]
            temp_data.reset_index(inplace=True,drop = True)
    if cluster_value == 3:
            temp_data = dataset[dataset['bin_cate']==3]
            temp_data.reset_index(inplace=True,drop = True)

    if cluster_value == 4:
            temp_data = dataset[dataset['bin_cate']==4]
            temp_data.reset_index(inplace=True,drop = True)

    if cluster_value == 5:
            temp_data = dataset[dataset['bin_cate']==5]
            temp_data.reset_index(inplace=True,drop = True)
    
     
    grouped_data = temp_data.groupby(['Date']).mean()
    grouped_data.reset_index(inplace=True)
    grouped_data = grouped_data[['Date','Bin_value']]

    st.subheader("The bin data for the specific cluster is")
    st.write(temp_data)

    st.subheader("The overall cluster data is")
    st.write(grouped_data)
    grouped_data['Date'] = pd.to_datetime(grouped_data['Date'])


    st.subheader('Trend value and mean of the cluster')

    fig102 = px.scatter(grouped_data, x='Date',y='Bin_value', trendline='ols',color='Bin_value')
    fig102.update_traces(mode="markers+lines", hovertemplate=None)
    fig102.update_layout(hovermode="x")
    st.plotly_chart(fig102, use_container_width=True)

    fig5 = px.scatter(temp_data, x='Bin_Number',y='Bin_value',color ='Bin_value', title ='Bin Level ')
    st.plotly_chart(fig5, use_container_width=True)
    

   
    #fig17 = px.scatter(grouped_data, x='Bin_Number',y='Bin_value',color ='Bin_value',trendline = 'ols')
    #st.plotly_chart(fig17, use_container_width=True)

   

    indiv()



def indiv():
    st.subheader("Individual bin values")

    st.write("To display the average waste collected on each day use all")
    HtmlFile = open("bin/home.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code,width =1350,height=2350)
    














