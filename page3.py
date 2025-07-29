# Topic Modeling

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import plotly.graph_objects as go
import matplotlib.colors as mcolors


def show():

    st.header('Word Cloud of Each University')
    df = st.session_state['df']

    usernames = df['username'].unique()


    selected_user = st.selectbox("Choose University:", usernames, key='wordcloud')
    user_texts = df[df['username'] == selected_user]['clean_text']
    combined_text = " ".join(user_texts.dropna().astype(str))

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(f"Wordcloud of {selected_user}")

    st.pyplot(fig)


    
    st.header("Most Discussed Topics Across the University")
    df = df.dropna(subset=['topic_keywords'])

    Topic_terbanyak = df['topic_keywords'].value_counts().reset_index()
    Topic_terbanyak.columns = ['Topic', 'Total']

    st.subheader("List of Most Popular Topics")
    st.dataframe(Topic_terbanyak)

    st.subheader("Visualization of Popular Topics")
    st.bar_chart(Topic_terbanyak.set_index('Topic'))


    st.header('Top Topic Keywords for Each University')
    selected_user = st.selectbox("Choose Username", sorted(usernames), key="topic_per_user")

    user_df = df[df['username'] == selected_user]

    if not user_df.empty:
        top_topics = user_df['topic_keywords'].value_counts().reset_index()
        top_topics.columns = ['Topic', 'Total']

        st.subheader(f"Topics Most Discussed by @{selected_user}")
        st.dataframe(top_topics)

        st.bar_chart(top_topics.set_index('Topic'))
    else:
        st.warning("This username does not yet have any topic data.")


    st.header('Tweet Each Keyword')
    df = df.dropna(subset=['topic_keywords', 'full_text'])

    keyword_counts = df['topic_keywords'].value_counts()
    min_count = 3 
    valid_keywords = keyword_counts[keyword_counts >= min_count].index.tolist()

    selected_keywords = st.selectbox("Choose Combination of Keywords", valid_keywords)

    filtered_df = df[df['topic_keywords'] == selected_keywords]


    st.subheader(f"Tweet with Keywords: {selected_keywords}")
    st.write(f"Number of tweets found: {len(filtered_df)}")
    st.dataframe(filtered_df[['username', 'full_text', 'topic_keywords']].reset_index(drop=True))




    