from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from database import get_db
from models import KnowledgePoint
from schemas import KnowledgePointResponse

router = APIRouter(prefix="/api/knowledge-points", tags=["知识点"])


@router.get("/", response_model=List[KnowledgePointResponse])
async def get_all_knowledge_points(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(KnowledgePoint).order_by(KnowledgePoint.id))
    return result.scalars().all()


@router.get("/by-chapter/{chapter_id}", response_model=List[KnowledgePointResponse])
async def get_knowledge_points_by_chapter(chapter_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(KnowledgePoint)
        .where(KnowledgePoint.chapter_id == chapter_id)
        .order_by(KnowledgePoint.order_index)
    )
    return result.scalars().all()


@router.get("/{kp_id}", response_model=KnowledgePointResponse)
async def get_knowledge_point(kp_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(KnowledgePoint).where(KnowledgePoint.id == kp_id))
    kp = result.scalar_one_or_none()
    if not kp:
        raise HTTPException(status_code=404, detail="知识点不存在")
    return kp
