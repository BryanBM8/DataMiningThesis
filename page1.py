# Informasi umum

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

def show():
    df = st.session_state['df']

    usernames = df['username'].unique()

   
    # st.dataframe(df, use_container_width=True)

    st.title("Mapping Tweets by Time Based on Hours")

    charts=[]
    for user in usernames:
        user_df = df[df['username'] == user]

        hist = (
            alt.Chart(user_df)
            .mark_bar(color='skyblue')
            .encode(
                x=alt.X('hour:O', bin=alt.Bin(maxbins=24), title='Hour (0-23)'),
                y=alt.Y('count()', title='Total Tweet'),
                tooltip=['hour', 'count()']
            )
            .properties(
                width=250,
                height=200,
                title=f"Tweet Distribution of {user}"
            )
        )
        charts.append(hist)

    for i in range(0, len(charts), 3):
        row = alt.hconcat(*charts[i:i+3]).resolve_scale(y='shared')
        st.altair_chart(row, use_container_width=True)

    st.title('Distribution of Tweets per Day')
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    selected_users = st.multiselect(
        "Choose Username:", usernames, default=list(usernames), 
    key="user_selector"
    )

    selected_days = st.multiselect(
        "Choose Day:", day_order, default=day_order, 
    key="day_selector"
    )

    df_filtered = df[
        (df["username"].isin(selected_users)) &
        (df["day"].isin(selected_days))
    ]

    if df_filtered.empty:
        st.warning("No data matches the selected filter.")
    else:
        bar_chart = (
            alt.Chart(df_filtered)
            .mark_bar()
            .encode(
                x=alt.X('day:N', sort=day_order, title='Day'),
                y=alt.Y('count():Q', title='Total Tweet'),
                color='username:N',
                tooltip=['day', 'username', 'count()']
            )
            .properties(
                width=600,
                height=400,
            )
        )
        st.altair_chart(bar_chart, use_container_width=True)




    # st.title('Distribution of Tweets per Day')
    # day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # selected_users = st.multiselect(
    #     "Choose Username:", usernames, default=list(usernames), 
    #     key="user_selector"
    # )

    # selected_days = st.multiselect(
    #     "Choose Day:", day_order, default=day_order, 
    #     key="day_selector"
    # )

    # df_filtered = df[
    #     (df["username"].isin(selected_users)) &
    #     (df["day"].isin(selected_days))
    # ]

    # if df_filtered.empty:
    #     st.warning("No data matches the selected filter.")
    # else:
    #     line_chart = (
    #         alt.Chart(df_filtered)
    #         .mark_line(point=True)
    #         .encode(
    #             x=alt.X('day:N', sort=day_order, title='Day'),
    #             y=alt.Y('count():Q', title='Total Tweet'),
    #             color='username:N',
    #             tooltip=['day', 'username', 'count()']
    #         )
    #         .properties(
    #             width=600,
    #             height=400,
    #         )
    #     )
    #     st.altair_chart(line_chart, use_container_width=True)

    st.title("Heatmap Tweet Activity")

    heatmap_data = (
        df.groupby(['day', 'hour'])
        .size()
        .reset_index(name='count')
        .pivot_table(index='day', columns='hour', values='count', fill_value=0)
        .stack()
        .reset_index(name='count')
    )

    heatmap_chart = (
        alt.Chart(heatmap_data)
        .mark_rect()
        .encode(
            x=alt.X('hour:O', title='Hour (0–23)'),
            y=alt.Y('day:N', sort=day_order, title='Day'),
            color=alt.Color('count:Q', scale=alt.Scale(scheme='blues')),
            tooltip=['day', 'hour', 'count']
        )
        .properties(
            width=700,
            height=300,
            title="Tweet Activity per Hour & Day"
        )
    )

    st.altair_chart(heatmap_chart, use_container_width=True)
    st.title('Sentiment Distribution per Day')
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day'] = pd.Categorical(df['day'], categories=day_order, ordered=True)

    grouped = df.groupby(['day', 'Predicted Label']).size().reset_index(name='Total Tweet')
    chart = alt.Chart(grouped).mark_bar().encode(
        x=alt.X('day:N', title='Day'),
        y=alt.Y('Total Tweet:Q', title='Total Tweet'),
        color=alt.Color('Predicted Label:N', title='Sentimen'),
        tooltip=['day', 'Predicted Label', 'Total Tweet'],
    ).properties(

    ).configure_axis(
        labelAngle=-45
    ).encode(
        x=alt.X('day:N', sort=day_order),
        column='Predicted Label:N' 
    )

    chart = alt.Chart(grouped).mark_bar().encode(
        x=alt.X('day:N', title='Day', sort=day_order),
        y=alt.Y('Total Tweet:Q', title='Total Tweet'),
        color=alt.Color('Predicted Label:N', title='Sentimen'),
        tooltip=['day', 'Predicted Label', 'Total Tweet']
    )

    chart = chart.encode(
        x=alt.X('day:N', title='Day', sort=day_order),
        y='Total Tweet:Q',
        color='Predicted Label:N'
    ).properties(
        width=600,
        height=400,

    )

    st.altair_chart(chart, use_container_width=True)



    total_counts = df['entity_role'].value_counts().reset_index()
    total_counts.columns = ['entity_role', 'Total Count']

    top_users = (
        df.groupby(['entity_role', 'username'])
        .size()
        .reset_index(name='Count')
        .sort_values(['entity_role', 'Count'], ascending=[True, False])
    )

    top_user_summary = (
        top_users.groupby('entity_role')
        .apply(lambda x: ', '.join(f"{u} ({c})" for u, c in list(zip(x['username'], x['Count']))[:3]))
        .reset_index(name='Top Usernames')
    )

    summary = total_counts.merge(top_user_summary, on='entity_role', how='left')

    st.title("Most Entity Roles (General & Per Username)")
    st.dataframe(summary)
    st.bar_chart(summary.set_index('entity_role')['Total Count'])



    role_counts = df.groupby(['username', 'entity_role']).size().reset_index(name='Count')

    usernames = role_counts['username'].unique()
    selected_user = st.selectbox("Choose Username", usernames)

    filtered = role_counts[role_counts['username'] == selected_user].sort_values(by='Count', ascending=False)

    st.title("Most Entity Role per Username")
    st.subheader(f"Username: {selected_user}")

    st.dataframe(filtered)

    st.bar_chart(filtered.set_index('entity_role')['Count'])
