import streamlit as st

st.title("Session State Basics")

"st.session_state object:", st.session_state

## works with all widgets
number = st.slider("A number",1, 10, key="slider") #重要,session_state沒有就初始化,有就更新

st.write(st.session_state)

col1, buff, col2 = st.columns([1,0.5,3]) #columns已經在此建立container

#---------這一段最後寫------------
#-----下面的print()是驗証,當使用者和input widge互動時,程式會由上而下重新執行一次
print("我的下面是button")
next = st.button("Next optin") #button第一次始始化,next初設定為false,按一下,就更改為true
print(next)

if next:
    if st.session_state["radio_option"] == 'a':
        st.session_state.radio_option = 'b'
    elif st.session_state["radio_option"] == 'b':
        st.session_state.radio_option = 'c'
    else:
        st.session_state.radio_option = 'a'
#---------這一段最後寫------------

option_names = ["a", "b", "c"]
option = col1.radio("請選擇1個",option_names,key="radio_option")
st.session_state

if option == 'a':
    col2.write("您選擇的是'a' :smile:")
elif option == 'b':
    col2.write("您選擇的是'b' :heart:")
else:
    col2.write("您選擇是'c' :rocket:")
