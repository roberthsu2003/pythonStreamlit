import csv
import pandas as pd
import streamlit as st
import ffn
import matplotlib.pyplot as plt
import plotly.express as px

st.write("""
# 股票交易價格
""")
@st.cache_data
def getStockNames()->pd.Series:
    '''
    - 取得股票名稱
    - 透過台灣codeSearch.csv檔
    '''
    with open('codeSearch.csv',encoding='utf-8',newline='') as file:
        next(file)
        csv_reader = csv.reader(file)
        stock_codes = {}
        for item in csv_reader:
            key = item[2]
            stock_codes[key] = item[3]
    code_series:pd.Series = pd.Series(stock_codes)
    return code_series

@st.cache_data
def get_dataFrame(menu:list,start_year)->pd.DataFrame:
    stock_data = ffn.get(menu,start=start_year)
    return stock_data

@st.cache_data
def raname_columns_name(dataFrame:pd.DataFrame,mapping:pd.Series) -> pd.DataFrame:
    '''
    欄位名稱改為中文名稱
    '''
    #print(dataFrame.columns.str[:4])
    ser1:pd.Series = mapping[dataFrame.columns.str[:4]]
    dataFrame.columns = ser1.values
    return dataFrame

#多重選取
stockNames:pd.Series = getStockNames()
stock_name_id = stockNames.index.to_numpy() + "_" + stockNames.values #ndArray陣列相加
options = st.sidebar.multiselect('請選擇',
                   stock_name_id,
                   placeholder="股票:"  
                       )
names:list[str] = [] #建立符合ffn需要的股票名稱2330.TW
for name in options: 
    name_string = name.split('_')[0]
    names.append(name_string+".TW")



def display_Data(dataFrame:pd.DataFrame,start_year) -> None:
    '''
    顯示資料
    '''   
    st.subheader(f'{start_year}~目前的歷史資料')  
    st.dataframe(dataFrame)
    st.subheader(f'{start_year}~目前的線圖')
    st.line_chart(dataFrame)
    rebase:pd.DataFrame = dataFrame.rebase()
    st.subheader(f'{start_year}~目前,投資100美金的回報金額')
    st.line_chart(rebase)
    st.subheader(f'{start_year}~目前,報酬分布圖')
    #使用plotly express
    returns = dataFrame.to_returns().dropna()
    for name in returns.columns:        
        figure = px.histogram(returns,x=name)
        st.plotly_chart(figure)
    
    #使用matplotlib figure
    #figure = plt.figure(figsize=(10,5))
    #ax = figure.add_subplot(1,1,1)
    #returns.hist(ax=ax)
    #st.pyplot(figure) 

    
    perf = dataFrame.calc_stats()
    stats = perf.stats
    print(stats)
    stats = stats.loc[['start','end','rf','total_return','cagr','max_drawdown','mtd','three_month','six_month','one_year','three_year','five_year','ten_year']]
    #st.dataframe(stats)
    stats.index = ["起始日期","結束日期","無風險比例","總報酬率","CAGR","最大虧損","持有1個月","持有3個月","持有6個月","持有1年","持有3年","持有5年","持有10年"]
    styler = stats[2:].style.format(precision=3)
    styler.format(lambda v: f'{v*100:.3f}%')
    st.dataframe(styler,height=425)
    


    


 
if len(names) != 0:
    start_year = st.sidebar.selectbox("起始年份",range(2000,2023)) #起始年份選擇
    dataFrame:pd.DataFrame= get_dataFrame(names,f"{start_year}-01-01")
    dataFrame1 = raname_columns_name(dataFrame,stockNames)
    st.sidebar.write("you selected:",start_year)
    display_Data(dataFrame1,start_year)
        



