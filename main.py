# FastAPI：用來建立 API 的框架
from fastapi import Depends, FastAPI

# CORS 中介層：讓瀏覽器允許「不同網址」的前端（例如 Vue 開發伺服器）呼叫這個 API
from fastapi.middleware.cors import CORSMiddleware

# Pydantic 的 BaseModel：用來定義「請求資料的格式」，FastAPI 會自動驗證傳進來的資料符不符合這個格式
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import TodoModel

# 建立一個 FastAPI 應用程式實例，之後所有路由都掛在這個 app 上
app = FastAPI()

# 讓 SQLAlchemy 根據 models.py 裡定義的類別，在資料庫裡建立對應的資料表
# 如果資料表已經存在，這行不會重複建立或清空資料，只有「不存在時」才會建立
Base.metadata.create_all(bind=engine)

# 加上 CORS 設定
# 瀏覽器預設會擋掉「網頁所在網址」跟「API 網址」不同源的請求（例如 Vue 在 5173、API 在 8000）
# 這裡明確允許來自 http://localhost:5173（Vue 開發伺服器）的請求可以打進來
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允許哪些網址呼叫這個 API
    allow_methods=["*"],  # 允許所有 HTTP 方法（GET、POST...）
    allow_headers=["*"],  # 允許所有的 request header
)


# @app.get("/") 代表：當有人用 GET 方法造訪網站根目錄「/」時，執行下面這個函式
@app.get("/")
def read_root():
    # 回傳一個 dict，FastAPI 會自動轉成 JSON 格式回給呼叫端
    return {"message": "Hello, API!"}


# 路徑裡的 {item_id} 是「路徑參數」，會被自動帶入下面函式的 item_id 參數
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    # item_id: int 代表 FastAPI 會自動把網址上的文字轉成整數，並驗證格式對不對
    # q: str | None = None 代表這是「選填的查詢參數」（網址上 ?q=xxx 的部分），沒帶的話預設是 None
    return {"item_id": item_id, "q": q}


# 定義一個資料格式（schema）：新增待辦事項時，前端傳來的 JSON 必須要有一個叫 text 的字串欄位
# FastAPI 會自動檢查傳進來的資料符不符合這個格式，不符合會自動回傳錯誤訊息
class Todo(BaseModel):
    text: str


# 取得目前所有待辦事項
# db: Session = Depends(get_db) 是「依賴注入」：
# FastAPI 會在每次請求進來時，呼叫 database.py 裡的 get_db()，拿到一個資料庫 session 傳進來
@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    # 查詢 todos 資料表裡的所有資料列，回傳的是 TodoModel 物件的 list
    return db.query(TodoModel).all()


# 新增一筆待辦事項
# todo: Todo 代表這個函式會自動從請求的 JSON body 裡，解析並驗證出一個 Todo 物件
@app.post("/todos")
def add_todo(todo: Todo, db: Session = Depends(get_db)):
    db_todo = TodoModel(text=todo.text)  # 建立一筆對應到資料表的物件
    db.add(db_todo)  # 加進這次 session 的待處理清單
    db.commit()  # 真正寫進資料庫檔案
    db.refresh(db_todo)  # 把資料庫產生的欄位（例如自動遞增的 id）同步回這個物件
    return db_todo


# 刪除一筆待辦事項
# {todo_id} 是路徑參數，代表要刪除哪一筆
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    # 先查詢這筆資料存不存在
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)  # 標記要刪除
        db.commit()  # 真正寫進資料庫
    return {"ok": True}

# 修改一筆待辦事項
# 沿用同一個 Todo schema(只需要傳新的 text)
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if db_todo:
        db_todo.text = todo.text  # 更新內容
        db.commit()
        db.refresh(db_todo)
    return db_todo
