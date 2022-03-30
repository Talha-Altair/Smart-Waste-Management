import streamlit as st
import Data_etl
import streamlit.components.v1 as components
import time
import prediction
import analytics




def app():
    st.header('Municipality Smart Waste Management System')

    db = st.sidebar.radio('View BIN 1',['Dashboard','Table','Dustbin Data','Location','Analytics','GarbageCollection'])

  
    if db =='Dashboard':
        page = Data_etl
        page.dataetl()
      
    if db == 'Table':
        st.subheader('House no:1')
        st.write("House ID:001")
        page = Data_etl
        page.table()
    if db == 'Dustbin Data':
        st.write("House ID:001")
        page = Data_etl
        page.dustbindata()
    if db == 'Location':
        page = Data_etl
        page.location()
    if db == 'Analytics':
        page = analytics
        page.analytics()
    if db == 'GarbageCollection':
        page = prediction
        page.pred()


