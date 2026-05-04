import streamlit as st

st.title('간단한 streamlit 퀴즈!')

# 1. 체크박스 --> 여러개 동시 선택도 가능하고, 선택을 하나도 안해도 됨!
agree = st.checkbox('Q1. 파이썬은 프로그래밍 언어이다. (맞으면 체크)')

if agree: # 체크를 하면 참, 체크를 안하면 거짓
    st.write('정답입니다!')

st.divider()

# 2. 라디오 버튼 --> 무조건 하나만 꼭 선택해야 함!
person = st.radio(
    'Q2. 당신의 성별은?',
    ['남자', '여자']
)

if person == '남자':
    st.write('당신은 남자입니다')
else : 
    st.write('당신은 여자입니다~')

# 3. 단일 선택박스
transport = st.selectbox(
    'Q3. 가장 빠른 교통수단은?',
    ['기차', '자동차', '비행기', '배']
)

if transport == '비행기':
    st.write('정답~ 비행기가 가장 빠릅니다~')
else :
    st.write('땡! 비행기가 가장 빠릅니다ㅠㅠ')