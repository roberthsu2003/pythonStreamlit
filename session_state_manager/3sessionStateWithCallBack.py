import streamlit as st

st.title("Session State Basic")
"st.session_state object:", st.session_state

def lbs_to_kg():
    st.session_state.kg = st.session_state.lbs/2.2046

def kg_to_lbs():
    st.session_state.lbs = st.session_state.kg * 2.2046

col1, buff, col2 = st.columns([2,1,2])
with col1:
    st.number_input("Pounds:",key='lbs', on_change=lbs_to_kg)

with col2:
    st.number_input("Kilograms:", key="kg", on_change=kg_to_lbs)