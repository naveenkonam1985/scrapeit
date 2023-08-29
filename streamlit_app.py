# Streamlit app file
# Importing libraries
from requests.api import options
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

table_dict = {}
connection = False

# Sidebar
with st.sidebar:
    st.title("ScrapeIt")
    st.header("Table Crawler")
    st.write("A simple table crawler built with Python")
    url = st.text_input("Please enter the URL to scrape the tables")

    try:
        if 'clicked' not in st.session_state:
            st.session_state.clicked = False

        def click_button():
            st.session_state.clicked = True

        st.button('Click me', on_click=click_button)
        #if st.button("Click", type='primary'):
        if st.session_state.clicked:
            html = requests.get(url=str(url))
            if html.status_code in [200]:
                st.write("The connection successful")
                connection = True
                data = html.text

    except Exception:
        st.write("Please enter a url")

    st.write("Note: This app searches for table tag in the html page, so it returns the table only if concern tags exists.")


# Main Container
with st.container():
   st.markdown("#### Scraped Tables from the URL")
   if connection:
       soup = BeautifulSoup(data, 'lxml')
       tables = soup.find_all('table')

       if tables:
           for i,tab in enumerate(tables):
               table_dict[f'Table{i+1}'] = pd.read_html(str(tab))[0]

               st.write(f"Table{i+1}")
               st.dataframe(table_dict[f'Table{i+1}'])

           @st.cache_resource
           def convert_df(df):
               return df.to_csv(index=False)

           #csv = convert_df()
           #st.download_button("Download as csv", data=csv,file_name=f"table{i+1}.csv")
           #st.button("Download", on_click=convert_df, key=f'table{i+1}')

       else:
           st.write("No tables with tag 'table' in the web page")

   else:
       st.write("No url for scraping tables")


try:
    if table_dict:
        st.write(table_dict.keys())

        if 'loaded' not in st.session_state:
            st.session_state.loaded = False

        def loaded_button():
            st.session_state.loaded = True

        st.button('Download', on_click=loaded_button)

        if st.session_state.loaded:
            table_dict['Table1'].to_csv('data.csv')
            st.write("Downloaded")
except Exception:
    pass
