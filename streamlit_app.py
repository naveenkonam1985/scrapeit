# Streamlit app file
import streamlit as st
import pandas

st.title("Table Crawler")
st.header("ScrapeIt")

df = pd.DataFrame({"SNo":[1,2,3], "Name":['a','b','c'], "phone":[1,2,3]})
st.dataframe(df)
