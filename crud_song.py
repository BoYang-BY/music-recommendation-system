from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.model import Song, Artist


def get_songs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> List[tuple[Song, str]]:
    """
    從資料庫取得歌曲列表（支援分頁）。

    :param db: 資料庫 Session
    :param skip: 跳過幾筆資料
    :param limit: 最多回傳幾筆資料
    :return: [(Song, artist_name), ...]
    """

    statement = (
        select(Song, Artist.artist_name)
        .join(Artist, Song.artist_id == Artist.artist_id)
        .offset(skip)
        .limit(limit)
    )

    songs = db.exec(statement).all()

    return songs


def get_song(
    db: Session,
    song_id: str,
) -> Optional[tuple[Song, str]]:
    """
    根據 song_id 查詢單一歌曲。

    :param db: 資料庫 Session
    :param song_id: 歌曲 ID
    :return: (Song, artist_name)
    """

    statement = (
        select(Song, Artist.artist_name)
        .join(Artist, Song.artist_id == Artist.artist_id)
        .where(Song.song_id == song_id)
    )

    result = db.exec(statement).first()

    return result