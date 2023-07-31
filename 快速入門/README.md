## 快速入門(重要觀念)

### 開發階段
- #### 開啟右上方'Always rerun',達到及時更新
- #### side by side(螢幕左右各開一個視窗,一個為編輯器,一個為browser)

### 程式執行流程
- streamlit的程式流程和一般視窗和後端程式不一樣
- streamlit在以下2程情況會自動更新螢幕畫面(streamlit會由上而下執行所有的程式碼)
	- app的程式碼被更新時
	- 當使用者和工具(widgets)互動時,如使用者按下按鈕

由於以上的特性,使用者和工具互動時,會觸發on_change 或(on_click)的事件，並執行事件的callback function，但後面的程式並還未執行

如果要執行大量的資料,要使用@st.cache_data decorator, 以便app有更好的執行效能。

### 畫面的顯示和資料的修飾