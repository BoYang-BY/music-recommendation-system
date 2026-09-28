from sqlmodel import Session, create_engine

from app.core.config import settings

# 建立資料庫引擎
engine = create_engine(settings.DATABASE_URL)


def get_session():
    """
    提供資料庫 Session
    使用完會自動關閉
    """
    with Session(engine) as session:
        yield session