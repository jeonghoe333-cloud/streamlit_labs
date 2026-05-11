import streamlit as st
from datetime import time

st.title('Streamlit 입력 위젯 실습 2')

st.divider()

# 1. 다중 선택박스 퀴즈
st.subheader('1. 다중 선택박스 퀴즈!')

# 커서 뚱뚱하면 (밑에 ovr) insert를 누르면 or 

fruits = st.multiselect(
    'Q1. 과일을 모두 선택하세요 (복수 정답 가능)',
    ['사과', '토마토', '당근', '바나나']
)

correct = {'사과', '토마토', '바나나'}

if set(fruits) == correct: # set 자료형으로 형변환해라
    st.write('완벽해요! 모두 맞았어요~~')
else:
    st.write('틀렸어요ㅠㅠ 다시 선택해보세요')

st.divider()

st.subheader('2. 숫자 슬라이더')
score = st.slider('Your score is ...', 0, 100, 1)

st.text(f'Score : {score}')

st.divider()

st.subheader('3. 시간 범위 슬라이더')

# 시작시간, 종료시간 --> 각각 슬라이더로 입력받는다
start_time, end_time = st.slider(
    'Working time is ...',
    min_value=time(0), max_value=time(23), value=(time(9), time(18)), format='HH:mm'
)

# 선택한 시작 시간과 종료시간을 텍스트로 출력
st.text(f'Working time : {start_time}, {end_time}')

# 이렇게 사용자가 드래그할 수 있는거 : interactive 










# 파이썬, list[] / dictionary {key:value} / 튜플 (,) 수정불가 / 집합 set {}
