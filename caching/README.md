# Streamlit Caching 快取機制

> **版本說明**: Streamlit 1.18.0+ 推薦使用 `@st.cache_data` 和 `@st.cache_resource`

## 什麼是 Caching？

Streamlit 每次使用者互動時都會重新執行整個腳本，這可能導致效能問題，特別是當你需要：
- 載入大量資料
- 執行複雜的計算
- 呼叫外部 API
- 訓練機器學習模型

**Caching 快取機制**可以儲存函數的執行結果，避免重複計算，大幅提升應用程式效能。

## Caching 的運作原理

1. **第一次執行**：函數正常執行，結果被快取
2. **後續執行**：如果輸入參數相同，直接返回快取結果
3. **參數改變**：重新執行函數並更新快取

![Caching 流程圖概念](./images/caching_flow.png)

## 新版 Caching API

### `@st.cache_data` - 資料快取

用於快取**資料**（如 DataFrame、字典、列表等可序列化物件）：

```python
import streamlit as st
import pandas as pd
import time

@st.cache_data
def load_data():
    # 模擬耗時的資料載入
    time.sleep(3)
    data = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['台北', '台中', '高雄']
    })
    return data

# 第一次執行會花 3 秒，之後會立即返回
df = load_data()
st.dataframe(df)
```

### `@st.cache_resource` - 資源快取

用於快取**全域資源**（如資料庫連線、機器學習模型等不可序列化物件）：

```python
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
import joblib

@st.cache_resource
def load_model():
    # 載入預訓練模型
    model = joblib.load('model.pkl')
    return model

@st.cache_resource
def init_database():
    # 初始化資料庫連線
    import sqlite3
    conn = sqlite3.connect('database.db')
    return conn

# 模型和資料庫連線只會初始化一次
model = load_model()
db_conn = init_database()
```

## 重要注意事項

### ⚠️ 快取限制

1. **參數必須是可雜湊的**：
```python
# ❌ 錯誤：list 不可雜湊
@st.cache_data
def process_data(data_list):
    return sum(data_list)

# ✅ 正確：使用 tuple
@st.cache_data
def process_data(data_tuple):
    return sum(data_tuple)
```

2. **避免快取可變物件**：
```python
# ❌ 危險：返回可變物件
@st.cache_data
def get_mutable_data():
    return {'count': 0}

# ✅ 安全：每次返回新物件
@st.cache_data
def get_immutable_data():
    return {'count': 0}.copy()
```

### 🔄 清除快取

```python
# 清除特定函數的快取
load_data.clear()

# 清除所有快取
st.cache_data.clear()
st.cache_resource.clear()
```

### 📊 快取設定參數

```python
@st.cache_data(
    ttl=3600,  # 快取存活時間（秒）
    max_entries=100,  # 最大快取條目數
    show_spinner=True,  # 顯示載入動畫
    persist="disk"  # 持久化到磁碟
)
def expensive_computation(x, y):
    time.sleep(2)
    return x * y + 42
```

## 實作範例

### 範例 1：資料載入快取

```python
import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("資料載入快取範例")

@st.cache_data
def generate_large_dataset(rows, cols):
    """生成大型資料集"""
    st.info(f"正在生成 {rows}x{cols} 的資料集...")
    time.sleep(2)  # 模擬耗時操作
    
    data = np.random.randn(rows, cols)
    df = pd.DataFrame(data, columns=[f'col_{i}' for i in range(cols)])
    return df

@st.cache_data
def process_data(df):
    """處理資料"""
    st.info("正在處理資料...")
    time.sleep(1)
    
    # 計算統計資訊
    stats = {
        'mean': df.mean().mean(),
        'std': df.std().mean(),
        'min': df.min().min(),
        'max': df.max().max()
    }
    return stats

# UI 控制項
rows = st.slider("資料列數", 100, 10000, 1000)
cols = st.slider("資料欄數", 5, 50, 10)

if st.button("生成資料"):
    # 第一次會執行函數，之後會使用快取
    df = generate_large_dataset(rows, cols)
    stats = process_data(df)
    
    st.success("資料生成完成！")
    st.dataframe(df.head())
    
    st.subheader("統計資訊")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("平均值", f"{stats['mean']:.2f}")
    col2.metric("標準差", f"{stats['std']:.2f}")
    col3.metric("最小值", f"{stats['min']:.2f}")
    col4.metric("最大值", f"{stats['max']:.2f}")

# 清除快取按鈕
if st.button("清除快取"):
    generate_large_dataset.clear()
    process_data.clear()
    st.success("快取已清除！")
```

### 範例 2：API 呼叫快取

```python
import streamlit as st
import requests
import time
from datetime import datetime

st.title("API 呼叫快取範例")

@st.cache_data(ttl=300)  # 快取 5 分鐘
def fetch_weather_data(city):
    """獲取天氣資料（模擬 API 呼叫）"""
    st.info(f"正在獲取 {city} 的天氣資料...")
    time.sleep(2)  # 模擬網路延遲
    
    # 模擬天氣資料
    import random
    weather_data = {
        'city': city,
        'temperature': random.randint(15, 35),
        'humidity': random.randint(30, 90),
        'description': random.choice(['晴天', '多雲', '小雨', '陰天']),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return weather_data

@st.cache_data(ttl=600)  # 快取 10 分鐘
def get_city_list():
    """獲取城市列表"""
    return ['台北', '台中', '台南', '高雄', '桃園', '新竹']

# 獲取城市列表
cities = get_city_list()
selected_city = st.selectbox("選擇城市", cities)

if st.button("獲取天氣"):
    weather = fetch_weather_data(selected_city)
    
    st.success(f"天氣資料獲取成功！（快取時間：{weather['timestamp']}）")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("溫度", f"{weather['temperature']}°C")
    col2.metric("濕度", f"{weather['humidity']}%")
    col3.metric("天氣", weather['description'])

# 顯示快取狀態
st.sidebar.subheader("快取管理")
if st.sidebar.button("清除天氣快取"):
    fetch_weather_data.clear()
    st.sidebar.success("天氣快取已清除！")

if st.sidebar.button("清除所有快取"):
    st.cache_data.clear()
    st.sidebar.success("所有快取已清除！")
```

## 舊版 API 對照

| 舊版 API | 新版 API | 用途 |
|---------|---------|------|
| `@st.cache` | `@st.cache_data` | 一般資料快取 |
| `@st.cache(allow_output_mutation=True)` | `@st.cache_resource` | 資源快取 |
| `@st.cache(persist=True)` | `@st.cache_data(persist="disk")` | 持久化快取 |

## 效能最佳化建議

1. **合理使用快取**：不要快取所有函數，只快取耗時操作
2. **設定適當的 TTL**：根據資料更新頻率設定快取時間
3. **監控記憶體使用**：設定 `max_entries` 避免記憶體溢出
4. **避免快取副作用**：確保函數是純函數
5. **使用持久化快取**：對於大型資料可考慮磁碟快取

## 常見問題

### Q: 什麼時候使用 `@st.cache_data` vs `@st.cache_resource`？
- `@st.cache_data`：用於可序列化的資料（DataFrame、字典、列表）
- `@st.cache_resource`：用於不可序列化的資源（資料庫連線、模型物件）

### Q: 如何處理快取鍵衝突？
```python
@st.cache_data
def load_data(file_path, _hash_funcs={pd.DataFrame: lambda x: x.shape}):
    return pd.read_csv(file_path)
```

### Q: 如何在快取中排除某些參數？
```python
@st.cache_data
def process_data(data, _debug=False):
    if _debug:  # 以 _ 開頭的參數不會影響快取鍵
        print("Debug mode")
    return data.sum()
```