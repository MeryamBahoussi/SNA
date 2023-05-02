import streamlit as st
# from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import BytesIO
import pickle
from bertopic import BERTopic
from os import path


#############################################
# Setup Streamlit config
#############################################
st.set_page_config(page_title = "SNA-TM", layout='wide')
st.sidebar.markdown("SNA-TM")
