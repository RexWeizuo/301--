from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Date, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)


class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(String, primary_key=True)
    subject_id = Column(String, ForeignKey("subjects.id"), nullable=False)
    name = Column(String, nullable=False)
    order_index = Column(Integer, default=0)


class KnowledgePoint(Base):
    __tablename__ = "knowledge_points"
    id = Column(String, primary_key=True)
    chapter_id = Column(String, ForeignKey("chapters.id"), nullable=False)
    name = Column(String, nullable=False)
    content = Column(Text, default="")
    order_index = Column(Integer, default=0)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    knowledge_point_id = Column(String, ForeignKey("knowledge_points.id"), nullable=False)
    type = Column(String, default="choice")
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    answer = Column(String, nullable=False)
    explanation = Column(Text, default="")
    difficulty = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)


class StudyRecord(Base):
    __tablename__ = "study_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    knowledge_point_id = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    study_date = Column(Date, nullable=False)
    time_spent = Column(Integer, default=0)
    correct_rate = Column(Float, default=0.0)
    mastery_level = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    next_review_date = Column(Date, nullable=True)
    last_review_date = Column(Date, nullable=True)
    interval_days = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)


class ChapterProgress(Base):
    __tablename__ = "chapter_progress"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    subject_id = Column(String, nullable=False)
    chapter_id = Column(String, nullable=False)
    total_knowledge_points = Column(Integer, default=0)
    completed_knowledge_points = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    completed_questions = Column(Integer, default=0)
    average_correct_rate = Column(Float, default=0.0)
    last_studied_date = Column(Date, nullable=True)
    completion_percentage = Column(Float, default=0.0)
