## session_state管理和callback function
- #0.84版後,callback的觀念已經加入

### 什麼是session state:
當瀏覽器的一個標籤頁面執行Streamlit的應用程式時,整個streamlit應用程式會產生一個全新的session(當作一張白紙)。streamlit應用程式會由上而下執行所有的程式碼,並且依據程式碼建立session專用的變數。(白紙上記錄資料)

每一次使用者和streamlit應用程式互動時,streamlit清除所有的變數(又變成一張沒有記錄資料的白紙),程式會由上而下再執行一次。所以每次的使用者的互動無法保留原來的變數。

Session state就是一個解決方案,讓每次程式每次由上而下執行時,重要的資訊(重要的記錄)可以儲存在session state內。如下圖表示!

![](./images/pic1.png)

> 附註:當按下瀏覽器的重新整理時,是建立一個全新的Session。當使用者互動時,將現有的Session清空,程式由上而下再執行一次。


### 範例1(lesson1):

```

```


## 參考文件:
- 文章介紹:
	- [Add statefulness to apps 官方說明](https://docs.streamlit.io/library/advanced-features/session-state)
	
	- [Session State for Streamlit](https://blog.streamlit.io/session-state-for-streamlit/)



- 影片介紹:
	- [Session State basic官方說明](https://youtu.be/92jUAXBmZyU?si=acJpTrmuIkcG0XW3)
	
	- [How to use Streamlit session states and callback functions](https://youtu.be/5l9COMQ3acc?si=aRPhivyJN3xdixqk)
