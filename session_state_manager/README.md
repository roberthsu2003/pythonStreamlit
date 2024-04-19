## session_state管理和callback function
- #0.84版後,callback的觀念已經加入

### 什麼是session state:
當瀏覽器的一個標籤頁面執行Streamlit的應用程式時,整個streamlit應用程式會產生一個全新的session(當作一張白紙)。streamlit應用程式會由上而下執行所有的程式碼,並且依據程式碼建立session專用的變數。(白紙上記錄資料)

每一次使用者和streamlit應用程式互動時,streamlit清除所有的變數(又變成一張沒有記錄資料的白紙),程式會由上而下再執行一次。所以每次的使用者的互動無法保留原來的變數。

Session state就是一個解決方案,讓每次程式每次由上而下執行時,重要的資訊(重要的記錄)可以儲存在session state內。如下圖表示!

![](./images/pic1.png)

> 附註:當按下瀏覽器的重新整理時,是建立一個全新的Session。

### 為何要學習session_state
- 下面程式有問題

```python
#下面是錯誤的寫法
#每按一次按鈕,一樣是顯示1
#要了解原因必需要學會session_state
import streamlit as st

st.title('Counter Example')
count = 0

increment = st.button('Increment')
if increment:
    count += 1

st.write('Count = ', count)
```

##### 初始化session_state

```python
import streamlit as st

# Check if 'key' already exists in session_state
# If not, then initialize it
if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# Session State also supports the attribute based syntax
if 'key' not in st.session_state:
    st.session_state.key = 'value'
```

##### 讀取和更新session_state

```python
import streamlit as st

if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# Reads
st.write(st.session_state.key)

# Outputs: value
```


```python
if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# Updates
st.session_state.key = 'value2'     # Attribute API
st.session_state['key'] = 'value2'  # Dictionary like API
```

##### 沒有初始化session_state,就取出會throw exception

```python
mport streamlit as st

st.write(st.session_state['value'])

# Throws an exception!
```

##### 增加session state(計數器的標準寫法)

```python
import streamlit as st

st.title('Counter Example')
if 'count' not in st.session_state:
    st.session_state.count = 0

increment = st.button('Increment')
if increment:
    st.session_state.count += 1

st.write('Count = ', st.session_state.count)
```

##### Session State 和 Callback

```python
import streamlit as st

st.title('Counter Example using Callbacks')
if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter():
    st.session_state.count += 1

st.button('Increment', on_click=increment_counter)

st.write('Count = ', st.session_state.count)
```

#### Callback 和 args,kwargs

```python
import streamlit as st

st.title('Counter Example using Callbacks with args')
if 'count' not in st.session_state:
    st.session_state.count = 0

increment_value = st.number_input('Enter a value', value=0, step=1)

def increment_counter(increment_value):
    st.session_state.count += increment_value

increment = st.button('Increment', on_click=increment_counter,
    args=(increment_value, ))

st.write('Count = ', st.session_state.count)
```

```
import streamlit as st

st.title('Counter Example using Callbacks with kwargs')
if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter(increment_value=0):
    st.session_state.count += increment_value

def decrement_counter(decrement_value=0):
    st.session_state.count -= decrement_value

st.button('Increment', on_click=increment_counter,
	kwargs=dict(increment_value=5))

st.button('Decrement', on_click=decrement_counter,
	kwargs=dict(decrement_value=1))

st.write('Count = ', st.session_state.count)
```


##### Forms and Callback

```python
import streamlit as st
import datetime

st.title('Counter Example')
if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.last_updated = datetime.time(0,0)

def update_counter():
    st.session_state.count += st.session_state.increment_value
    st.session_state.last_updated = st.session_state.update_time

with st.form(key='my_form'):
    st.time_input(label='Enter the time', value=datetime.datetime.now().time(), key='update_time')
    st.number_input('Enter a value', value=0, step=1, key='increment_value')
    submit = st.form_submit_button(label='Update', on_click=update_counter)

st.write('Current Count = ', st.session_state.count)
st.write('Last Updated = ', st.session_state.last_updated)
```

#### Advanced concepts

##### Session State and Widget State association

```python
import streamlit as st

if "celsius" not in st.session_state:
    # set the initial default value of the slider widget
    st.session_state.celsius = 50.0

st.slider(
    "Temperature in Celsius",
    min_value=-100.0,
    max_value=100.0,
    key="celsius"
)

# This will get the value of the slider widget
st.write(st.session_state.celsius)
```


##### 重要,st.button,st.file_uploader, 不可以使用Session API 設定default value

```python
#會出錯
import streamlit as st

if 'my_button' not in st.session_state:
    st.session_state.my_button = True
    # Streamlit will raise an Exception on trying to set the state of button

st.button('Submit', key='my_button')
```


### 範例1(1session_state_basics.py):

- session_state初始化
- 更改session_state
- 刪除session_state

```
import streamlit as st

st.title("Session State Basics")

"st.session_state object:", st.session_state

if 'a_counter' not in st.session_state: #初始化
    st.session_state['a_counter'] = 0 #只執行一次

if "boolean" not in st.session_state: #初始化
    st.session_state.boolean = False #只執行一次

st.write(st.session_state)

st.write("a_counter is:", st.session_state["a_counter"])
st.write("boolean is:",st.session_state.boolean)

for the_key in st.session_state.keys(): #取出所有session_state的key
    st.write(the_key)

for the_value in st.session_state.values():#取出所有session_state的value
    st.write(the_value)

for item in st.session_state.items():#取出所有session_state的key,value
    item

button = st.button("Update State",key="button") #button第一次始始化,button初設定為false,按一下,就更改為true,未來都是true了

"按button之前",st.session_state


if button:
    st.session_state['a_counter'] += 1
    st.session_state.boolean = not st.session_state.boolean
    "按完按鈕後",st.session_state


#for key in st.session_state.keys(): #清空所有的session_state
#    del st.session_state[key]
#
#st.session_state

```


### 範例2(2sessionStateWithWidgets.py):
- 了解widgets和session_state的關係

```
import streamlit as st

st.title("Session State Basics")

"st.session_state object:", st.session_state

## works with all widgets
number = st.slider("A number",1, 10, key="slider") #重要,session_state沒有就初始化,有就更新

st.write(st.session_state)

col1, buff, col2 = st.columns([1,0.5,3]) #columns已經在此建立container

#---------這一段最後寫------------
next = st.button("Next optin") #button第一次始始化,next初設定為false,按一下,就更改為true

if next:
    if st.session_state["radio_option"] == 'a':
        st.session_state.radio_option = 'b'
    elif st.session_state["radio_option"] == 'b':
        st.session_state.radio_option = 'c'
    else:
        st.session_state.radio_option = 'a'
#---------這一段最後寫------------

option_names = ["a", "b", "c"]
option = col1.radio("請選擇1個",option_names,key="radio_option")
st.session_state

if option == 'a':
    col2.write("您選擇的是'a' :smile:")
elif option == 'b':
    col2.write("您選擇的是'b' :heart:")
else:
    col2.write("您選擇是'c' :rocket:")

```

### callbacks function的運作
- 可以籍由參數名稱on_change和on_click 使用callbacks
- 可以接受on_change和on_click的引數值使用function名稱

### 範例3(3sessionStateWithCallBack.py)

```
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
```

## 參考文件:
- 文章介紹:
	- [Add statefulness to apps 官方說明](https://docs.streamlit.io/library/advanced-features/session-state)
	
	- [Session State for Streamlit](https://blog.streamlit.io/session-state-for-streamlit/)



- 影片介紹:
	- [Session State basic官方說明](https://youtu.be/92jUAXBmZyU?si=acJpTrmuIkcG0XW3)
	
	- [How to use Streamlit session states and callback functions](https://youtu.be/5l9COMQ3acc?si=aRPhivyJN3xdixqk)
