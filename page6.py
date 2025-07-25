# Hate

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
from collections import Counter

def show():
    df = st.session_state['df']
    df['HS_label'] = df['HS_label'].replace({1: 'hate', 0: 'non_hate'})
    hate_counts = df['HS_label'].value_counts()
    hate_percentages = (hate_counts / hate_counts.sum()) * 100

    hate_df = pd.DataFrame({
        'hate': hate_counts.index,
        'Percentage': hate_percentages.values,
        'Count': hate_counts.values
    })

    fig = px.pie(
        hate_df,
        names='hate',
        values='Count',  
        color='hate',
        title="Distribusi hate Umum (Berdasarkan Jumlah)",
        hole=0.4
    )

    fig.update_traces(
        textinfo='percent+label',
        hovertemplate='%{label}<br>Jumlah: %{value}<extra></extra>'
    )

    st.plotly_chart(fig)

    hate_by_univ = df.groupby(['username', 'HS_label']).size().reset_index(name='count')
    total_by_univ = df.groupby('username').size().reset_index(name='total')
    hate_by_univ = hate_by_univ.merge(total_by_univ, on='username')
    hate_by_univ['percentage'] = (hate_by_univ['count'] / hate_by_univ['total']) * 100



    cols = st.columns(3)
    col_index = 0
    usernames = df['username'].dropna().unique()
    for i, user in enumerate(usernames):
        user_data = hate_by_univ[hate_by_univ['username'] == user]
        
        fig = px.pie(
            user_data,
            names='HS_label',
            values='count', 
            color='HS_label',
            title=f"hate {user}"
        )
        fig.update_traces(
            textinfo='percent+label',
            hovertemplate='%{label}<br>Jumlah: %{value}<extra></extra>'
        )

        with cols[col_index]:
            st.plotly_chart(fig, use_container_width=True)

        
        col_index += 1
        if col_index == 3:
            cols = st.columns(3)
            col_index = 0

    df = df.dropna(subset=['full_text', 'HS_label', 'username'])

    st.title("Lihat Tweet berdasarkan Hate & Universitas")

    selected_univ = st.selectbox("Pilih Universitas", sorted(df['username'].dropna().unique()), key="select_univ_hate")

    hates = df['HS_label'].unique()
    selected_hate = st.radio("Pilih hate", sorted(hates), key="selected_hate")

    filtered_df = df[
        (df['username'] == selected_univ) &
        (df['HS_label'] == selected_hate)
    ]

    st.subheader(f"Tweet dari {selected_univ} dengan {selected_hate}")
    st.write(f"Jumlah tweet ditemukan: {len(filtered_df)}")

    st.dataframe(
        filtered_df[['username', 'full_text', 'HS_label']].reset_index(drop=True),
        use_container_width=True
    )


    hate_sarcasm = (
        df.groupby(['sarcasm', 'HS_label'])
        .size()
        .reset_index(name='count')
    )

    hate_sarcasm['Sarcasm'] = hate_sarcasm['sarcasm'].map({'sarcastic': 'Sarcastic', 'not_sarcastic': 'Not Sarcastic'})

    st.subheader("Distribusi Umum Hate & Sarkasme")
    st.dataframe(hate_sarcasm[['Sarcasm', 'HS_label', 'count']])

    fig = px.bar(
        hate_sarcasm,
        x='HS_label',
        y='count',
        color='Sarcasm',
        barmode='group',
        text='count',
        title="Distribusi Sarkas vs Hate (Gabungan Seluruh Tweet)"
    )
    st.plotly_chart(fig)



    st.subheader("Distribusi Hate pada Tweet Sarkastik per Universitas")

    sarkas_df = df[df['sarcasm'] == 'sarcastic']

    hate_sarcasm_by_user = (
    df.groupby(['username', 'sarcasm', 'HS_label'])
    .size()
    .reset_index(name='Count')
)

    hate_sarcasm_by_user['Sarcasm'] = hate_sarcasm_by_user['sarcasm'].map({
        'sarcastic': 'Sarkas',
        'not_sarcastic': 'Non-Sarkas'
    })

    usernames = hate_sarcasm_by_user['username'].unique()
    cols = st.columns(3)
    col_index = 0

    for univ in usernames:
        univ_data = hate_sarcasm_by_user[hate_sarcasm_by_user['username'] == univ]

        fig = px.bar(
            univ_data,
            x='HS_label',
            y='Count',
            color='Sarcasm',
            barmode='group',
            text='Count',
            title=f"Hate Tweet Sarkas vs Non-Sarkas - {univ}"
        )

        with cols[col_index]:
            st.plotly_chart(fig, use_container_width=True)

        col_index += 1
        if col_index == 3:
            cols = st.columns(3)
            col_index = 0

    df_hs = df[df['HS_label'] == 'hate'].copy()

    df_hs['clean_text'] = df_hs['clean_text'].astype(str)

    combined_text = " ".join(df_hs['clean_text'].dropna())

    wordcloud = WordCloud(width=1000, height=500, background_color='white').generate(combined_text)

    st.subheader("WordCloud untuk Hate Speech Tweets")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

    universitas_list = df_hs['username'].dropna().unique()

    univ_list = df_hs['username'].dropna().unique()

    per_row = 3
    for i in range(0, len(univ_list), per_row):
        cols = st.columns(per_row)

        for j, univ in enumerate(univ_list[i:i + per_row]):
            with cols[j]:
                univ_texts = df_hs[df_hs['username'] == univ]['clean_text'].dropna()
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


    df_hs = df[(df['HS_label'] == 'hate') & df['entity_role'].notna()].copy()

    df_hs['entity_list'] = df_hs['entity_role'].apply(lambda x: [e.strip() for e in str(x).split(',')])

    df_exp = df_hs.explode('entity_list')
    df_exp = df_exp.rename(columns={'entity_list': 'Entity|Role'})

    entity_user_counts = df_exp.groupby(['username', 'Entity|Role']).size().reset_index(name='Count')
    
    st.subheader("Jumlah Entity Target Hate Speech per Username")
    st.dataframe(entity_user_counts.sort_values(by='Count', ascending=False))