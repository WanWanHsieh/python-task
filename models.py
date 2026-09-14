from sqlalchemy import Column, Integer, String

from database import Base


# 這個類別對應到資料庫裡的一張表：todos
# SQLAlchemy 的 ORM 會自動把這個類別跟資料表的欄位、資料列互相轉換
class TodoModel(Base):
    __tablename__ = "todos"

    # 主鍵，自動遞增
    id = Column(Integer, primary_key=True, index=True)
    # 待辦事項內容
    text = Column(String, nullable=False)
