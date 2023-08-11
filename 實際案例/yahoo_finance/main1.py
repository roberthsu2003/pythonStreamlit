from FinMind.data import DataLoader
import streamlit as st

st.write("""
# 簡易股票價格
台積電股票價格
""")

stock_no = '2330'
dl = DataLoader()
stock_data = dl.taiwan_stock_daily(stock_id=stock_no, start_date='2000-01-01')

st.line_chart(stock_data,x='date',y='close')
st.line_chart(stock_data,x='date',y='Trading_Volume')