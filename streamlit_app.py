# Streamlit app file
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup


with st.sidebar:
    st.title("ScrapeIt")
    st.header("Table Crawler")
    st.write("A simple table crawler built with Python")
    url = st.text_input("Please enter the URL to scrape the tables", key='url_path')
    connection = False
    
    try:
        if st.button("Click", type='primary'):
            html = requests.get(url=str(url))
            if html.status_code in [200]:
                st.write("The connection successful")
                connection = True
                data = html.text

    except Exception:
        st.write("Please enter a url")

df = pd.DataFrame({"SNo":[1,2,3], "Name":['a','b','c'], "phone":[1,2,3]})
st.dataframe(df)

@st.cache_resource
def convert_df(df):
    return df.to_csv().encode('utf-8')
csv = convert_df(df)

st.download_button("Download as csv", data=csv,file_name="data.csv")

st.subheader("The Scraped tables from URL")

if connection:
    st.write("You can scrape data")
    soup = BeautifulSoup(data)
    tables = soup.find('table')
    df_table = pd.read_html(str(tables))[0]
    st.dataframe(df_table) 

