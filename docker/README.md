# fastapi学习
## 容器启动
---
```
docker compose up -d
```

## 爬虫工具firecrawl
### 启动
```   
docker compose up -d
```
```
http://localhost:3002/v0/scrape

header = {
    "Content-Type": "application/json"
}

body= {
    "url":"https://news.cctv.com/world/"
}

```



## 网易云工具neteasecloudmusicapi
### 启动
```
npm install
PORT=4000 node app.js
```
## 图像数据库
cypher-shell -a 'neo4j://127.0.0.1:7687'

username: neo4j
password: neo4j123456


