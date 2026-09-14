.PHONY: install backend frontend dev

# 安裝後端 + 前端所有套件
install:
	venv/Scripts/pip install -r requirements.txt
	cd frontend && npm install

# 只啟動後端 (FastAPI, http://127.0.0.1:8000)
backend:
	venv/Scripts/uvicorn main:app --reload

# 只啟動前端 (Vue, http://localhost:5173)
frontend:
	cd frontend && npm run dev

# 同時啟動前後端 (兩個伺服器會一起在這個視窗裡跑)
dev:
	$(MAKE) -j 2 backend frontend
