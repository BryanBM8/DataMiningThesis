# Informasi umum

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

def show():
    df = st.session_state['df']

    usernames = df['username'].unique()

    st.title("Pembagian Tweet per Universitas")
    if 'username' not in df.columns:
        st.error("Kolom 'univ' tidak ditemukan.")
        st.stop()

    counts  = df['username'].value_counts().sort_index()
    total   = counts.sum()
    percent = counts / total * 100



    per_row = 3
    univ_list = counts.index.tolist()

    for i in range(0, len(univ_list), per_row):
        cols = st.columns(per_row)
        for j, univ in enumerate(univ_list[i:i + per_row]):
            with cols[j]:
                st.markdown(f"<div style='font-size: 32px; font-weight: bold;'>{univ}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size: 16 px; '>{counts[univ]} tweet</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: gray; font-size: 16px;'>{percent[univ]:.1f}%</div>", unsafe_allow_html=True)


    st.markdown('')
    # st.dataframe(df, use_container_width=True)

    st.title("Pemetaan Waktu Tweet Berdasarkan Jam")

    charts=[]
    for user in usernames:
        user_df = df[df['username'] == user]

        hist = (
            alt.Chart(user_df)
            .mark_bar(color='skyblue')
            .encode(
                x=alt.X('hour:O', bin=alt.Bin(maxbins=24), title='Jam (0-23)'),
                y=alt.Y('count()', title='Jumlah Tweet'),
                tooltip=['hour', 'count()']
            )
            .properties(
                width=250,
                height=200,
                title=f"Distribusi Jam Tweet: {user}"
            )
        )
        charts.append(hist)

    for i in range(0, len(charts), 3):
        row = alt.hconcat(*charts[i:i+3]).resolve_scale(y='shared')
        st.altair_chart(row, use_container_width=True)

    st.title('Distribusi Tweet Per Hari')
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    selected_users = st.multiselect(
        "Pilih Username:", usernames, default=list(usernames), 
    key="user_selector"
    )

    selected_days = st.multiselect(
        "Pilih Hari:", day_order, default=day_order, 
    key="day_selector"
    )

    df_filtered = df[
        (df["username"].isin(selected_users)) &
        (df["day"].isin(selected_days))
    ]

    if df_filtered.empty:
        st.warning("Tidak ada data yang cocok dengan filter yang dipilih.")
    else:
        bar_chart = (
            alt.Chart(df_filtered)
            .mark_bar()
            .encode(
                x=alt.X('day:N', sort=day_order, title='Hari'),
                y=alt.Y('count():Q', title='Jumlah Tweet'),
                color='username:N',
                tooltip=['day', 'username', 'count()']
            )
            .properties(
                width=600,
                height=400,
            )
        )
        st.altair_chart(bar_chart, use_container_width=True)


    st.title("Heatmap Aktivitas Tweet")

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
            x=alt.X('hour:O', title='Jam (0–23)'),
            y=alt.Y('day:N', sort=day_order, title='Hari'),
            color=alt.Color('count:Q', scale=alt.Scale(scheme='blues')),
            tooltip=['day', 'hour', 'count']
        )
        .properties(
            width=700,
            height=300,
            title="Aktivitas Tweet per Jam & Hari"
        )
    )

    st.altair_chart(heatmap_chart, use_container_width=True)
    st.title('Distribusi Sentimen Per Hari')
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['day'] = pd.Categorical(df['day'], categories=day_order, ordered=True)

    grouped = df.groupby(['day', 'Predicted Label']).size().reset_index(name='Jumlah Tweet')
    chart = alt.Chart(grouped).mark_bar().encode(
        x=alt.X('day:N', title='Hari'),
        y=alt.Y('Jumlah Tweet:Q', title='Jumlah Tweet'),
        color=alt.Color('Predicted Label:N', title='Sentimen'),
        tooltip=['day', 'Predicted Label', 'Jumlah Tweet'],
    ).properties(

    ).configure_axis(
        labelAngle=-45
    ).encode(
        x=alt.X('day:N', sort=day_order),
        column='Predicted Label:N' 
    )

    chart = alt.Chart(grouped).mark_bar().encode(
        x=alt.X('day:N', title='Hari', sort=day_order),
        y=alt.Y('Jumlah Tweet:Q', title='Jumlah Tweet'),
        color=alt.Color('Predicted Label:N', title='Sentimen'),
        tooltip=['day', 'Predicted Label', 'Jumlah Tweet']
    )

    chart = chart.encode(
        x=alt.X('day:N', title='Hari', sort=day_order),
        y='Jumlah Tweet:Q',
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

    st.title("Entity Role Terbanyak (Umum & Per Username)")
    st.dataframe(summary)
    st.bar_chart(summary.set_index('entity_role')['Total Count'])



    role_counts = df.groupby(['username', 'entity_role']).size().reset_index(name='Count')

    usernames = role_counts['username'].unique()
    selected_user = st.selectbox("Pilih Username", usernames)

    filtered = role_counts[role_counts['username'] == selected_user].sort_values(by='Count', ascending=False)

    st.title("Entity Role Terbanyak per Username")
    st.subheader(f"Username: {selected_user}")

    st.dataframe(filtered)

    st.bar_chart(filtered.set_index('entity_role')['Count'])
