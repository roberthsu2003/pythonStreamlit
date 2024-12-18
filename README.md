# python Streamlit
## 重要觀念
1. streamlit建立的實體,只有layout元件和container元件傳回的是參考
2. 由於第一個觀念,所以streamlit一開始便需要layout
3. 大部份元件(除了layout和container元件),建立後傳出來的並非元件的參考
4. 和使用者互動,會讓所有頁面從上而下重新讀取
5. 由於重新讀取,所有變數資料會消失,要保留資料必需使用st.session來保留資料
6. input元件已經有callback的事件方法,如果使用input元件的callback屬性,元件必需要加入key屬性,callback function透過key屬性來存取使st.session_state.key

## [安裝](./安裝和執行)
## [快速入門](./快速入門/)
## [版面](./版面)
## [session state和callback管理](./session_state_manager)
## [Auto-Refresh](./autorefresh)
## [模擬環境變數](./模擬環境變數)
## 實際案例
- [各種類型圖表顯示](./實際案例/student_scores/)
- [台幣匯率換算](./實際案例/exchange_rate/)
- [台灣天氣預測](./實際案例/taiwan_weather/)
- [股票資訊](./實際案例/finance/)
- [(y=2x-1)機器學習](./實際案例/tansorflow1/)
## [官方專業Demo](https://github.com/streamlit)