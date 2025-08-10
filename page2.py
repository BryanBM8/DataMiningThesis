# Virality

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
def show():


    st.markdown("""
        ## How the Virality Score is Calculated

        The **virality score** is designed to identify which tweets are the most impactful or "viral" based on user interactions, such as **replies, quotes, retweets, and likes**.  
        This calculation is based on the **ranking logic of Twitter (X)**, made public in 2023 when parts of their recommendation algorithm were open-sourced — specifically, the engagement weights defined in `ScoredTweetsParam.scala`.

        ### **Theoretical Basis (Twitter/X Algorithm)**

        According to Twitter’s source code:
        - **Replies (comments)** carry the highest weight (around **13.5 points per reply**) because they represent meaningful two-way interaction.
        - **Quote Tweets** (retweets with comments) are weighted higher than regular retweets (around **1.5 points per quote**).
        - **Retweets** are significant signals (around **1.0 point per retweet**).
        - **Likes (Favorites)** are considered weaker signals (around **0.5 points per like**).
        - Other actions (like bookmarks or profile clicks) are also weighted in the original algorithm, but are excluded here as they are not always available in the dataset.

        These weights are **not arbitrary** — they are derived from Twitter’s actual configuration for ranking tweets, as seen in their open-sourced algorithm.

        ### **Virality Score Formula**

        For each tweet:

        Virality Score = (13.5 × Reply Count) + (1.5 × Quote Count) + (1.0 × Retweet Count) + (0.5 × Like Count)

        A higher score indicates a more "viral" tweet.  
        Optionally, the score can be **normalized by follower count** to make comparisons fair between small and large accounts.

        Source: https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md
        """)
    
    df = st.session_state['df']
    usernames = df['username'].unique()
    st.header('Average Virality Score per University')

    viral_avg = (
        df.groupby('username')['virality_score']
        .mean()
        .reset_index()
        .sort_values('virality_score', ascending=False)
    )

    fig = px.bar(
        viral_avg,
        x='username',
        y='virality_score',
        title="Average Virality per University",
        color='virality_score',
        color_continuous_scale='RdBu',
        hover_data={'username': True, 'virality_score': ':.2f'}
    )

    fig.update_layout(
        xaxis_title="University",
        yaxis_title="Average Virality",
        xaxis_tickangle=45
    )

    st.plotly_chart(fig, use_container_width=True)


    st.subheader("Average Virality Score per University (Sarcasm vs Non-Sarcasm)")
    df['Sarcasm'] = df['sarcasm'].map({
        'sarcastic': 'Sarcasm',
        'not_sarcastic': 'Non-Sarcasm'
    })

    virality_sarcasm = (
        df.groupby(['username', 'Sarcasm'])['virality_score']
        .mean()
        .reset_index()
    )

    usernames = virality_sarcasm['username'].unique()
    cols = st.columns(3)
    col_index = 0

    for univ in usernames:
        univ_data = virality_sarcasm[virality_sarcasm['username'] == univ]

        fig = px.bar(
            univ_data,
            x='Sarcasm',
            y='virality_score',
            color='Sarcasm',
            barmode='group',
            text='virality_score',
            title=f"Sarcasm vs Non-Sarcasm - {univ}"
        )

        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(yaxis_title="Average Virality Score", xaxis_title="Category")

        with cols[col_index]:
            st.plotly_chart(fig, use_container_width=True)

        col_index = (col_index + 1) % 3
        if col_index == 0:
            cols = st.columns(3)



    st.subheader("Average Virality Score per University (Hate vs Non-Hate)")

    virality_hate = (
        df.groupby(['username', 'HS_label'])['virality_score']
        .mean()
        .reset_index()
    )

    usernames = virality_hate['username'].unique()
    cols = st.columns(3)
    col_index = 0

    for univ in usernames:
        univ_data = virality_hate[virality_hate['username'] == univ]

        fig = px.bar(
            univ_data,
            x='HS_label',
            y='virality_score',
            color='HS_label',
            barmode='group',
            text='virality_score',
            title=f"Hate vs Non-Hate - {univ}"
        )

        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(yaxis_title="Average Virality Score", xaxis_title="Category")

        with cols[col_index]:
            st.plotly_chart(fig, use_container_width=True)

        col_index = (col_index + 1) % 3
        if col_index == 0:
            cols = st.columns(3)


    st.subheader("Average Virality Score per University (Sentiment)")

    virality_sentiment = (
        df.groupby(['username', 'Predicted Label'])['virality_score']
        .mean()
        .reset_index()
    )

    usernames = virality_sentiment['username'].unique()
    cols = st.columns(3)
    col_index = 0

    for univ in usernames:
        univ_data = virality_sentiment[virality_sentiment['username'] == univ]

        fig = px.bar(
            univ_data,
            x='Predicted Label',
            y='virality_score',
            color='Predicted Label',
            barmode='group',
            text='virality_score',
            title=f"Sentiment - {univ}"
        )

        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(yaxis_title="Average Virality Score", xaxis_title="Category")

        with cols[col_index]:
            st.plotly_chart(fig, use_container_width=True)

        col_index = (col_index + 1) % 3
        if col_index == 0:
            cols = st.columns(3)

    cols_needed = [
        "username", "full_text", "virality_score",
        "quote_count", "reply_count", "retweet_count", "favorite_count", "HS_label", "Predicted Label", "sarcasm"  
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

            ---
            **HS Label:** {row['HS_label']}  
            **Predicted Sentiment:** {row['Predicted Label']}  
            **Sarcasm Detected:** {row['sarcasm']}
            """
        )

    top_20_viral = df.sort_values(by='virality_score', ascending=False).head(20)

    top_20_viral_display = top_20_viral[['username', 'full_text', 'virality_score', 'quote_count', 'reply_count', 'retweet_count', 'favorite_count', "HS_label", "Predicted Label", "sarcasm"]]
    pd.set_option('display.max_colwidth', None)

    st.subheader("Top 20 Most Viral Tweet")
    st.dataframe(top_20_viral_display, use_container_width=True)

    st.header('Top 10 Tweets from Each University')
    selected_user = st.selectbox("Choose University:", usernames)
    top10 = (
        df[df['username'] == selected_user]
        .sort_values(by='virality_score', ascending=False)
        .head(10)
        [['full_text', 'virality_score', 'quote_count', 'reply_count', 'retweet_count', 'favorite_count', "HS_label", "Predicted Label", "sarcasm"]]
        .reset_index(drop=True)
    )

    st.subheader(f" @{selected_user}")
    st.dataframe(top10, use_container_width=True)

    cols_needed = [
    "username", "full_text", "virality_score",
    "quote_count", "reply_count", "retweet_count", "favorite_count",
    "HS_label", "Predicted Label", "sarcasm"
    ]

    top_10_hate = (
        df.loc[df["HS_label"]=='hate', cols_needed]
        .sort_values(by="virality_score", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    st.subheader("Top 10 Most Viral Hate Tweets")

    if top_10_hate.empty:
        st.write("There are no tweets with the label hate that meet the criteria.")
    else:
        for i, row in top_10_hate.iterrows():
            with st.expander(f"{i+1}. {row['username']} — Virality Score: {row['virality_score']:.2f}"):
                st.write(row["full_text"])
                st.markdown(
                    f"""
                    **💬 Reply:** {row['reply_count']} &nbsp;&nbsp;
                    **🔁 Retweet:** {row['retweet_count']} &nbsp;&nbsp;
                    **❤️ Like:** {row['favorite_count']} &nbsp;&nbsp;
                    **🔗 Quote:** {row['quote_count']}  

                    ---
                    **HS Label:** {row['HS_label']}  
                    **Predicted Sentiment:** {row['Predicted Label']}  
                    **Sarcasm Detected:** {row['sarcasm']}
                    """
                )


    cols_needed = [
    "username", "full_text", "virality_score",
    "quote_count", "reply_count", "retweet_count", "favorite_count",
    "HS_label", "Predicted Label", "sarcasm"
    ]

    top_10_sarcasm= (
        df.loc[df["sarcasm"].str.lower() == "sarcastic", cols_needed]
        .sort_values(by="virality_score", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    st.subheader("Top 10 Most Viral Sarcasm Tweets")

    if top_10_sarcasm.empty:
        st.write("There are no tweets with the label Sarcasm that meet the criteria.")
    else:
        for i, row in top_10_sarcasm.iterrows():
            with st.expander(f"{i+1}. {row['username']} — Virality Score: {row['virality_score']:.2f}"):
                st.write(row["full_text"])
                st.markdown(
                    f"""
                    **💬 Reply:** {row['reply_count']} &nbsp;&nbsp;
                    **🔁 Retweet:** {row['retweet_count']} &nbsp;&nbsp;
                    **❤️ Like:** {row['favorite_count']} &nbsp;&nbsp;
                    **🔗 Quote:** {row['quote_count']}  

                    ---
                    **HS Label:** {row['HS_label']}  
                    **Predicted Sentiment:** {row['Predicted Label']}  
                    **Sarcasm Detected:** {row['sarcasm']}
                    """
                )