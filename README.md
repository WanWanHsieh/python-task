# 待辦清單（FastAPI + Vue 練習）

用來學習前後端分離的小專案：Python **FastAPI** 寫 API，**Vue 3 + TypeScript** 寫畫面，資料存在 **SQLite**。程式碼內附詳細中文註解。

## 功能

- 新增、查看、修改、刪除待辦事項（CRUD）

## API

| 方法 | 路徑 | 說明 |
|---|---|---|
| GET | `/todos` | 取得所有待辦 |
| POST | `/todos` | 新增待辦 |
| PUT | `/todos/{id}` | 修改待辦 |
| DELETE | `/todos/{id}` | 刪除待辦 |

API 文件：啟動後開 http://127.0.0.1:8000/docs

## 執行方式

```bash
python -m venv venv
make install   # 安裝前後端套件
make dev       # 同時啟動後端 (:8000) 與前端 (:5173)
```

## 檔案結構

| 路徑 | 用途 |
|---|---|
| `main.py` | FastAPI 路由 |
| `models.py` | 資料表定義（SQLAlchemy） |
| `database.py` | 資料庫連線（SQLite `todos.db`） |
| `frontend/` | Vue 3 + Vite 前端（含 Vitest、Playwright 測試設定） |
