from qdrant_client import QdrantClient
from app.core.config import settings


class VectorStore:
    """
    Qdrant 向量資料庫連線管理
    """

    def __init__(self):
        # 建立 Qdrant Client
        self.client = QdrantClient(
            url=settings.VECTOR_DATABASE_URL,
        )

    async def close(self):
        """
        關閉 Qdrant Client
        """
        if self.client:
            self.client.close()