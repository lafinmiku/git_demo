# coding: utf-8
import requests
import pandas as pd
import json

# 基礎 URL (不包含參數)
base_url = "https://api.cnyes.com/media/api/v1/newslist/category/headline"

# 定義 payload 字典，包含所有 URL 參數
payload = {
    "page": 3,
    "limit": 30,
    "isCategoryHeadline": 1,
    "startAt": 1752644639, # Unix 時間戳：2025/07/15 06:17:19 (UTC)
    "endAt": 1753508639    # Unix 時間戳：2025/07/25 06:17:19 (UTC)
}

# 發送 GET 請求
res = requests.get(base_url, params=payload)

# 將響應內容解析為 JSON
jd = json.loads(res.text)

# 根據您提供的 JSON 結構，實際新聞資料在 'items' 鍵底下，然後再是 'data' 鍵
df = pd.DataFrame(jd['items']['data'])

# 篩選所需的欄位
df = df[['newsId', 'title', 'summary']]

# 創建 'link' 欄位，利用 newsId 構建完整的新聞連結
df['link'] = df['newsId'].apply(lambda x: 'https://m.cnyes.com/news/id/' + str(x))
df.to_csv('news.csv', encoding="utf-8-sig")
# 顯示 DataFrame
print(df)
>>>>>>> release
