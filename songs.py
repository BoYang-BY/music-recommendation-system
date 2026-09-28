from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.database import get_session
from app.services.song_service import SongService
from app.model import Song

router = APIRouter(
    prefix="/songs",
    tags=["songs"],
)


@router.get("/", response_model=List[dict])
def read_songs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
):
    """
    取得歌曲列表
    """

    service = SongService(db)

    return service.get_songs(
        skip=skip,
        limit=limit,
    )


@router.get("/{song_id}", response_model=dict)
def read_song(
    song_id: str,
    db: Session = Depends(get_session),
):
    """
    取得單一歌曲
    """

    service = SongService(db)

    song = service.get_song(song_id)

    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found",
        )

    return song