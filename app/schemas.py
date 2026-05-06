from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class KnowledgePointResponse(BaseModel):
    id: str
    chapter_id: str
    name: str
    content: str
    order_index: int
    model_config = {"from_attributes": True}


class QuestionResponse(BaseModel):
    id: int
    knowledge_point_id: str
    type: str
    question: str
    options: List[str]
    answer: str
    explanation: str
    difficulty: int
    created_at: datetime
    model_config = {"from_attributes": True}


class StudyRecordCreate(BaseModel):
    knowledge_point_id: str
    action_type: str
    time_spent: int = 0
    correct_rate: float = 0.0


class StudyRecordResponse(BaseModel):
    id: int
    user_id: int
    knowledge_point_id: str
    action_type: str
    study_date: date
    time_spent: int
    correct_rate: float
    mastery_level: float
    review_count: int
    next_review_date: Optional[date]
    last_review_date: Optional[date]
    interval_days: int
    model_config = {"from_attributes": True}


class ChapterProgressResponse(BaseModel):
    id: int
    user_id: int
    subject_id: str
    chapter_id: str
    total_knowledge_points: int
    completed_knowledge_points: int
    total_questions: int
    completed_questions: int
    average_correct_rate: float
    last_studied_date: Optional[date]
    completion_percentage: float
    model_config = {"from_attributes": True}


class StudyDashboard(BaseModel):
    today_new_count: int
    today_review_count: int
    today_question_count: int
    today_completed_percentage: float
    subject_progress: List[dict]
    urgent_reviews: List[dict]
    weak_points: List[dict]
