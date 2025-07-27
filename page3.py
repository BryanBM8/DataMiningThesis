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




    docs = [" ".join(keywords) if keywords else "no_keyword" for keywords in df["topic_keywords"]]
    usernames = df["username"].tolist()

    vectorizer = TfidfVectorizer(stop_words=None, token_pattern=r"(?u)\b\w+\b")
    tfidf_matrix = vectorizer.fit_transform(docs)

    similarity_matrix = cosine_similarity(tfidf_matrix)

    G = nx.Graph()

    for user, keywords in zip(usernames, docs):
        G.add_node(user, keywords=keywords)


    threshold = 0.2
    for i, user1 in enumerate(usernames):
        for j, user2 in enumerate(usernames):
            if i < j and similarity_matrix[i, j] > threshold:
                G.add_edge(user1, user2, weight=similarity_matrix[i, j])

    node_weights = {}
    for node in G.nodes():
        weights = [d["weight"] for _, _, d in G.edges(node, data=True)]
        node_weights[node] = sum(weights)/len(weights) if weights else 0


    norm = mcolors.Normalize(vmin=min(node_weights.values()), vmax=max(node_weights.values()))
    colors = {node: norm(value) for node, value in node_weights.items()}
    pos = nx.spring_layout(G, seed=42)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x, node_y, node_text, node_color = [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"{node}<br>Keywords: {G.nodes[node]['keywords']}")
        node_color.append(colors[node])  
    import matplotlib.cm as cm
    cmap = cm.get_cmap("Blues")
    node_color = [f"rgba{cmap(c, bytes=True)}" for c in node_color]
    node_values = [node_weights[node] for node in G.nodes()]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Blues',
            reversescale=True,
            color=node_values,
            size=30,
            colorbar=dict(
                thickness=15,
                title=dict(
                    text='Topic Similarity',
                    side='right'  
                ),
                xanchor='left'
        ),
            line_width=2
        ),
        hovertext=node_text
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='User Topic Similarity Network',
                        title_x=0.5,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0,l=0,r=0,t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    ))

    st.title("User Topic Similarity Graph")
    st.plotly_chart(fig, use_container_width=True)