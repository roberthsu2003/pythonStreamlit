#下面是錯誤的寫法
#每按一次按鈕,一樣是顯示1
#要了解原因必需要學會session_state
import streamlit as st

st.title('Counter Example')
count = 0

increment = st.button('Increment')
if increment:
    count += 1

st.write('Count = ', count)