# Sentiment Analysis
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

def show():
    df = st.session_state['df']
    st.header('Presentase Persebaran Sentiment')

    sentiment_counts = df['Predicted Label'].value_counts()
    sentiment_percentages = (sentiment_counts / sentiment_counts.sum()) * 100

    sentiment_df = pd.DataFrame({
        'Sentiment': sentiment_counts.index,
        'Percentage': sentiment_percentages.values,
        'Count': sentiment_counts.values
    })

    fig = px.pie(
        sentiment_df,
        names='Sentiment',
        values='Count',  
        color='Sentiment',
        title="Distribusi Sentimen Umum (Berdasarkan Jumlah)",
        hole=0.4
    )

    fig.update_traces(
        textinfo='percent+label',
        hovertemplate='%{label}<br>Jumlah: %{value}<extra></extra>'
    )

    st.plotly_chart(fig)

    sentiment_by_univ = df.groupby(['username', 'Predicted Label']).size().reset_index(name='count')
    total_by_univ = df.groupby('username').size().reset_index(name='total')
    sentiment_by_univ = sentiment_by_univ.merge(total_by_univ, on='username')
    sentiment_by_univ['percentage'] = (sentiment_by_univ['count'] / sentiment_by_univ['total']) * 100



    cols = st.columns(3)
    col_index = 0
    usernames = df['username'].dropna().unique()
    for i, user in enumerate(usernames):
        user_data = sentiment_by_univ[sentiment_by_univ['username'] == user]
        
        fig = px.pie(
            user_data,
            names='Predicted Label',
            values='count', 
            color='Predicted Label',
            title=f"Sentimen {user}"
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


    df = df.dropna(subset=['full_text', 'Predicted Label', 'username'])

    st.title("Lihat Tweet berdasarkan Sentimen & Universitas")

    selected_univ = st.selectbox("Pilih Universitas", sorted(df['username'].dropna().unique()), key="select_univ_sentiment")

    sentiments = df['Predicted Label'].unique()
    selected_sentiment = st.radio("Pilih Sentimen", sorted(sentiments), key="selected_sentiment")

    filtered_df = df[
        (df['username'] == selected_univ) &
        (df['Predicted Label'] == selected_sentiment)
    ]

    st.subheader(f"Tweet dari {selected_univ} dengan sentimen {selected_sentiment}")
    st.write(f"Jumlah tweet ditemukan: {len(filtered_df)}")

    st.dataframe(
        filtered_df[['username', 'full_text', 'Predicted Label']].reset_index(drop=True),
        use_container_width=True
    )

    grouped = filtered_df.groupby(['day', 'Predicted Label']).size().reset_index(name='Jumlah Tweet')

    chart = alt.Chart(grouped).mark_bar().encode(
        x=alt.X('day:N', title='Hari'),
        y=alt.Y('Jumlah Tweet:Q', title='Jumlah Tweet'),
        color=alt.Color('Predicted Label:N', title='Sentimen'),
        column=alt.Column('Predicted Label:N', title='Sentimen'),
        tooltip=['day:N', 'Predicted Label:N', 'Jumlah Tweet:Q']
    ).properties(
        width=100,
        height=300,
        title="Distribusi Sentimen per Hari berdasarkan Pilihan"
    ).configure_axisX(
        labelAngle=-45
    )

    st.altair_chart(chart, use_container_width=True)


    grouped = filtered_df.groupby(['hour', 'Predicted Label']).size().reset_index(name='Jumlah Tweet')


    chart = alt.Chart(grouped).mark_bar().encode(
        x=alt.X('hour:O', title='Jam (0–23)'),
        y=alt.Y('Jumlah Tweet:Q', title='Jumlah Tweet'),
        color=alt.Color('Predicted Label:N', title='Sentimen'),
        column=alt.Column('Predicted Label:N', title='Sentimen'),
        tooltip=['hour:O', 'Predicted Label:N', 'Jumlah Tweet:Q']
    ).properties(
        width=100,
        height=300,
        title="Distribusi Tweet per Jam berdasarkan Sentimen yang Dipilih"
    )

    st.altair_chart(chart, use_container_width=True)