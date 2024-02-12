#0.84版後,callback的觀念已經加入,session_state的管理就不再這麼重要了
import streamlit as st
st.title("session State Basics")
"st.session_state object:", st.session_state

if 'a_counter' not in st.session_state:
    st.session_state['a_counter'] = 0

if 'boolean' not in st.session_state:
    st.session_state.boolean = False

st.write(st.session_state)

st.write("a_counter is:",st.session_state['a_counter'])
st.write("boolean is:",st.session_state.boolean)

for item in st.session_state.items():
    item

button = st.button("update State",key='btn')
"before pressing button", st.session_state

if button:
    st.session_state['a_counter'] += 1
    st.session_state.boolean = not st.session_state.boolean
    "after pressing button", st.session_state