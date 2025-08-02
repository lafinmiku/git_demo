# coding: utf-8
import requests
import pandas as pd
import time
from datetime import datetime, timedelta

# API 基本網址
base_url = "https://api.cnyes.com/media/api/v1/newslist/category/headline"

# 設定起始與結束時間（預設抓近10日資料）
start_time = int((datetime.today() - timedelta(days=10)).timestamp())
end_time = int(datetime.today().timestamp())

# 發送第一次請求，取得 last_page
res = requests.get(base_url, params={
    "page": 1,
    "limit": 30,
    "isCategoryHeadline": 1,
    "startAt": start_time,
    "endAt": end_time
})
jd = res.json()

# 取出總頁數
last_page = jd['items']['last_page']
print(f"📄 共 {last_page} 頁，開始抓取...")

# 把第 1 頁的資料先放進來
all_data = jd['items']['data']

# 從第 2 頁開始逐頁抓
for page in range(2, last_page + 1):
    res = requests.get(base_url, params={
        "page": page,
        "limit": 30,
        "isCategoryHeadline": 1,
        "startAt": start_time,
        "endAt": end_time
    })
    jd = res.json()
    all_data.extend(jd['items']['data'])
    print(f"✅ 第 {page} 頁完成，目前累積 {len(all_data)} 筆")
    time.sleep(0.8)  # 為避免 API 過載，稍作延遲

# 整理成 DataFrame，只保留你要的欄位：newsId、title、summary
df = pd.DataFrame(all_data)[['newsId', 'title', 'summary']]

# 補上完整連結欄位
df['link'] = df['newsId'].apply(lambda x: f"https://m.cnyes.com/news/id/{x}")

# 存成 CSV
df.to_csv('cnyes_news_full.csv', encoding='utf-8-sig', index=False)

# 顯示前幾筆確認
print(df.head(10))
