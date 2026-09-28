from typing import List, Optional

from sqlmodel import Session

from app.crud.crud_song import get_songs, get_song


class SongService:

    def __init__(self, db: Session):
        self.db = db

    def get_songs(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[dict]:

        songs = get_songs(
            self.db,
            skip=skip,
            limit=limit,
        )

        return [
            {
                "song": song.model_dump(),
                "artist_name": artist_name,
            }
            for song, artist_name in songs
        ]

    def get_song(
        self,
        song_id: str,
    ) -> Optional[dict]:

        song_tuple = get_song(
            self.db,
            song_id,
        )

        if not song_tuple:
            return None

        song, artist_name = song_tuple

        return {
            "song": song.model_dump(),
            "artist_name": artist_name,
        }