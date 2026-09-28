from typing import List

from sqlmodel import Session, select

from app.model import UserSongPlay


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> List[str]:

    statement = (
        select(UserSongPlay.user_id)
        .distinct()
        .offset(skip)
        .limit(limit)
    )

    users = db.exec(statement).all()

    return users


def get_user_history(
    db: Session,
    user_id: str,
) -> List[str]:

    statement = (
        select(UserSongPlay.song_id)
        .where(UserSongPlay.user_id == user_id)
    )

    songs = db.exec(statement).all()

    return songs