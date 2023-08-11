import csv
import pandas as pd
import streamlit as st
import ffn

st.write("""
# 股票交易價格
""")
@st.cache_data
def getStockNames()->pd.Series:
    with open('codeSearch.csv',encoding='utf-8',newline='') as file:
        next(file)
        csv_reader = csv.reader(file)
        stock_codes = {}
        for item in csv_reader:
            key = item[2]
            stock_codes[key] = item[3]
    code_series = pd.Series(stock_codes)
    return code_series

def get_dataFrame(menu:list,start_year)->pd.DataFrame:
    stock_data = ffn.get(menu,start=start_year)
    return stock_data

#多重選取
stockNames = getStockNames()
stock_name_id = stockNames.index.to_numpy() + "_" + stockNames.values
options = st.sidebar.multiselect('請選擇',
                   stock_name_id,
                   placeholder="股票:"  
                       )
names = []
for name in options:
    name_string = name.split('_')[0]
    names.append(name_string+".TW")

dataFrame:pd.DataFrame | None = None
if len(names) != 0:    
    #start year
    start_year = st.sidebar.selectbox("起始年份",range(2000,2023))
    st.sidebar.write("you selected:",start_year)
    print(start_year)
    dataFrame = get_dataFrame(names,f"{start_year}-01-01")
    st.dataframe(dataFrame)
    st.line_chart(dataFrame)



