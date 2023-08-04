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

def download_save_file(url)->None:
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
    
 


url = 'https://rate.bot.com.tw/xrt/flcsv/0/day'
download_save_file(url)
st.write(f'台灣銀行牌告匯率 {get_today()}')
df = rates_dataFrame()
st.write(df.T)
       
    


