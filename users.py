from typing import List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.database import get_session
from app.services.user_vector_service import UserVectorService


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/{user_id}/recommendations",
    response_model=List[Dict[str, Any]],
)
async def get_recommendations(
    user_id: str,
    limit: int = 10,
    db: Session = Depends(get_session),
):
    """
    根據使用者 ID 取得推薦歌曲

    user_id：
        要推薦的使用者 ID

    limit：
        推薦歌曲數量
    """

    service = UserVectorService(db)

    try:

        recommendations = await service.get_recommended_songs(
            user_id=user_id,
            limit=limit,
        )

        return recommendations

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )


@router.get(
    "/",
    response_model=List[str],
)
async def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
):
    """
    取得所有使用者
    """

    service = UserVectorService(db)

    try:

        users = await service.get_users(
            skip=skip,
            limit=limit,
        )

        return users

    except RuntimeError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {e}",
        )