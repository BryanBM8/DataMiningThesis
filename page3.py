# Topic Modeling

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network

def show():

    st.header('Word Cloud Masing-masing Universitas')
    df = st.session_state['df']

    usernames = df['username'].unique()


    selected_user = st.selectbox("Pilih Universitas (username):", usernames, key='wordcloud')
    user_texts = df[df['username'] == selected_user]['clean_text']
    combined_text = " ".join(user_texts.dropna().astype(str))

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(f"Wordcloud untuk {selected_user}")

    st.pyplot(fig)


    
    st.header("Topik Paling Banyak Dibahas di Seluruh Kampus")

    # Drop NaN di kolom topic_keywords
    df = df.dropna(subset=['topic_keywords'])

    # Hitung frekuensi topik
    topik_terbanyak = df['topic_keywords'].value_counts().reset_index()
    topik_terbanyak.columns = ['Topik', 'Jumlah']

    # Tampilkan sebagai tabel
    st.subheader("Daftar Topik Terpopuler")
    st.dataframe(topik_terbanyak)

    # Visualisasi bar chart
    st.subheader("Visualisasi Topik Terpopuler")
    st.bar_chart(topik_terbanyak.set_index('Topik'))


    st.header('Top Topic Keywords Masing-masing Universitas')
    selected_user = st.selectbox("Pilih Username", sorted(usernames), key="topic_per_user")

    user_df = df[df['username'] == selected_user]

    if not user_df.empty:
        top_topics = user_df['topic_keywords'].value_counts().reset_index()
        top_topics.columns = ['Topik', 'Jumlah']

        st.subheader(f"Topik yang Paling Banyak Dibahas oleh @{selected_user}")
        st.dataframe(top_topics)

        st.bar_chart(top_topics.set_index('Topik'))
    else:
        st.warning("Username ini belum memiliki data topik.")


    st.header('Tweet Masing-masing Keywords')
    df = df.dropna(subset=['topic_keywords', 'full_text'])

    keyword_counts = df['topic_keywords'].value_counts()
    min_count = 3 
    valid_keywords = keyword_counts[keyword_counts >= min_count].index.tolist()

    selected_keywords = st.selectbox("Pilih Kombinasi Keywords", valid_keywords)

    filtered_df = df[df['topic_keywords'] == selected_keywords]


    st.subheader(f"Tweet dengan Keywords: {selected_keywords}")
    st.write(f"Jumlah tweet ditemukan: {len(filtered_df)}")
    st.dataframe(filtered_df[['username', 'full_text', 'topic_keywords']].reset_index(drop=True))




    # df = df.dropna(subset=['username', 'topic_keywords'])

    
    # st.title("Graph Keterkaitan User Berdasarkan Topik yang Dibahas")

    # user_keywords = df.groupby("username")["topic_keywords"].apply(lambda x: " ".join(x)).reset_index()

    # vectorizer = TfidfVectorizer()
    # tfidf_matrix = vectorizer.fit_transform(user_keywords["topic_keywords"])

    # cos_sim_matrix = cosine_similarity(tfidf_matrix)

    # threshold = st.slider("Threshold Kedekatan (0-1)", 0.0, 1.0, 0.3)

    # G = nx.Graph()
    # usernames = user_keywords["username"].tolist()
    # G.add_nodes_from(usernames)
    # for i in range(len(usernames)):
    #     for j in range(i+1, len(usernames)):
    #         sim = cos_sim_matrix[i, j]
    #         if sim > threshold:
    #             G.add_edge(usernames[i], usernames[j], weight=sim)

    # net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
    # for node in G.nodes():
    #     net.add_node(node, label=node)
    # for source, target, data in G.edges(data=True):
    #     weight = data["weight"]
    #     color_intensity = int(255 * weight)
    #     color = f"rgb({255 - color_intensity}, {255 - color_intensity}, 255)"
    #     net.add_edge(source, target, value=weight, color=color)

    # net.repulsion(node_distance=200, central_gravity=0.33)
    # net.save_graph("user_similarity_graph.html")
    # components.html(open("user_similarity_graph.html", 'r', encoding='utf-8').read(), height=650)