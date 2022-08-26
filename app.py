import streamlit as st
import pandas as pd
import time
import os
from src import model


st.title("리뷰 기반 맛집 추천 in Seoul")

st.subheader("음식점 리뷰 감성 분석하기")

input = st.text_area(
    label='입력', key='review',
    help="'로 구분해서 입력해주세요. (예시) '리뷰', '리뷰', ..."
    )

if st.button('결과 보기'):
    input_list = input.split("',")
    prob_list, processed_review, score_list, total_score_list = model.inference_model(input_list)

    st.write('**Score per Topics**')
    df = pd.DataFrame(
        [total_score_list],
        columns=['서비스', '음식', '장소', '가격']
    )
    st.write(df)

    st.write('**raw data**')
    df_raw = pd.DataFrame({
        '리뷰':input_list,
        'prob in topics(서비스, 음식, 장소, 가격)': prob_list,
        'tokenized': processed_review,
        'senti score': score_list
    })
    df_raw = df_raw.astype(str)
    st.write(df_raw)

st.write("""
---
""")

st.subheader("우리 동네 맛집 리스트")

f_path = 'data/'
df = pd.read_pickle(os.path.join(f_path, "seoul.pkl"))
dong_selected = st.multiselect(
    '동네', ['서교동', '종로1.2.3.4가동', '역삼1동']
    )
topic_selected = st.multiselect(
    'Topic', ['음식', '서비스', '가격', '편의성']
    )

if st.button("보기"):
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





# # 입력 값 받기
# if btn_clicked:
#     con = st.container()
#     con.caption("Result")
#     if not str(input_user_name):
#         con.error("리뷰데이터를 형식에 맞춰 입력해주세요. ")
#     else:
#         # error 안 났을 경우 inference
#         con.write(f"Hello~ {str(input_user_name)}")