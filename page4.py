# Sentiment Analysis
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

def show():
    df = st.session_state['df']
    st.title('Percentage Distribution of Sentiment')

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
        title="General Sentiment Distribution (Based on Number)",
        hole=0.4
    )

    fig.update_traces(
        textinfo='percent+label',
        hovertemplate='%{label}<br>Total: %{value}<extra></extra>'
    )

    st.plotly_chart(fig)




    # fig = px.bar(
    #     sentiment_df,
    #     x='Sentiment',      
    #     y='Count',          
    #     color='Sentiment',  
    #     text='Count',      
    #     title="General Sentiment Distribution (Based on Number)",
    # )

    # fig.update_traces(
    #     textposition='outside',
    #     hovertemplate='%{x}<br>Total: %{y}<extra></extra>'
    # )

    # fig.update_layout(
    #     yaxis=dict(title='Jumlah Pesan'),
    #     xaxis=dict(title='Sentiment'),
    #     uniformtext_minsize=8,
    #     uniformtext_mode='hide'
    # )

    # st.plotly_chart(fig)

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
            title=f"Sentiment {user}"
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



    # cols = st.columns(3)
    # col_index = 0
    # usernames = df['username'].dropna().unique()

    # for i, user in enumerate(usernames):
    #     user_data = sentiment_by_univ[sentiment_by_univ['username'] == user]

    #     fig = px.bar(
    #         user_data,
    #         x='Predicted Label',       
    #         y='count',               
    #         color='Predicted Label',   
    #         text='count',             
    #         title=f"Sentimen {user}",
    #     )

    #     fig.update_traces(
    #         textposition='outside',
    #         hovertemplate='%{x}<br>Total: %{y}<extra></extra>'
    #     )

    #     fig.update_layout(
    #         yaxis=dict(title='Jumlah Pesan'),
    #         xaxis=dict(title='Sentiment'),
    #         uniformtext_minsize=8,
    #         uniformtext_mode='hide'
    #     )

    #     with cols[col_index]:
    #         st.plotly_chart(fig, use_container_width=True)

    #     col_index = (col_index + 1) % 3


    df = df.dropna(subset=['full_text', 'Predicted Label', 'username'])

    st.title("View Tweets by Sentiment & University")

    selected_univ = st.selectbox("Choose University", sorted(df['username'].dropna().unique()), key="select_univ_sentiment")

    sentiments = df['Predicted Label'].unique()
    selected_sentiment = st.radio("Choose Sentiment", sorted(sentiments), key="selected_sentiment")

    filtered_df = df[
        (df['username'] == selected_univ) &
        (df['Predicted Label'] == selected_sentiment)
    ]

    st.subheader(f"Tweet from {selected_univ} with {selected_sentiment} sentiment")
    st.write(f"Number of tweets found: {len(filtered_df)}")

    st.dataframe(
        filtered_df[['username', 'full_text', 'Predicted Label']].reset_index(drop=True),
        use_container_width=True
    )

    grouped = filtered_df.groupby(['day', 'Predicted Label']).size().reset_index(name='Total Tweet')

    chart = alt.Chart(grouped).mark_bar().encode(
        x=alt.X('day:N', title='Day'),
        y=alt.Y('Total Tweet:Q', title='Total Tweet'),
        color=alt.Color('Predicted Label:N', title='Sentimen'),
        column=alt.Column('Predicted Label:N', title='Sentimen'),
        tooltip=['day:N', 'Predicted Label:N', 'Total Tweet:Q']
    ).properties(
        width=100,
        height=300,
        title="Sentiment Distribution per Day based on Choice"
    ).configure_axisX(
        labelAngle=-45
    )

    st.altair_chart(chart, use_container_width=True)


    grouped = filtered_df.groupby(['hour', 'Predicted Label']).size().reset_index(name='Total Tweet')


    chart = alt.Chart(grouped).mark_bar().encode(
        x=alt.X('hour:O', title='Hour (0–23)'),
        y=alt.Y('Total Tweet:Q', title='Total Tweet'),
        color=alt.Color('Predicted Label:N', title='Sentiment'),
        column=alt.Column('Predicted Label:N', title='Sentiment'),
        tooltip=['hour:O', 'Predicted Label:N', 'Total Tweet:Q']
    ).properties(
        width=100,
        height=300,
        title="Distribution of Tweets per Hour based on Selected Sentiment"
    )

    st.altair_chart(chart, use_container_width=True)