"""Ops endpoints: health + stats."""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import current_user
from app.api.schemas import HealthOut
from app.core.db import get_session
from app.models import Article, Feed, Story, User
from app.services.process import queue_depth
from app.version_metadata import get_version_metadata

router = APIRouter(tags=["ops"])


@router.get("/health")
async def health() -> HealthOut:
    metadata = get_version_metadata()
    return HealthOut(status="ok", version=metadata["sift_version"], **metadata)


@router.get("/stats")
async def stats(
    user: User = Depends(current_user), session: AsyncSession = Depends(get_session)
) -> dict[str, int]:
    return {
        "feeds": int(await session.scalar(select(func.count(Feed.id))) or 0),
        "articles": int(await session.scalar(select(func.count(Article.id))) or 0),
        "stories": int(await session.scalar(select(func.count(Story.id))) or 0),
        "llm_queue_depth": queue_depth(),
    }
