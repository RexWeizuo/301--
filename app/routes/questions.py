from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from database import get_db
from models import Question, KnowledgePoint, Chapter, Subject
from schemas import QuestionResponse

router = APIRouter(prefix="/api/questions", tags=["题目"])

SUBJECT_NAMES = {"advanced_math": "高等数学", "linear_algebra": "线性代数", "probability": "概率论与数理统计"}
SUBJECT_ICONS = {"advanced_math": "📐", "linear_algebra": "📊", "probability": "🎲"}


@router.get("/", response_model=List[QuestionResponse])
async def get_all_questions(
    knowledge_point_id: Optional[str] = None,
    chapter_id: Optional[str] = None,
    subject_id: Optional[str] = None,
    type: Optional[str] = None,
    difficulty: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Question)

    if knowledge_point_id:
        query = query.where(Question.knowledge_point_id == knowledge_point_id)
    if type:
        query = query.where(Question.type == type)
    if difficulty:
        query = query.where(Question.difficulty == difficulty)

    if chapter_id:
        kp_result = await db.execute(
            select(KnowledgePoint.id).where(KnowledgePoint.chapter_id == chapter_id)
        )
        kp_ids = [row[0] for row in kp_result.fetchall()]
        if kp_ids:
            query = query.where(Question.knowledge_point_id.in_(kp_ids))
        else:
            return []

    if subject_id:
        ch_result = await db.execute(
            select(Chapter.id).where(Chapter.subject_id == subject_id)
        )
        ch_ids = [row[0] for row in ch_result.fetchall()]
        if ch_ids:
            kp_result = await db.execute(
                select(KnowledgePoint.id).where(KnowledgePoint.chapter_id.in_(ch_ids))
            )
            kp_ids = [row[0] for row in kp_result.fetchall()]
            if kp_ids:
                query = query.where(Question.knowledge_point_id.in_(kp_ids))
            else:
                return []
        else:
            return []

    query = query.order_by(Question.knowledge_point_id, Question.id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/grouped")
async def get_questions_grouped(
    subject_id: Optional[str] = None,
    type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """批量加载所有数据，在内存中组装（避免 N+1 查询）"""
    # 从 Subject 表获取学科列表（而非从 chapters 猜）
    subjects_result = await db.execute(select(Subject).order_by(Subject.id))
    subjects = subjects_result.scalars().all()

    # 一次性加载所有章节、知识点、题目
    chapters_result = await db.execute(
        select(Chapter).order_by(Chapter.subject_id, Chapter.order_index)
    )
    all_chapters = chapters_result.scalars().all()

    kps_result = await db.execute(
        select(KnowledgePoint).order_by(KnowledgePoint.chapter_id, KnowledgePoint.order_index)
    )
    all_kps = kps_result.scalars().all()

    q_query = select(Question)
    if type:
        q_query = q_query.where(Question.type == type)
    q_query = q_query.order_by(Question.knowledge_point_id, Question.id)
    q_result = await db.execute(q_query)
    all_questions = q_result.scalars().all()

    # 内存中建立索引
    kps_by_chapter = {}
    for kp in all_kps:
        kps_by_chapter.setdefault(kp.chapter_id, []).append(kp)

    questions_by_kp = {}
    for q in all_questions:
        questions_by_kp.setdefault(q.knowledge_point_id, []).append(q)

    chapters_by_subject = {}
    chapter_obj = {}
    for ch in all_chapters:
        chapter_obj[ch.id] = ch
        chapters_by_subject.setdefault(ch.subject_id, []).append(ch.id)

    result_data = []
    for subject in subjects:
        if subject_id and subject.id != subject_id:
            continue

        ch_ids = chapters_by_subject.get(subject.id, [])
        chapter_data = []
        for ch_id in ch_ids:
            ch = chapter_obj[ch_id]
            kps = kps_by_chapter.get(ch.id, [])
            kp_data = []
            for kp in kps:
                questions = questions_by_kp.get(kp.id, [])
                if questions:
                    kp_data.append({
                        "knowledge_point_id": kp.id,
                        "knowledge_point_name": kp.name,
                        "questions": [{
                            "id": q.id, "type": q.type, "question": q.question,
                            "options": q.options, "answer": q.answer,
                            "explanation": q.explanation, "difficulty": q.difficulty,
                        } for q in questions],
                    })
            if kp_data:
                chapter_data.append({
                    "chapter_id": ch.id,
                    "chapter_name": ch.name,
                    "knowledge_points": kp_data,
                })

        if chapter_data:
            result_data.append({
                "subject_id": subject.id,
                "subject_name": SUBJECT_NAMES.get(subject.id, subject.id),
                "subject_icon": SUBJECT_ICONS.get(subject.id, "📘"),
                "chapters": chapter_data,
            })

    return {"subjects": result_data}


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    return question
