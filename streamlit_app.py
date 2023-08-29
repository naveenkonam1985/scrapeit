# Streamlit app file
# Importing libraries
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Sidebar
with st.sidebar:
    st.title("ScrapeIt")
    st.header("Table Crawler")
    st.write("A simple table crawler built with Python")
    url = st.text_input("Please enter the URL to scrape the tables")
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

# Main Container
with st.container():
   st.markdown("#### Scraped Tables from the URL")
   if connection:
       soup = BeautifulSoup(data, 'lxml')
       tables = soup.find_all('table')

       for i,tab in enumerate(tables):
           df_table = pd.read_html(str(tab))[0]

           st.write(f"Table{i+1}")
           st.dataframe(df_table)

           @st.cache_resource
           def convert_df(df):
               return df.to_csv().encode('utf-8')

           csv = convert_df(df_table)
           st.download_button("Download as csv", data=csv,file_name=f"table{i+1}.csv")
   else:
       st.write("No url for scraping tables")
