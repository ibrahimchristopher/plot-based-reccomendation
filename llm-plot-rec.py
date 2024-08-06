# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 08:33:45 2024

@author: user
"""

import json


API_KEY = "18c0530f-d2f0-4fec-b5f2-7bf9a4e5ddb8"
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

pc = Pinecone(api_key=API_KEY)

index = pc.Index('movie-plot')
# Specify the file name
file_name = "movie_names_and_ids.json"

# Reading the JSON file into a dictionary
with open(file_name, 'r') as json_file:
    movie_names_and_ids = json.load(json_file)

movie_list = list(movie_names_and_ids.keys())

movie_list.sort()

import streamlit as st

st.title('Plot Based Movie Reccomendation')

st.text("By Ibrahim Ibrahim")

st.header("Generating Movie Reccomendations Leveraging Vector Databases via Pinecone and Langchain")

st.subheader("Select Movie")

#st.text("hello world text")

#st.markdown("this is a markdown")

#st.success("Text Goes Here")

#st.info("Text Goes Here")

#st.warning("Text Goes Here")

#st.error("Text Goes Here")

#exp = ZeroDivisionError("trying to divide by 0")

#st.exception(exp)


    
movie_name = st.selectbox('Movie: This List Contans 10K Movies', movie_list)

movie_id = movie_names_and_ids[movie_name]

res = index.fetch(ids=[movie_id])

res = res.to_dict()
metadata = res['vectors'][movie_id]['metadata']


def get_reccomendations(movie_name):
  #get the id
  movie_id = movie_names_and_ids[movie_name]
  #use the id to query and get results
  similar_movies = index.query(
  id=movie_id,top_k=6,
  include_metadata=True)
  scores = [i['score'] for i in similar_movies['matches']]
  metadata = [i['metadata'] for i in similar_movies['matches']]

  return metadata, scores

def write_to_screen(movie):
    st.write('Plot')
    st.write(movie['overview'])
    st.write('Cast')
    st.write(movie['crew'])
status = st.checkbox("show plot and cast")
if st.button('Generate Reccomendations'):
    metadata, scores = get_reccomendations(movie_name)
    st.header(f"Reccomendations If You Liked: {movie_name}")
    
    for i in range(len(scores)):
        score = scores[i]
        movie = metadata[i]
        st.subheader(f"Movie name: {movie['names']} | Similarity : {100 * score}%")
        if status:
            write_to_screen(movie)