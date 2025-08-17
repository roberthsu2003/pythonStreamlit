# Session State 管理和 Callback Function

> **版本說明**: 0.84版後，callback 的觀念已經加入

## 什麼是 Session State？

當瀏覽器的一個標籤頁面執行 Streamlit 應用程式時，整個 Streamlit 應用程式會產生一個全新的 session（當作一張白紙）。Streamlit 應用程式會由上而下執行所有的程式碼，並且依據程式碼建立 session 專用的變數（白紙上記錄資料）。

每一次使用者和 Streamlit 應用程式互動時，Streamlit 清除所有的變數（又變成一張沒有記錄資料的白紙），程式會由上而下再執行一次。所以每次的使用者的互動無法保留原來的變數。

**Session State 就是一個解決方案**，讓每次程式由上而下執行時，重要的資訊（重要的記錄）可以儲存在 session state 內。如下圖表示：

![Session State 概念圖](./images/pic1.png)

> **注意**: 當按下瀏覽器的重新整理時，是建立一個全新的 Session。

## 為何要學習 Session State？

下面程式有問題：

```python
# 下面是錯誤的寫法
# 每按一次按鈕，一樣是顯示 1
# 要了解原因必須要學會 session_state
import streamlit as st

st.title('Counter Example')
count = 0

increment = st.button('Increment')
if increment:
    count += 1

st.write('Count = ', count)
```

## Session State 基本操作

### 初始化 Session State

```python
import streamlit as st

# 檢查 'key' 是否已經存在於 session_state 中
# 如果不存在，則初始化它
if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# Session State 也支援屬性語法
if 'key' not in st.session_state:
    st.session_state.key = 'value'
```

### 讀取和更新 Session State

**讀取**：
```python
import streamlit as st

if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# 讀取
st.write(st.session_state.key)
# 輸出: value
```

**更新**：
```python
if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# 更新
st.session_state.key = 'value2'     # 屬性 API
st.session_state['key'] = 'value2'  # 字典 API
```

### 錯誤示範

沒有初始化 session_state 就取出會拋出異常：

```python
import streamlit as st

st.write(st.session_state['value'])
# 拋出異常！
```

## 實際應用範例

### 計數器的標準寫法

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

### Session State 和 Callback

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

### Callback 和 args、kwargs

**使用 args 參數**：
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

**使用 kwargs 參數**：
```python
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


### Forms 和 Callback

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

## 進階概念

### Session State 和 Widget State 關聯

```python
import streamlit as st

if "celsius" not in st.session_state:
    # 設定滑桿 widget 的初始預設值
    st.session_state.celsius = 50.0

st.slider(
    "Temperature in Celsius",
    min_value=-100.0,
    max_value=100.0,
    key="celsius"
)

# 這會取得滑桿 widget 的值
st.write(st.session_state.celsius)
```

### 重要限制

⚠️ **注意**: `st.button`、`st.file_uploader` 不可以使用 Session API 設定預設值

```python
# 會出錯的寫法
import streamlit as st

if 'my_button' not in st.session_state:
    st.session_state.my_button = True
    # Streamlit 會在嘗試設定按鈕狀態時拋出異常

st.button('Submit', key='my_button')
```


## 實作範例

### 範例 1：Session State 基礎操作 (`1session_state_basics.py`)

**功能**：
- Session State 初始化
- 更改 Session State
- 刪除 Session State

```python
import streamlit as st

st.title("Session State Basics")

"st.session_state object:", st.session_state

# 初始化
if 'a_counter' not in st.session_state:
    st.session_state['a_counter'] = 0  # 只執行一次

if "boolean" not in st.session_state:
    st.session_state.boolean = False  # 只執行一次

st.write(st.session_state)

st.write("a_counter is:", st.session_state["a_counter"])
st.write("boolean is:", st.session_state.boolean)

# 取出所有 session_state 的 key
for the_key in st.session_state.keys():
    st.write(the_key)

# 取出所有 session_state 的 value
for the_value in st.session_state.values():
    st.write(the_value)

# 取出所有 session_state 的 key, value
for item in st.session_state.items():
    item

# button 第一次初始化，button 初設定為 false，按一下就更改為 true，未來都是 true 了
button = st.button("Update State", key="button")

"按 button 之前", st.session_state

if button:
    st.session_state['a_counter'] += 1
    st.session_state.boolean = not st.session_state.boolean
    "按完按鈕後", st.session_state

# 清空所有的 session_state（註解掉的程式碼）
# for key in st.session_state.keys():
#     del st.session_state[key]
# st.session_state
```


### 範例 2：Session State 與 Widgets (`2sessionStateWithWidgets.py`)

**功能**：了解 widgets 和 session_state 的關係

```python
import streamlit as st

st.title("Session State Basics")

"st.session_state object:", st.session_state

# 適用於所有 widgets
# 重要：session_state 沒有就初始化，有就更新
number = st.slider("A number", 1, 10, key="slider")

st.write(st.session_state)

# columns 已經在此建立 container
col1, buff, col2 = st.columns([1, 0.5, 3])

# ---------這一段最後寫------------
# button 第一次初始化，next 初設定為 false，按一下就更改為 true
next = st.button("Next option")

if next:
    if st.session_state["radio_option"] == 'a':
        st.session_state.radio_option = 'b'
    elif st.session_state["radio_option"] == 'b':
        st.session_state.radio_option = 'c'
    else:
        st.session_state.radio_option = 'a'
# ---------這一段最後寫------------

option_names = ["a", "b", "c"]
option = col1.radio("請選擇 1 個", option_names, key="radio_option")
st.session_state

if option == 'a':
    col2.write("您選擇的是 'a' :smile:")
elif option == 'b':
    col2.write("您選擇的是 'b' :heart:")
else:
    col2.write("您選擇的是 'c' :rocket:")
```

## Callback Function 的運作

- 可以藉由參數名稱 `on_change` 和 `on_click` 使用 callbacks
- 可以接受 `on_change` 和 `on_click` 的引數值使用 function 名稱

### 範例 3：Session State 與 Callback (`3sessionStateWithCallBack.py`)

```python
import streamlit as st

st.title("Session State Basic")
"st.session_state object:", st.session_state

def lbs_to_kg():
    st.session_state.kg = st.session_state.lbs / 2.2046

def kg_to_lbs():
    st.session_state.lbs = st.session_state.kg * 2.2046

col1, buff, col2 = st.columns([2, 1, 2])

with col1:
    st.number_input("Pounds:", key='lbs', on_change=lbs_to_kg)

with col2:
    st.number_input("Kilograms:", key="kg", on_change=kg_to_lbs)
```

## 參考資源

### 📖 文章介紹
- [Add statefulness to apps 官方說明](https://docs.streamlit.io/library/advanced-features/session-state)
- [Session State for Streamlit](https://blog.streamlit.io/session-state-for-streamlit/)

### 🎥 影片介紹
- [Session State basic 官方說明](https://youtu.be/92jUAXBmZyU?si=acJpTrmuIkcG0XW3)
- [How to use Streamlit session states and callback functions](https://youtu.be/5l9COMQ3acc?si=aRPhivyJN3xdixqk)
