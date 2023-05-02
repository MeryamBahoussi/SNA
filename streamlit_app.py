import streamlit as st
from azure.storage.blob import BlobServiceClient
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



#############################################
# Setup variables for Azure Data lake
#############################################
storageAccount = "sasnadatalake"
containerName = "sna"
accessKey = "JyC+4No6iP37g5K0BfGtN9UoihS3Hn8uND/R1wc1CNclAmkMPcSCk2FTbJybreIhUgVKTJdN+0kC+ASt2A4WNg=="


#############################################
# Setup connection to Azure Data lake
#############################################
connectionString = f"DefaultEndpointsProtocol=https;AccountName={storageAccount};AccountKey={accessKey};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connectionString)
container_client = blob_service_client.get_container_client(containerName)
