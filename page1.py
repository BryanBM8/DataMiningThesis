import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def show():
    file_path_new='all_tweet_virality.csv'

    df = pd.read_csv(file_path_new,
                            header= 0)

    usernames = df['username'].unique()

    st.title("Pembagian Tweet per Universitas")
    if 'username' not in df.columns:
        st.error("Kolom 'univ' tidak ditemukan.")
        st.stop()

    counts  = df['username'].value_counts().sort_index()
    total   = counts.sum()
    percent = counts / total * 100


    st.subheader("Statistik per Universitas")
    per_row = 3
    univ_list = counts.index.tolist()

    for i in range(0, len(univ_list), per_row):
        cols = st.columns(per_row)
        for j, univ in enumerate(univ_list[i:i + per_row]):
            with cols[j]:
                st.metric(
                    label=univ,
                    value=f"{counts[univ]} tweet",
                    delta=f"{percent[univ]:.1f}%",
                    delta_color="normal"
                )

    st.dataframe(df, use_container_width=True)

    st.title("Pemetaan Waktu Tweet Berdasarkan Jam")

    cols = st.columns(2)
    col_idx = 0

    for user in usernames:
        fig, ax = plt.subplots()
        sns.histplot(
            df[df['username'] == user]['hour'],
            bins=24,
            kde=False,
            color='skyblue',
            ax=ax
        )
        ax.set_title(f"Distribusi Jam Tweet: {user}")
        ax.set_xlabel("Jam")
        ax.set_ylabel("Jumlah Tweet")
        ax.set_xticks(range(0, 24, 2))
        ax.set_xlim(0, 23)
        cols[col_idx].pyplot(fig)
        col_idx = (col_idx + 1) % len(cols)


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
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.countplot(
            data=df_filtered,
            x='day',
            order=day_order,
            hue='username',
            ax=ax
        )
        ax.set_title("Distribusi Tweet per Hari")
        ax.set_xlabel("Hari")
        ax.set_ylabel("Jumlah Tweet")
        ax.tick_params(axis='x', rotation=45)

        st.pyplot(fig)

    heat = (
        df
        .pivot_table(
            index='day',
            columns='hour',
            values='username',   
            aggfunc='size',
            fill_value=0
        )
        .reindex(index=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
                columns=range(24), fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(
        heat,
        cmap='Blues',          
        linewidths=.5,
        linecolor='white',
        cbar_kws={'label': 'Jumlah Tweet'},
        ax=ax
    )
    ax.set_title("Aktivitas Tweet per Jam & Hari")
    ax.set_xlabel("Jam (0‑23)")
    ax.set_ylabel("Hari")

    st.pyplot(fig)


