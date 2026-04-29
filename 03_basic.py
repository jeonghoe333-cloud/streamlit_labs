import streamlit as st

# 파이썬 코드
code = '''
import seaborn as sns

iris = sns.load_dataset('iris')
sns.pairplot(data=iris, hue='species', corner=True)
plt.show()
'''

st.code(code, language='javascript')
# 그냥 ''' '''이면 ? 근데 ~~에 ''' '''하면 코드 ! 근데 함수 안에 """ """하면 이건 함수 설명!


# 버튼
def button_write():
    """버튼을 클릭하면 실행되는 함수"""
    st.write('button activated!')




st.button('클릭해보시오', on_click=button_write) # 이벤트               
st.button('Reset', type='primary')                       

st.divider()

if st.button('Reset', type='primary', key='btn1'):
    st.write('Reset clicked!')

if st.button('Cancel', type='secondary', key='btn2'):
    st.write('Cancel clike')
    
if st.button('Ignore', type='tertiary', key='btn3'):
    st.write('Ignore clicked!')