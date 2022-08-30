import streamlit as st
import pandas as pd
import time
import os
from src import model


st.title("리뷰 기반 맛집 추천 in Seoul")

st.subheader("음식점 리뷰 감성 분석하기")

input = st.text_area(value="'파채가 비싼감이 없지 않지만 안시킬수 없는 양갈비와 같이 먹기 딱이에요. 갓피클 깻잎이랑 함께 먹음 덜 느끼하고 맛나요 예약필수!', '마스크 안쓰고ㅠㅠ 안에 요리하시는 분 머리카락이 선풍기 바람에 날리는데 맛은 있는데 조금 찝찝하네요.. 다음엔 안올것 같아요..','직원분들 사장님 모두 친절하시고 변함없는 맛 :-) 강추합니다!!', '가격대비 맛과 친절함이 좋은 곳! 해동최고! 내년이 개업 30주년인 역사와 전통이 있는 곳'",
    label='입력', key='review',
    help="'로 구분해서 입력해주세요. (예시) '리뷰', '리뷰', ...", 
    max_chars=1000
    )

if st.button('결과 보기'):
    input_list = input.split("',")
    prob_list, processed_review, score_list, total_score_list = model.inference_model(input_list)

    st.write('**Score per Topics**')
    df = pd.DataFrame(
        [total_score_list],
        columns=['서비스', '음식', '편의성', '가격']
    )
    st.write(df)

    st.write('**raw data**')
    df_raw = pd.DataFrame({
        '리뷰':input_list,
        'prob in topics(서비스, 음식, 편의성, 가격)': prob_list,
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
    '동네', ['서교동', '종로1.2.3.4가동', '역삼1동'],
    help="서울 전체 행정동으로 확대 예정", 
    )
topic_selected = st.multiselect(
    'Topic', ['음식', '서비스', '가격', '편의성'],
    help="선호하는 토픽순으로 클릭"
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


st.write("""
---
""")


st.subheader("(구현 예정) 내가 좋아하는 맛집과 비슷한 추천 맛집은?")



# # 입력 값 받기
# if btn_clicked:
#     con = st.container()
#     con.caption("Result")
#     if not str(input_user_name):
#         con.error("리뷰데이터를 형식에 맞춰 입력해주세요. ")
#     else:
#         # error 안 났을 경우 inference
#         con.write(f"Hello~ {str(input_user_name)}")