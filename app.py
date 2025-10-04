import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Top University Clustering",layout="wide")

st.title('University Dashboard')
st.subheader('Topic: Comparison of Language Manners and Opinion Habits in Top Indonesian Universities Based on X Platform With Text Clustering')
# st.markdown()
st.divider()
file_path_new='all_tweet_virality.csv'

df = pd.read_csv(file_path_new,
                        header= 0)
# Data Clean
clean=pd.read_csv('Data Cleaning/CleanDataFull.csv')
clean_cols = clean[['ID', 'full_text']].copy()
clean_cols = clean_cols.rename(columns={'full_text': 'clean_text'})
df = df.merge(clean_cols, on='ID', how='left')

# Hate
hate=pd.read_csv('hate.csv')
hs_cols = hate.loc[:, 'HS':'Abusive_label'].copy()
hs_cols['ID'] = hate['ID'] 
df= df.merge(hs_cols, on='ID', how='left')
df['HS_label'] = df['HS_label'].map({0: 'non_hate', 1: 'hate'})

# Topik
topik=pd.read_csv('Topik/hasil_topik_per_tweet.csv')
topic_cols = topik.loc[:, 'topic':'topic_keywords'].copy()
topic_cols['ID'] = topik['ID'] 
df= df.merge(topic_cols, on='ID', how='left')


# NER dan Sarkas meragukan
# Sentiment
sentiment=pd.read_csv('hasil_prediksi_sentiment.csv')
sentiment_cols = sentiment.loc[:, 'Predicted':'Predicted Label'].copy()
sentiment_cols['ID'] = sentiment['ID'] 
df= df.merge(sentiment_cols, on='ID', how='left')

# Sarcasm
sarcasm=pd.read_csv('predicted_sarcasm_results.csv')
# st.dataframe(sarcasm)
sarcasm_cols = sarcasm.loc[:, 'sarcasm':'sarcasm_score'].copy()
sarcasm_cols['ID'] = sarcasm['ID'] 
df= df.merge(sarcasm_cols, on='ID', how='left')
# st.dataframe(sarcasm)

# NER
ner=pd.read_csv('NER/hs_entity_per_tweet.csv')
# st.dataframe(ner)
ner['entity_role'] = (ner['entity'].astype(str) + ' - ' + ner['role'].astype(str))

ner_grouped = (
    ner.groupby('ID')['entity_role']
    .apply(lambda x: ', '.join(x.dropna().astype(str)))
    .reset_index()
)

df = df.merge(ner_grouped, on='ID', how='left')

# df.to_csv('final.csv')
# st.dataframe(df)

if "df" not in st.session_state:
    st.session_state['df'] = df

usernames = df['username'].unique()
st.write("""
    General Information of University:
    -  ui_fess= University of Indonesia
    -  UGM_fess= University Gajah Mada
    -  sunib_fess= Bina Nusantara University
    -  ug_fess= Gunadarma University
    -  telyufess= Telkom University
    -  draftanakunpad3= University Padajajaran
""")

st.subheader("Distribution of Tweets per University")

counts  = df['username'].value_counts().sort_index()
total   = counts.sum()
percent = counts / total * 100



per_row = 3
univ_list = counts.index.tolist()


total_tweet = len(df)
st.metric(label="Total Tweets (Overall)", value=total_tweet)
st.markdown('')
for i in range(0, len(univ_list), per_row):
    cols = st.columns(per_row)
    for j, univ in enumerate(univ_list[i:i + per_row]):
        with cols[j]:
            st.markdown(f"<div style='font-size: 16px; font-weight: bold;'>{univ}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 16 px; '>{counts[univ]} tweet</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='color: gray; font-size: 16px;'>{percent[univ]:.1f}%</div>", unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Make the tab labels larger and adjust padding */
    .stTabs [data-baseweb="tab"] {
        font-size: 18px !important;  /* increase font size */
        padding: 12px 24px !important;  /* adjust tab padding */
    }

    /* Optional: make selected tab bold */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        font-weight: bold;
        color: #1E88E5;
    }
    </style>
""", unsafe_allow_html=True)



tabs1, tabs2, tabs3, tabs4, tabs5, tabs6= st.tabs( ["General Information", "Virality", "Topic Modeling", "Sentiment Analysis", "Sarcasm", "Hate"])

with tabs1:
    import page1
    page1.show()
with tabs2:
    import page2
    page2.show()
with tabs3:
    import page3
    page3.show()
with tabs4:
    import page4
    page4.show()
with tabs5:
    import page5
    page5.show()
with tabs6:
    import page6
    page6.show()

