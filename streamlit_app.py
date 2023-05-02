import streamlit as st
import pandas as pd
import pickle
from azure.storage.blob import BlobServiceClient


#############################################
# Setup Streamlit config
#############################################
st.set_page_config(page_title = "SNA-TM", layout='wide')
st.sidebar.markdown("SNA-TM")



#############################################
# Setup variables for Azure Data lake
#############################################
storageAccount = "sasnadatalake"
containerName = "sna"
accessKey = "JyC+4No6iP37g5K0BfGtN9UoihS3Hn8uND/R1wc1CNclAmkMPcSCk2FTbJybreIhUgVKTJdN+0kC+ASt2A4WNg=="
