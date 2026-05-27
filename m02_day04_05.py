# -------------------------------------------
# 1. 라이브러리 불러오기
# -------------------------------------------
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split



# -------------------------------------------
# 2. 한글 폰트 설정 (matplotlib 라이브러리는 한글 지원을 하지 않음)
# -------------------------------------------
# rcParams라는 딕셔너리 설정
matplotlib.rcParams['axes.unicode_minus'] = False  # 음수 기호가 깨지는 것을 방지

# 예외처리
try:
    matplotlib.rcParams['font.family'] = 'Malgun Gothic' # 운영체제가 윈도우인 경우
except Exception:
    matplotlib.rcParams['font.family'] = 'DejaVu Sans' # 운영체제가 맥이나 리눅스인 경우



# -------------------------------------------
# 3. 페이지 기본 설정
# -------------------------------------------
st.set_page_config(
    page_title='광고 플랫폼별 판매량 예측',
    page_icon='💸'
)

st.title('💸 광고 플랫폼별 판매량 예측')
st.caption('Advertising Dataset - 단순/다중 선형 회귀')

st.divider() # 구분선



# -------------------------------------------
# 4. 데이터 불러오기
# -------------------------------------------
df_loaded = pd.read_csv('input/advertising.csv') # \보다는 /가 안전하니까 /로 바꿔주세요

# "Unnamed: 0"과 같은 인덱스 컬럼이 간혹 들어갈 수 있으므로
# 정규표현식 
df = df_loaded.loc[:, ~df_loaded.columns.str.contains(r"^Unnamed")] # 난이도가 조금 있어요...



# -------------------------------------------
# 5. 컬럼 상수 정의 및 데이터 검증
#    * 상수로 분리하는 이유 : 컬럼명을 코드 여러 곳에 문자열로 쓰면 오타를 발견하기 어려움. 상수로 정의하면 한 곳만 수정해도 전체에 반영된다. 주로 대문자+_로 표기!
# -------------------------------------------
FEATURE_COLUMNS = ['TV', 'Radio', 'Newspaper'] # 독립변수(입력값)
TARGET_COLUMN = 'Sales' # 종속변수(예측 대상)



# -------------------------------------------
# 6. 탭 레이아웃
# -------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ['데이터 탐색', '상관관계 분석', '단순 선형 회귀', '다중 선형 회귀']
)

# Tab1 - 데이터 탐색
with tab1:
    st.subheader('데이터셋 미리보기')
    
    st. caption('캐글에서 다운받은 데이터셋 : advertising.csv')

    col_a, col_b, col_c = st.columns(3) # 화면을 가로로 3등분
    col_a.metric('총 데이터 수', f'{len(df):,}개') # metric:숫자카드, :,:천단위 구분기호
    col_b.metric('속성 수', f'{df.shape[1]}개') # 속성 --> 컬럼을 의미 (행, 열)
    col_c.metric('결측치', f'{df.isnull().sum().sum()}개')

    st.markdown('**랜덤 샘플 5개**')
    st.dataframe(df.sample(5), width='stretch')

    st.markdown('**기초 통계량**')
    st.dataframe(df.describe().T, width='stretch') # df.T : 행과 열 전체

    st.markdown('**속성별 분포**')
    fig, axes = plt.subplots(1, 4, figsize=(14, 3)) # 1행 4열 나란히 그래프 배치
    colors = ['#478953', "#8A4249", "#220349", '#667893']
    for ax, col, color in zip(axes, df.columns, colors): # zip() : 튜플로 합치는 함수 --> 각각의 같은 인덱스번호끼리 묶는다
        ax.hist(df[col].dropna(), bins=20, color=color, alpha=0.8, edgecolor='#ffffff')
        # bins:구간, alpha:투명도(1이 100%), edgecolor:테두리선 색
        ax.set_title(col)
        ax.set_xlabel('값')
        ax.set_ylabel('빈도')
    plt.tight_layout() # 차트(서브플롯) 간격 자동 조절
    st.pyplot(fig)
    plt.close(fig) # 메모리에서 차트 삭제 (리소스 낭비 막는다)


# Tab2 - 상관관계 분석
with tab2:
    st.subheader('속성별 상관관계')

    # df.corr() : 피어슨 상관계수 행렬 계산
    # -1 ~ 0 ~ +1  --> 0은 무관, -1은 음의 상관관계, +1은 양의 상관관계
    corr = df.corr(numeric_only=True) # 숫자형 컬럼만 포함

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('**상관계수 행렬**')
        st.dataframe(corr.style.background_gradient(cmap='RdPu').format('{:.3f}'),
                     width='stretch')
        
    with col2:
        st.markdown('**Sales 기준 내림차순 정렬**')
        corr_sort = corr[[TARGET_COLUMN]].sort_values(TARGET_COLUMN, ascending=False)
        st.dataframe(
            corr_sort.style.background_gradient(cmap='YlGn').format("{:.3f}"),
            width='stretch'
        )

    st.markdown('**히트맵**')
    fig2, ax2 = plt.subplots(figsize=(6,4))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdPu', ax=ax2, linewidths=0.5)
    ax2.set_title('Correlation Heatmap')
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)


# Tab3 - 단순 선형 회귀
with tab3:
    st.subheader('단순 선형 회귀 (TV -> Sales)')

    st.markdown('#### 모델 파라미터')
    col_p1, col_p2 = st.columns(2)
    test_size1 = col_p1.slider('테스트 비율', 0.1, 0.5, 0.3, 0.05, key='ts1')
    random_state1 = col_p2.number_input('Random State', 0, 999, 10, key='rs1')

    # 독립변수(입력, feature)와 종속변수(정답, target) 분리
    X1 = df[['TV']]
    y1 = df[TARGET_COLUMN]

    # 훈련/테스트(검증) 데이터 분할
    X_train1, X_test1, y_train1, y_test1 = train_test_split(
        X1, y1, test_size=test_size1, random_state=int(random_state1) # 혹시 정수가 아닐 수도 있으니까 안전하게
    )
 
    # 모델 생성 및 학습
    model1 = LinearRegression()
    model1.fit(X_train1, y_train1)
    y_pred1 = model1.predict(X_test1)

    # 평가지표 계산
    mse1 = mean_squared_error(y_test1, y_pred1) # 평균제곱오차(MSE) / 낮을수록 좋음
    r2_1 = r2_score(y_test1, y_pred1) # R2스코어(결정계수) : 모델이 잘 만들어졌는가? / 높을수록 좋음
    w1 = model1.coef_[0]
    b1 = model1.intercept_

    # 성능 지표 카드
    st.markdown('#### 성능지표')
    m1, m2, m3, m4 = st.columns(4)
    m1.metric('MSE', f'{mse1:.2f}', help='0에 가까울수록 좋음')
    m2.metric('R2 Score', f'{r2_1:.3f}', help='1에 가까울수록 좋음')
    m3.metric('기울기(w)', f'{w1:.4f}')
    m4.metric('절편(b)', f'{b1:.2f}')

    # -------- 여기서부터 복붙 -----------------------------------------------------------------------------------------
    		# ── 그래프 3종 ────────────────────────────────────────────
    # c_idx  : x축에 쓸 인덱스 번호 리스트 [1, 2, 3, ..., n]
    # error1 : 잔차 = 실젯값 - 예측값
    #   잔차가 0 근처에서 특별한 패턴 없이 분포하면 모델이 잘 맞는 편이다.
    c_idx  = list(range(1, len(y_te1) + 1))
    error1 = y_te1.values - y_pred1

    fig4, axes4 = plt.subplots(1, 3, figsize=(15, 4))

    # ① 실젯값 vs 예측값
    #   빨간선(실젯값)과 파란선(예측값)이 얼마나 겹치는지 시각 확인
    axes4[0].plot(c_idx, y_te1.values, color="red",  label="실젯값", linewidth=1.2)
    axes4[0].plot(c_idx, y_pred1,      color="blue", label="예측값",
                  linewidth=1.2, linestyle="--")
    axes4[0].set_title("실젯값 vs 예측값")
    axes4[0].set_xlabel("index")
    axes4[0].set_ylabel("Sales")
    axes4[0].legend()

    # ② 잔차 그래프
    #   axhline(0) : y=0 기준선. 잔차가 이 선 위아래로 고르게 퍼져야 한다.
    axes4[1].plot(c_idx, error1, color="green", linewidth=1.2)
    axes4[1].axhline(0, color="gray", linestyle="--", linewidth=0.8)
    axes4[1].set_title("잔차(Residual)")
    axes4[1].set_xlabel("index")
    axes4[1].set_ylabel("error")

    # ③ 회귀선 그래프
    #   np.linspace로 x 범위 전체를 100등분한 뒤 predict()로 y를 구한다.
    #   → 테스트 데이터(X_te1)를 그대로 쓰면 x값이 섞인 순서라
    #     선이 지그재그로 보일 수 있다.
    #   pd.DataFrame({"TV": x_line}) 으로 감싸는 이유:
    #     model1이 컬럼명이 있는 DataFrame으로 fit됐으므로
    #     같은 형태로 넣어야 feature name 경고가 없다.
    x_line = np.linspace(X1["TV"].min(), X1["TV"].max(), 100)
    y_line = model1.predict(pd.DataFrame({"TV": x_line}))
    axes4[2].scatter(X1["TV"], y1, color="red", s=15, alpha=0.5, label="전체 데이터")
    axes4[2].plot(x_line, y_line, color="blue", linewidth=2, label="회귀선")
    axes4[2].set_title("단순 선형 회귀선")
    axes4[2].set_xlabel("TV 광고비 ($)")
    axes4[2].set_ylabel("Sales")
    axes4[2].legend()

    plt.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)
