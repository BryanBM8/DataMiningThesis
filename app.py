import streamlit as st
st.set_page_config(page_title="Dashboard Top University Clustering", layout="wide")


st.title('COMPARISON OF LANGUAGE MANNERS AND OPINION HABITS IN TOP INDONESIAN UNIVERSITIES BASED ON X PLATFORM WITH TEXT CLUSTERING')

# if "df" not in st.session_state:
#     st.session_state.df = None
#     st.session_state.risk1=None
#     st.session_state.signifikan1=None
#     st.session_state.signifikan2=None
#     st.session_state.id=None

tabs1, tabs2, tabs3= st.tabs( ["Informasi Umum", "Topic Modeling", "Sentiment Analysis"])

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
    # import page1
    # page1.show()
#     import modules.page3 as page3
#     page3.show()
