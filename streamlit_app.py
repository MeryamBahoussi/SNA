import streamlit as st
import pandas as pd
import pickle

from azure.storage.blob import BlobServiceClient

  

#############################################
# Setup Streamlit config
#############################################
st.set_page_config(page_title = "SNA-TMMM", layout='wide')
st.sidebar.markdown("SNA-TM")
