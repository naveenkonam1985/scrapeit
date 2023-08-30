# Streamlit app file
# Importing libraries
from requests.api import options
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

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

        st.button('Click me', on_click=click_button,type='primary')
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
    table_dict = {}
    if connection:
        soup = BeautifulSoup(data, 'lxml')
        tables = soup.find_all('table')

        if tables:
            for i,tab in enumerate(tables):
                table_dict[f'Table{i+1}'] = pd.read_html(str(tab))[0]

                st.write(f"Table{i+1}")
                st.dataframe(table_dict[f'Table{i+1}'])

            #@st.cache_resource
            #def convert_df(df):
            #    return df.to_csv(index=False)

            #csv = convert_df()
            #st.download_button("Download as csv", data=csv,file_name=f"table{i+1}.csv")
            #st.button("Download", on_click=convert_df, key=f'table{i+1}')

        else:
            st.write("No tables with tag 'table' in the web page")

    else:
        st.write("No url for scraping tables")


    try:
        if table_dict:
            
            # Selection box from the list of tables
            if 'selected' not in st.session_state:
                st.session_state.selected = False
            
            def selected_box():
                st.session_state.selected = True

            options_list = ['None']
            options_list.extend(list(table_dict.keys()))
            
            selected_value = st.selectbox('Tables', options=options_list, on_change=selected_box)
            
            if st.session_state.selected:
                st.write(f"Selected option is {selected_value}")
            
            # Button for download
            if 'loaded' not in st.session_state:
                st.session_state.loaded = False

            def loaded_button():
                st.session_state.loaded = True

            st.button('Download', on_click=loaded_button, type='primary')

            if st.session_state.loaded:
                table_dict[selected_value].to_csv(f'{selected_value}.csv')
                st.write(f"{selected_value} Downloaded")

    except Exception:
        st.write("Not able to get tables")
