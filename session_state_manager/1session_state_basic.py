import streamlit as st

st.title("Session State Basics")

"st.session_state object:", st.session_state

if 'a_counter' not in st.session_state: #初始化
    st.session_state['a_counter'] = 0 #只執行一次

if "boolean" not in st.session_state: #初始化
    st.session_state.boolean = False #只執行一次

st.write(st.session_state)

st.write("a_counter is:", st.session_state["a_counter"])
st.write("boolean is:",st.session_state.boolean)

for the_key in st.session_state.keys(): #取出所有session_state的key
    st.write(the_key)

for the_value in st.session_state.values():#取出所有session_state的value
    st.write(the_value)

for item in st.session_state.items():#取出所有session_state的key,value
    item

button = st.button("Update State",key="button") #button第一次始始化,button初設定為false,按一下,就更改為true,未來都是true了

"按button之前",st.session_state


if button:
    st.session_state['a_counter'] += 1
    st.session_state.boolean = not st.session_state.boolean
    "按完按鈕後",st.session_state


#for key in st.session_state.keys(): #清空所有的session_state
#    del st.session_state[key]
#
#st.session_state










