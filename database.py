# SQLAlchemy 的核心元件：
# create_engine：建立跟資料庫的連線
# declarative_base：讓我們可以用「類別」的方式定義資料表（ORM）
# sessionmaker：建立操作資料庫用的 session（每次讀寫都透過 session 進行）
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite 資料庫檔案路徑：sqlite:///./todos.db 代表在專案根目錄建立一個 todos.db 檔案
# 之後所有資料都會存在這個檔案裡，重啟伺服器也不會消失
DATABASE_URL = "sqlite:///./todos.db"

# 建立跟資料庫的連線引擎
# connect_args={"check_same_thread": False} 是 SQLite 特有設定：
# 因為 FastAPI 可能在不同 thread 處理請求，SQLite 預設只允許建立連線的那個 thread 使用，這裡把限制關掉
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal：每次請求要跟資料庫互動時，都會建立一個這樣的 session 實例
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base：之後定義資料表模型（models.py）時，都要繼承這個 Base
Base = declarative_base()


# 提供給 FastAPI 路由使用的相依性注入（dependency）
# 每次請求進來會建立一個新 session，用完後（無論成功或失敗）自動關閉，避免連線洩漏
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
