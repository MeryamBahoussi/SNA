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


#############################################
# Get last gold files
#############################################
rootPath = "topic-modeling"
dataPath = "/gold/data"
modelPath = "/gold/model"

blob_list = container_client.list_blobs(name_starts_with=f"{rootPath}{modelPath}")
available_models = [blob.name for blob in blob_list]
date = available_models[-1][35:45]

st.sidebar.write(f"Date : {date}")

topicsFile = f"{rootPath}{dataPath}/topics_{date}.parquet"
predsFile = f"{rootPath}{dataPath}/preds_{date}.parquet"
modelFile = f"{rootPath}{modelPath}/bertopic_{date}.pkl"


#############################################
# Load Azure files
#############################################
def load_blob(blob):
    stream_downloader = container_client.download_blob(blob)
    stream = BytesIO()
    stream_downloader.readinto(stream)
    df = pd.read_parquet(stream)
    return df


def load_parquet(path):
    blob_list = container_client.list_blobs(name_starts_with=f"{path}/part-")
    df = pd.DataFrame()
    for blob in blob_list:
        blob_df = load_blob(blob.name)
        df = pd.concat([df, blob_df], ignore_index=True)
    return df


topics = load_parquet(topicsFile)
preds = load_parquet(predsFile)

local_file = f"/tmp/bertopic_{date}.pkl"
if path.exists(local_file):
    model = pickle.load(open(local_file, 'rb'))
else:
    stream_downloader = container_client.download_blob(modelFile)
    object = stream_downloader.readall()
    model = pickle.loads(object)
    pickle.dump(model, open(local_file, 'wb'))


#############################################
# Topics over time
#############################################
st.header("Topics over time")

tmp_topics = topics[['short_name', 'full_name']]
tmp_topics = tmp_topics.rename(columns={"short_name": "Topic", "full_name": "Name"})
tmp_preds = preds[['topic_short_name', 'description', 'date', 'frequency']]
tmp_preds = tmp_preds.rename(columns={"topic_short_name": "Topic", "description": "Words", "date": "Timestamp", "frequency": "Frequency"})
topics_over_time = pd.merge(tmp_topics, tmp_preds, on='Topic', how='outer')

st.plotly_chart(model.visualize_topics_over_time(topics_over_time))


#############################################
# Search topics
#############################################
st.header("Search topics")

search_term = st.text_input('Topic search', 'nft art')
st.write('The current search is', search_term)

topics_info = model.get_topic_info()
topics_id, topics_contrib = model.find_topics(search_term, top_n=5)
d = {'Topic': topics_id, 'Confidence': topics_contrib}
search_df = pd.DataFrame(data=d)
search_df = topics_info.merge(search_df, on='Topic')
search_df = search_df[['Name', 'Confidence']].sort_values(by=['Confidence'], ascending=False)

st.write(search_df)


#############################################
# Topics distribution
#############################################
st.header("Topics distribution")
st.plotly_chart(model.visualize_topics())


#############################################
# Topics hierarchy
#############################################
st.header("Topics hierarchy")
st.plotly_chart(model.visualize_hierarchy())
