# Virality

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def show():
    df = st.session_state['df']
    usernames = df['username'].unique()
    st.header('Average Virality Score per University')
    viral_avg = df.groupby('username')['virality_score'].mean().sort_values(ascending=False)
    viral_total = df.groupby('username')['virality_score'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x=viral_avg.index,
        y=viral_avg.values,
        palette="coolwarm",
        ax=ax
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_ylabel("Average Virality")
    ax.set_xlabel("University")
    fig.tight_layout()
    st.pyplot(fig) 



    cols_needed = [
        "username", "full_text", "virality_score",
        "quote_count", "reply_count", "retweet_count", "favorite_count"
    ]

    top_viral_by_univ = (
        df.loc[df.groupby("username")["virality_score"].idxmax()][cols_needed]
        .sort_values(by="virality_score", ascending=False)
        .reset_index(drop=True)
    )

    st.subheader("Most Viral Tweets by University")

    for i, row in top_viral_by_univ.iterrows():
        with st.expander(f"{i+1}. {row['username']} — Virality Score: {row['virality_score']:.2f}"):
            st.write(row["full_text"])
            st.markdown(
                f"""
                **💬 Reply:** {row['reply_count']} &nbsp;&nbsp;
                **🔁 Retweet:** {row['retweet_count']} &nbsp;&nbsp;
                **❤️ Like:** {row['favorite_count']} &nbsp;&nbsp;
                **🔗 Quote:** {row['quote_count']}
                """
            )

    top_20_viral = df.sort_values(by='virality_score', ascending=False).head(20)

    top_20_viral_display = top_20_viral[['username', 'full_text', 'virality_score', 'quote_count', 'reply_count', 'retweet_count', 'favorite_count']]
    pd.set_option('display.max_colwidth', None)

    st.subheader("Top 20 Most Viral Tweet")
    st.dataframe(top_20_viral_display, use_container_width=True)

    st.header('Top 10 Tweets from Each University')
    selected_user = st.selectbox("Choose University:", usernames)
    top10 = (
        df[df['username'] == selected_user]
        .sort_values(by='virality_score', ascending=False)
        .head(10)
        [['full_text', 'virality_score', 'quote_count', 'reply_count', 'retweet_count', 'favorite_count']]
        .reset_index(drop=True)
    )

    st.subheader(f" @{selected_user}")
    st.dataframe(top10, use_container_width=True)

