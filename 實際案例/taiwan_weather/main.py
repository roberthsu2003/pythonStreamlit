import requests
import streamlit as st
from datetime import timezone,timedelta,datetime
import csv
import os
import pandas as pd

#中央氣象局天氣預測
#https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=rdec-key-123-45678-011121314&format=JSON

@st.cache_data
def get_csv_filePath():
    #建立時區
    t = timezone(timedelta(hours=8))
    #取得現在時間
    current_datetime = datetime.now(tz=t)
    #建立存檔檔案名稱
    file_name= current_datetime.strftime("%Y%m%d.csv")
    file_absname = f'{os.path.dirname(__file__)}/weather_data/{file_name}'
    return file_absname

@st.cache_data
def parse_json(w)->list:
    location = w['cwbopendata']['dataset']['location']
    weather_list = []
    for item in location:
        city_item = {}
        city_item['城市'] = item['locationName']
        city_item['啟始時間'] = item['weatherElement'][1]['time'][0]['startTime']
        city_item['結束時間'] = item['weatherElement'][1]['time'][0]['endTime']
        city_item['最高溫度'] = float(item['weatherElement'][1]['time'][0]['parameter']['parameterName'])
        city_item['最低溫度'] = float(item['weatherElement'][2]['time'][0]['parameter']['parameterName'])
        city_item['感覺'] = item['weatherElement'][3]['time'][0]['parameter']['parameterName']
        weather_list.append(city_item)
    return weather_list

@st.cache_data
def save_csv(filename,data)->None:
    with open(filename,mode='w',encoding='utf-8',newline='') as file:
        fieldnames = ['城市', '啟始時間','結束時間','最高溫度','最低溫度','感覺']
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def download_save_file(url:str)->None:
    file_path = get_csv_filePath()    
    if not os.path.exists(file_path):
        #沒有這個檔案
        response = requests.get(url)
       
        if response.status_code == 200:
            print("下載成功")
            weather = response.json()
            weatherlist = parse_json(weather)
            save_csv(file_path,weatherlist)




        
        
            
#主程式
url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=rdec-key-123-45678-011121314&format=JSON'
download_save_file(url=url)
filepath = get_csv_filePath()
dataframe = pd.read_csv(filepath)

print(dataframe)
#轉換為datatime型別
dataframe['啟始時間'] = pd.to_datetime(dataframe['啟始時間'])
dataframe['結束時間'] = pd.to_datetime(dataframe['結束時間'])
#改變時間格式
dataframe['啟始時間'] = dataframe['啟始時間'].dt.strftime('%Y-%m-%d-%H:00')
dataframe['結束時間'] = dataframe['結束時間'].dt.strftime('%Y-%m-%d-%H:00')
#改變整數型別
dataframe['最高溫度'] = dataframe['最高溫度'].astype(int)
dataframe['最低溫度'] = dataframe['最低溫度'].astype(int)
st.title('目前天氣預測')
st.dataframe(
    dataframe.style\
    .highlight_max(axis=0,subset=['最高溫度'],color='red')\
    .highlight_min(axis=0,color='lightblue',subset=['最低溫度'])
    ,width=600,height=900)

dataframe = dataframe.set_index('城市')
st.line_chart(dataframe[['最高溫度','最低溫度']])


        