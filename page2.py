# Virality

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

        Virality Score = (13.5 × Reply Count)
        + (1.5 × Quote Count)
        + (1.0 × Retweet Count)
        + (0.5 × Like Count)

        A higher score indicates a more "viral" tweet.  
        Optionally, the score can be **normalized by follower count** to make comparisons fair between small and large accounts.

        Source: https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md
        """)
    
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
        "quote_count", "reply_count", "retweet_count", "favorite_count", "HS_label", "Predicted Label", "sarcasm"  
    ]

    top_viral_by_univ = (
        df.loc[df.groupby("username")["virality_score"].idxmax()][cols_needed]
        .sort_values(by="virality_score", ascending=False)
        .reset_index(drop=True)
    )

    st.subheader("Most Viral Tweets by University")

    for i, row in top_viral_by_univ.iterrows():
        hs_label_text = "Hate" if row["HS_label"] == 1.0 else "Non Hate"
        with st.expander(f"{i+1}. {row['username']} — Virality Score: {row['virality_score']:.2f}"):
            st.write(row["full_text"])
            st.markdown(
            f"""
            **💬 Reply:** {row['reply_count']} &nbsp;&nbsp;
            **🔁 Retweet:** {row['retweet_count']} &nbsp;&nbsp;
            **❤️ Like:** {row['favorite_count']} &nbsp;&nbsp;
            **🔗 Quote:** {row['quote_count']}  

            ---
            **HS Label:** {hs_label_text}  
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
        df.loc[df["HS_label"].astype(str) == '1.0', cols_needed]
        .sort_values(by="virality_score", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    st.subheader("Top 10 Most Viral Hate Tweets")

    if top_10_hate.empty:
        st.write("Tidak ada tweet dengan label Hate yang memenuhi kriteria.")
    else:
        for i, row in top_10_hate.iterrows():
            hs_label_text = "Hate" if str(row["HS_label"]) == "1.0" else "Non-Hate"
            with st.expander(f"{i+1}. {row['username']} — Virality Score: {row['virality_score']:.2f}"):
                st.write(row["full_text"])
                st.markdown(
                    f"""
                    **💬 Reply:** {row['reply_count']} &nbsp;&nbsp;
                    **🔁 Retweet:** {row['retweet_count']} &nbsp;&nbsp;
                    **❤️ Like:** {row['favorite_count']} &nbsp;&nbsp;
                    **🔗 Quote:** {row['quote_count']}  

                    ---
                    **HS Label:** {hs_label_text}  
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
        st.write("Tidak ada tweet dengan label Sarcasm yang memenuhi kriteria.")
    else:
        for i, row in top_10_sarcasm.iterrows():
            hs_label_text = "Hate" if str(row["HS_label"]) == "1.0" else "Non-Hate"
            with st.expander(f"{i+1}. {row['username']} — Virality Score: {row['virality_score']:.2f}"):
                st.write(row["full_text"])
                st.markdown(
                    f"""
                    **💬 Reply:** {row['reply_count']} &nbsp;&nbsp;
                    **🔁 Retweet:** {row['retweet_count']} &nbsp;&nbsp;
                    **❤️ Like:** {row['favorite_count']} &nbsp;&nbsp;
                    **🔗 Quote:** {row['quote_count']}  

                    ---
                    **HS Label:** {hs_label_text}  
                    **Predicted Sentiment:** {row['Predicted Label']}  
                    **Sarcasm Detected:** {row['sarcasm']}
                    """
                )