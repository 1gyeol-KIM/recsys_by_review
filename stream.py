import streamlit as st
import pandas as pd

st.title("리뷰 기반 맛집 추천! in Seoul")

pd.options.display.float_format = '{:.2f}'.format
df = pd.read_csv('seoul/seoul.csv')


dong_selected = st.multiselect(
    '행정동', ['서교동', '종로1.2.3.4가동', '역삼1동']
    )


topic_selected = st.multiselect(
    'Topic', ['음식', '서비스', '가격', '편의성']
    )

# input_user_name = st.text_input(label="User Name", value="default value")
# radio_gender = st.radio(label="Gender", options=["Male", "Female"])
# check_1 = st.checkbox(label="agree", value=False)
# memo = st.text_area(label="memo", value="")

if st.button("Confirm"):
    con = st.container()
    con.caption("Result")
    col_dong = []
    for i in range(len(dong_selected)):
        col_dong.append(dong_selected[i])
    col_topic = []
    for i in range(len(topic_selected)):
        col_topic.append(topic_selected[i])
    

    df_res = df[df['행정동'].isin(dong_selected)]
    st.write(
        df_res.sort_values(by=col_topic, ascending=False)
        )
    # st.write(df['음식'].style.format("{:.2}"))
    # st.dataframe(df['음식'].style.format("{:.2%}"))
    # st.dataframe(df['가격'].style.format("{:.2%}"))
    # st.dataframe(df['서비스'].style.format("{:.2%}"))
    # st.dataframe(df['장소'].style.format("{:.2%}"))
    # con.write(f"User Name is {str(input_user_name)}")
    # con.write(str(radio_gender))
    # con.write(f"agree : {check_1}")
    # con.write(f"memo : {str(memo)}")
