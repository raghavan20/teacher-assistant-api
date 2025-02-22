from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, LargeBinary
from datetime import datetime
from utils.utils import Registry


class Recording(Registry.s_db.Model):

    __tablename__ = 'recordings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    recording_blob = Column(LargeBinary, nullable=False)
    user_id = Column(Integer, nullable=False)
    subject = Column(String(255), nullable=False)
    grade = Column(String(50), nullable=False)
    language = Column(String(50), nullable=False)
    topic = Column(String(200), nullable=False)
    state = Column(String(50), nullable=False)
    board = Column(String(50), nullable=False)
    district = Column(String(100), nullable=False)
    block = Column(String(100), nullable=False)

    r_full_response_json = Column(JSON, nullable=True)
    r_overall_score = Column(Float, nullable=True)
    r_suggestions_count = Column(Integer, nullable=True)
    r_topics_required = Column(Integer, nullable=True)
    r_topics_covered = Column(Integer, nullable=True)
    r_structure = Column(Float, nullable=True) # pedagogy_score
    r_depth = Column(Float, nullable=True) # lesson_quality_score
    r_style = Column(Float, nullable=True) # teaching_guidelines_score
