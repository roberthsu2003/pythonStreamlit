import requests
import os
import streamlit as st
from datetime import datetime,timezone,timedelta
import pandas as pd
#台灣銀行牌告匯率下載csv網址
# https://rate.bot.com.tw/xrt/flcsv/0/day

@st.cache_data
def get_today() -> str:
    #建立時區
    t = timezone(timedelta(hours=8))
    #取得現在時間
    current_datetime = datetime.now(tz=t)
    #建立存檔檔案名稱
    today_str = current_datetime.strftime("%Y-%m-%d")
    return today_str

@st.cache_data
def get_csv_filePath() -> str:
    #建立時區
    t = timezone(timedelta(hours=8))
    #取得現在時間
    current_datetime = datetime.now(tz=t)
    #建立存檔檔案名稱
    file_name= current_datetime.strftime("%Y%m%d.csv")
    file_absname = f'{os.path.dirname(__file__)}/rates_data/{file_name}'
    return file_absname

def download_save_file(url:str)->None:
    file_path = get_csv_filePath()
    if not os.path.exists(file_path):
        #沒有這個檔案
        response = requests.get(url)
        encoding = response.encoding
        if response.status_code == 200:
            with open(file_path,mode='w',encoding=encoding,newline='') as file:
                file.write(response.text)

@st.cache_data
def rates_dataFrame() -> pd.DataFrame:
    file_path = get_csv_filePath()
    df = pd.read_csv(file_path)
    right_df = df[['匯率','匯率.1']]
    right_df.columns = ['買進','賣出']
    return right_df

@st.cache_data
def get_rate(df:pd.DataFrame) -> pd.Series:
    list_s = pd.Series({'USD':'美金','HKD':'港幣','GBP':'英鎊','CAD':'加拿大幣',
     'SGD':'新加坡幣','CHF':'瑞士法郎','JPY':'日圓','ZAR':'南非幣',
     'SEK':'瑞典幣','NDZ':'紐元','THB':'泰幣','PHP':'菲國比索','IDR':'印尼幣',
     'EUR':'歐元','KRW':'韓元','VND':'越南盾','MYR':'馬來幣','CNY':'人民幣'
     })
    
    return list_s.apply(lambda val: val+ list_s[list_s == val].index[0])
    
 


url = 'https://rate.bot.com.tw/xrt/flcsv/0/day'
download_save_file(url)
st.write(f'台灣銀行牌告匯率 {get_today()}')
df = rates_dataFrame()
st.write(df.T)

#sidebar
st.sidebar.title("台幣匯率換算")
st.sidebar.divider()
add_radio = st.sidebar.radio(
    "試算方式:",
    ("買入","賣出")
)

st.sidebar.divider()

add_selectbox = st.sidebar.selectbox(
    "請選擇貨幣:",
    get_rate(df)
)
st.sidebar.divider()
if add_radio == '買入':
    st.sidebar.write('買入'+add_selectbox[-3:])
    num = st.sidebar.number_input("",0)
    nt_dallar = df['賣出'][add_selectbox[-3:]] * num
    st.sidebar.write(f'買入{add_selectbox[-3:]}需要{round(nt_dallar,ndigits=2)}台幣')
else:
    st.sidebar.write('賣出'+add_selectbox[-3:])
    num = st.sidebar.number_input("",0)
    nt_dallar = df['買進'][add_selectbox[-3:]] * num
    st.sidebar.write(f'賣出{add_selectbox[-3:]}可得{round(nt_dallar,ndigits=2)}台幣')

print(df)








    


