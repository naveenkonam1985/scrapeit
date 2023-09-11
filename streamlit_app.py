# Streamlit app file
# Importing libraries
from requests.api import options
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Table Crawler", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

connection = False

# Sidebar config
with st.sidebar:
    st.title("ScrapeIt")
    st.header("Table Crawler")
    st.write("A simple table crawler built with Python")
    
    # Input for URL
    url = st.text_input("Please enter the URL to scrape the tables")

    try:
        # Clicked status for click me button
        if 'clicked' not in st.session_state:
            st.session_state.clicked = False

        # Function for enabling clicked 
        def click_button():
            st.session_state.clicked = True

        
        # Button for click me
        st.button('Click me', on_click=click_button,type='primary')
        if st.session_state.clicked:
            html = requests.get(url=str(url))
            if html.status_code in [200]:
                st.write("The connection successful")
                connection = True
                data = html.text
            else:
                st.write("Seems the entered url is not valid")

    except Exception:
        st.write("Please enter a url")

    st.write("Note: This app searches for table tag in the html page, so it returns the table only if concern tags exists.")


# Main Container config
with st.container():
    st.markdown("#### Scraped Tables from the URL")
    # Defining tables dictionary
    table_dict = {}
    
    # Getting the soup object
    if connection:
        soup = BeautifulSoup(data, 'lxml')
        tables = soup.find_all('table')
        
        # If found any tables, add them to table_dict
        if tables:
            for i,tab in enumerate(tables):
                table_dict[f'Table{i+1}'] = pd.read_html(str(tab),header=0)[0]

                st.write(f"Table{i+1}")
                st.dataframe(table_dict[f'Table{i+1}'], use_container_width=True)

        else:
            st.write("No tables with tag 'table' in the web page")

    else:
        st.write("No url for scraping tables")

    # Itertaing through table_dict to select the table and download the data
    try:
        if table_dict:
            
            # Selection box from the list of tables
            if 'selected' not in st.session_state:
                st.session_state.selected = False
            
            # Function for enabling selected value
            def selected_box():
                st.session_state.selected = True

            # List of values for select box
            options_list = ['None']
            options_list.extend(list(table_dict.keys()))
            selected_value = st.selectbox('Select Table to Download', options=options_list, on_change=selected_box)
            
            # Writing selected value
            if st.session_state.selected:
                st.write(f"Selected option is {selected_value}")

            
            # Download Button for download
            if 'loaded' not in st.session_state:
                st.session_state.loaded = False

            # Function for enabling loaded
            def loaded_button():
                st.session_state.loaded = True

            # Function for download csv data with cache
            @st.cache_resource
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')
            
            # Download based on the selected value
            if selected_value != 'None':
                csv = convert_df(table_dict[selected_value])
                download = st.download_button('Download', data=csv, file_name=f"{selected_value}.csv",on_click=loaded_button, type='primary')
                
                if download:
                    st.write(f"{selected_value} Downloaded")

    except Exception:
        st.write("Not able to extract tables")
