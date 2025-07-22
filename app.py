import streamlit as st
import pandas as pd
st.set_page_config(page_title="Dashboard Top University Clustering")


st.title('COMPARISON OF LANGUAGE MANNERS AND OPINION HABITS IN TOP INDONESIAN UNIVERSITIES BASED ON X PLATFORM WITH TEXT CLUSTERING')
file_path_new='all_tweet_virality.csv'

df = pd.read_csv(file_path_new,
                        header= 0)

hate=pd.read_csv('hate.csv')
# st.dataframe(hate)
topik=pd.read_csv('topik/hasil_topik_per_tweet.csv')
# st.dataframe(topik)

# Belum ada NER dan Sarkas

sentiment=pd.read_csv('hasil_prediksi_sentiment.csv')
# st.dataframe(sentiment)

hs_cols = hate.loc[:, 'HS':'HS_Strong_label'].copy()
hs_cols['ID'] = hate['ID'] 

df= df.merge(hs_cols, on='ID', how='left')

topic_cols = topik.loc[:, 'topic':'topic_keywords'].copy()
topic_cols['ID'] = topik['ID'] 

df= df.merge(topic_cols, on='ID', how='left')

sentiment_cols = sentiment.loc[:, 'Predicted':'Predicted Label'].copy()
sentiment_cols['ID'] = sentiment['ID'] 

df= df.merge(sentiment_cols, on='ID', how='left')

st.dataframe(df)

# if "df" not in st.session_state:
#     st.session_state.df = None
#     st.session_state.risk1=None
#     st.session_state.signifikan1=None
#     st.session_state.signifikan2=None
#     st.session_state.id=None

tabs1, tabs2, tabs3, tabs4= st.tabs( ["Informasi Umum", "Virality", "Topic Modeling", "Sentiment Analysis"])

with tabs1:
    import page1
    page1.show()
with tabs2:
    # import page1
    # page1.show()
    import page2
    page2.show()
with tabs3:
    st.write('To be develop')
with tabs4:
    st.write('To be develop')
    # import page1
    # page1.show()
#     import modules.page3 as page3
#     page3.show()
