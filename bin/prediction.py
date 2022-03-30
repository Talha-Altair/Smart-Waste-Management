import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

import random
from sklearn.neighbors import DistanceMetric
from math import radians


import warnings
warnings.simplefilter('ignore')

def pred():
    df = pd.read_csv('bin/finaldata.csv')
    present_data = df.tail(50)
    lat_mean = []
    long_mean = []
    bin_mean = []
    for value in present_data['bin_cate'].unique():
        temp_data = present_data[present_data['bin_cate']==value]
        mean_lat_val = np.mean(temp_data['Latitude'])
        mean_long_val = np.mean(temp_data['Longitude'])
        mean_bin_val = np.mean(temp_data['Bin_value'])
        lat_mean.append(mean_lat_val)
        long_mean.append(mean_long_val)
        bin_mean.append(mean_bin_val)

    present_data_sample = {
    'latitude':lat_mean,
    'longitude':long_mean,
    'Binvalue':bin_mean,
    'cluster':[1,2,3,4,5]
    
    }


    present_data_sample = pd.DataFrame(present_data_sample)

    st.subheader("Today's up-to-date Data collected from every bin")


    st.write(present_data_sample[['cluster','Binvalue']])

    present_data_sample['latitude'] = np.radians(present_data_sample['latitude'])
    present_data_sample['longitude'] = np.radians(present_data_sample['longitude'])
    dist = DistanceMetric.get_metric('haversine')
    dj = pd.DataFrame(dist.pairwise(present_data_sample[['latitude','longitude']].to_numpy())*6373,  columns=present_data_sample.cluster.unique(),
     index=present_data_sample.cluster.unique())
    clusters = ['Cluster1','Cluster2','Cluster3','Cluster4','Cluster5']
    dj.columns = clusters
    dj.index = clusters
    dj = dj.round(3)
    list_dj = dj.to_numpy()
    sub_dj = pd.DataFrame(list_dj[0],columns =['Distance'])
    sub_dj['binvalue'] = present_data_sample['Binvalue']
    max_bin = max(sub_dj['binvalue'])

    st.subheader("Choose ective smart waste collection")
    selection_value_waste = st.selectbox('Choose',['Yes','No'],key ='wasteselection')


    if selection_value_waste =='Yes':
      
        
        st.write("The maximum value at present is {}".format(max_bin))

       
        
        if np.int(max_bin)>60:
            location_cat = sub_dj[sub_dj['binvalue']==max_bin].index.values.astype(int)    
            sub_dj1 = sub_dj.copy()
            sub_dj1.index = clusters
            output_values = sub_dj1.iloc[location_cat]
            st.write('Start from cluster',output_values.to_html(),unsafe_allow_html=True)
            st.subheader("Different paths for clusters")
            st.graphviz_chart("""
                        digraph{
                        Cluster1-> Cluster2
                        Cluster1 -> Cluster3
                        Cluster3 -> Cluster5
                        Cluster5  -> Cluster4
                        Cluster4 -> Cluster2
                        Cluster1 -> Cluster4
                        Cluster4 -> Cluster5
                      
                      
                        }
                        """, use_container_width = True)

            short()
    else:

        st.write("The distance (in KM) from each cluster is given below, choose at your convenience")

        st.write(dj)

        st.write('At each cluster, the present bin value is')
        sub_dj1 = sub_dj.copy()
        sub_dj1.index = clusters  
        st.write(sub_dj1['binvalue'])




def short():
    graph ={
        'Cluster1':['Cluster2','Cluster4','Cluster3'],

        'Cluster2':['Cluster1','Cluster4'],
        'Cluster3':['Cluster5'],
        'Cluster4':['Cluster2','Cluster5'],
        'Cluster5':['Cluster4', 'Cluster3']
        }
        
        # function to find the shortest path
    def find_shortest_path(graph, start, end, path =[]):
                path = path + [start]
                if start == end:
                    return path
                shortest = None
                for node in graph[start]:
                    if node not in path:
                        newpath = find_shortest_path(graph, node, end, path)
                        if newpath:
                            if not shortest or len(newpath) < len(shortest):
                                shortest = newpath
                return shortest
                
        # Driver function call to print
        # the shortest path
    st.subheader("Shortest path to reach cluster")
    val1 = st.selectbox("Choose FROM Cluster",['Cluster1','Cluster2','Cluster3','Cluster4','Cluster5'],key ="Clusterpoint1")
    val2 = st.selectbox("Choose TO  Cluster",['Cluster1','Cluster2','Cluster3','Cluster4','Cluster5'], key ="Clusterpoint2")

    values = find_shortest_path(graph, val1, val2)
    st.write("You can reach by")
    for i in values:
        
        st.write(i)
            
           
    HtmlFile = open("bin/cluster.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code,width =1000,height=800)



