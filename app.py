import streamlit as st
from googleapiclient.discovery import build

import os
API_KEY = os.getenv("API_KEY")

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(query, max_results=5):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    search_response = youtube.search().list(
        q=query, part="id,snippet", maxResults=max_results, type="video"
    ).execute()
    return [
        {
            "id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
        }
        for item in search_response["items"]
    ]

st.set_page_config(page_title="Music Search", layout="wide")
st.markdown("<h2 style='text-align:center;'>🎵 Music Search</h2>", unsafe_allow_html=True)

query = st.text_input("Enter Song, Artist, or Movie Name:")

if query:
    results = youtube_search(query)

    for vid in results:
        st.markdown(f"**{vid['title']}**", unsafe_allow_html=True)
        st.markdown(
            f"""
            <iframe width="400" height="225"
            src="https://www.youtube.com/embed/{vid['id']}?autoplay=0"
            frameborder="0"
            allow="autoplay; encrypted-media"
            allowfullscreen></iframe>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")
