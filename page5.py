# Sarcasm

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

def show():
    df = st.session_state['df']

    sarcasm_counts = df['sarcasm'].value_counts()
    sarcasm_percentages = (sarcasm_counts / sarcasm_counts.sum()) * 100

    sarcasm_df = pd.DataFrame({
        'sarcasm': sarcasm_counts.index,
        'Percentage': sarcasm_percentages.values,
        'Count': sarcasm_counts.values
    })

    fig = px.pie(
        sarcasm_df,
        names='sarcasm',
        values='Count',  
        color='sarcasm',
        title="General Sarcasm Distribution (Based on Number)",
        hole=0.4
    )

    fig.update_traces(
        textinfo='percent+label',
        hovertemplate='%{label}<br>Total: %{value}<extra></extra>'
    )

    st.plotly_chart(fig)

    sarcasm_by_univ = df.groupby(['username', 'sarcasm']).size().reset_index(name='count')
    total_by_univ = df.groupby('username').size().reset_index(name='total')
    sarcasm_by_univ = sarcasm_by_univ.merge(total_by_univ, on='username')
    sarcasm_by_univ['percentage'] = (sarcasm_by_univ['count'] / sarcasm_by_univ['total']) * 100



    cols = st.columns(3)
    col_index = 0
    usernames = df['username'].dropna().unique()
    for i, user in enumerate(usernames):
        user_data = sarcasm_by_univ[sarcasm_by_univ['username'] == user]
        
        fig = px.pie(
            user_data,
            names='sarcasm',
            values='count', 
            color='sarcasm',
            title=f"Sarcasm {user}"
        )
        fig.update_traces(
            textinfo='percent+label',
            hovertemplate='%{label}<br>Total: %{value}<extra></extra>'
        )

        with cols[col_index]:
            st.plotly_chart(fig, use_container_width=True)

        
        col_index += 1
        if col_index == 3:
            cols = st.columns(3)
            col_index = 0



    df = df.dropna(subset=['full_text', 'sarcasm', 'username'])

    st.title("View Tweets based on Sarcasm & University")

    selected_univ = st.selectbox("Choose University", sorted(df['username'].dropna().unique()), key="select_univ_sarcasmt")

    sarcasmts = df['sarcasm'].unique()
    selected_sarcasmt = st.radio("Choose sarcasm or not sarcasm", sorted(sarcasmts), key="selected_sarcasmt")

    filtered_df = df[
        (df['username'] == selected_univ) &
        (df['sarcasm'] == selected_sarcasmt)
    ]

    st.subheader(f"Tweet from {selected_univ} with {selected_sarcasmt} label")
    st.write(f"Total tweets found: {len(filtered_df)}")

    st.dataframe(
        filtered_df[['username', 'full_text', 'sarcasm']].reset_index(drop=True),
        use_container_width=True
    )


  
    sentiment_sarcasm = (
        df.groupby(['sarcasm', 'Predicted Label'])
        .size()
        .reset_index(name='count')
    )

    sentiment_sarcasm['Sarcasm'] = sentiment_sarcasm['sarcasm'].map({'sarcastic': 'Sarcastic', 'not_sarcastic': 'Not Sarcastic'})

    st.subheader("Distribusi Umum Sentimen & Sarkasme")
    st.dataframe(sentiment_sarcasm[['Sarcasm', 'Predicted Label', 'count']])

    fig = px.bar(
        sentiment_sarcasm,
        x='Predicted Label',
        y='count',
        color='Sarcasm',
        barmode='group',
        text='count',
        title="Distribusi Sarkas vs Sentimen (Gabungan Seluruh Tweet)"
    )
    st.plotly_chart(fig)



    st.subheader("Distribusi Sentimen pada Tweet Sarkastik per Universitas")

    sarkas_df = df[df['sarcasm'] == 'sarcastic']

    sentiment_sarcasm_by_user = (
    df.groupby(['username', 'sarcasm', 'Predicted Label'])
    .size()
    .reset_index(name='Count')
)

    sentiment_sarcasm_by_user['Sarcasm'] = sentiment_sarcasm_by_user['sarcasm'].map({
        'sarcastic': 'Sarkas',
        'not_sarcastic': 'Non-Sarkas'
    })

    usernames = sentiment_sarcasm_by_user['username'].unique()
    cols = st.columns(3)
    col_index = 0

    for univ in usernames:
        univ_data = sentiment_sarcasm_by_user[sentiment_sarcasm_by_user['username'] == univ]

        fig = px.bar(
            univ_data,
            x='Predicted Label',
            y='Count',
            color='Sarcasm',
            barmode='group',
            text='Count',
            title=f"Sentimen Tweet Sarkas vs Non-Sarkas - {univ}"
        )

        with cols[col_index]:
            st.plotly_chart(fig, use_container_width=True)

        col_index += 1
        if col_index == 3:
            cols = st.columns(3)
            col_index = 0




    df_sarcasm = df[df['sarcasm'] == 'sarcastic'].copy()

    df_sarcasm['clean_text'] = df_sarcasm['clean_text'].astype(str)

    combined_text = " ".join(df_sarcasm['clean_text'].dropna())

    wordcloud = WordCloud(width=1000, height=500, background_color='white').generate(combined_text)

    st.subheader("WordCloud untuk Sarcasm Tweets")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    universitas_list = df_sarcasm['username'].dropna().unique()

    univ_list = df_sarcasm['username'].dropna().unique()

    per_row = 3
    for i in range(0, len(univ_list), per_row):
        cols = st.columns(per_row)

        for j, univ in enumerate(univ_list[i:i + per_row]):
            with cols[j]:
                univ_texts = df_sarcasm[df_sarcasm['username'] == univ]['clean_text'].dropna()
                combined_text = " ".join(univ_texts.astype(str))

                if combined_text.strip():  # cek tidak kosong
                    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)

                    fig, ax = plt.subplots(figsize=(6, 3))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    ax.set_title(univ, fontsize=12)

                    st.pyplot(fig)
                else:
                    st.write(f"Tidak ada tweet HS untuk {univ}")


    df_hs = df[(df['sarcasm'] == 'sarcastic') & df['entity_role'].notna()].copy()

    df_hs['entity_list'] = df_hs['entity_role'].apply(lambda x: [e.strip() for e in str(x).split(',')])

    df_exp = df_hs.explode('entity_list')
    df_exp = df_exp.rename(columns={'entity_list': 'Entity|Role'})

    entity_user_counts = df_exp.groupby(['username', 'Entity|Role']).size().reset_index(name='Count')
    
    st.subheader("Total Entity Target Sarcasm per Username")
    st.dataframe(entity_user_counts.sort_values(by='Count', ascending=False))