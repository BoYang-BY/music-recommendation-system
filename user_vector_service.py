from typing import List, Dict, Any, Optional

from sqlmodel import Session

from app.crud.crud_vector import VectorRepository
from app.crud.crud_user import get_user_history, get_users
from app.services.song_service import SongService


class UserVectorService:
    """
    處理使用者向量推薦相關業務邏輯，含推薦的歌曲
    """

    def __init__(self, db: Session):
        self.vector_repository = VectorRepository()
        self.db = db

    async def get_recommended_songs(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:

        # 1. 查詢使用者向量
        user_vector = await self.vector_repository.search_vector_by_user_id(
            user_id
        )

        if not user_vector:
            raise ValueError(
                f"No vector found for user id: {user_id}. Cannot generate recommendations."
            )

        # 2. 搜尋相似使用者
        similar_users = await self._find_similar_users(
            user_id,
            user_vector,
            limit + 1
        )

        # 3. 從相似使用者歷史推薦歌曲
        recommended_song_ids = await self._get_recommendations_from_similar_users(
            user_id,
            similar_users
        )

        # 限制推薦數量
        recommended_song_ids = recommended_song_ids[:limit]

        # 取得歌曲詳細資料
        recommended_songs = []

        for song_id in recommended_song_ids:

            song_details = await self._fetch_song_details(
                song_id
            )

            if song_details:
                recommended_songs.append(song_details)

        return recommended_songs

    async def _find_similar_users(
        self,
        user_id: str,
        user_vector: List[float],
        limit: int
    ) -> List[str]:

        """
        內部方法：在 Qdrant 中搜尋與給定向量相似的用戶。
        """

        search_result = await self.vector_repository.search_similar_users(
            user_vector,
            limit
        )

        # 從 Point 中擷取 original_id（使用者 ID）
        similar_users = [
            point.payload["user_id"]
            for point in search_result
            if point.payload
            and "user_id" in point.payload
            and point.payload["user_id"] != user_id
        ]

        if not similar_users:
            return []

        return similar_users

    async def _get_recommendations_from_similar_users(
        self,
        user_id: str,
        similar_user_ids: List[str]
    ) -> List[str]:

        """
        內部方法：從相似用戶的歷史記錄中篩選推薦歌曲。
        """

        # 從 PostgreSQL 獲取目前使用者的歷史紀錄
        user_history_songs = set(
            get_user_history(
                self.db,
                user_id
            )
        )

        recommended_songs = set()

        for similar_user_id in similar_user_ids:

            # 從 PostgreSQL 獲取相似使用者的歷史紀錄
            similar_user_history_songs = set(
                get_user_history(
                    self.db,
                    similar_user_id
                )
            )

            # 找到相似使用者聽過，但目前使用者沒聽過的歌曲
            new_recommendations = (
                similar_user_history_songs
                -
                user_history_songs
            )

            recommended_songs.update(new_recommendations)

        return list(recommended_songs)

    async def _fetch_song_details(
        self,
        song_id: str
    ) -> Optional[Dict[str, Any]]:

        """
        內部方法：從 PostgreSQL 獲取歌曲詳細資訊。
        """

        song_service = SongService(self.db)

        song_details = song_service.get_song(song_id)

        if not song_details:
            print(f"Warning: Song with ID {song_id} not found in DB.")
            return None

        return song_details

    async def get_users(
        self,
        skip: int = 0,
        limit: int = 10
    ) -> List[str]:

        """
        獲取所有使用者列表。
        """

        if limit <= 0:
            raise ValueError(
                "Limit must be a positive integer."
            )

        try:
            return get_users(
                self.db,
                skip=skip,
                limit=limit
            )

        except Exception as e:
            raise RuntimeError(
                f"An error occurred while fetching users: {e}"
            )