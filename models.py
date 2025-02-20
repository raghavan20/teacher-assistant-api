from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float, LargeBinary, create_engine
from datetime import datetime
from utils import Registry

from db_init import init_db

class Recording(Registry.s_db.Model):
    __tablename__ = 'recordings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    recording_blob = Column(LargeBinary, nullable=False)
    user_id = Column(Integer, nullable=False)
    subject = Column(String(255), nullable=False)
    grade = Column(String(50), nullable=False)

    r_full_response_json = Column(JSON, nullable=True)
    r_overall_score = Column(Float, nullable=True)
    r_suggestions_count = Column(Integer, nullable=True)
    r_topics_required = Column(Integer, nullable=True)
    r_topics_covered = Column(Integer, nullable=True)
    r_structure = Column(Float, nullable=True)
    r_depth = Column(Float, nullable=True)
    r_style = Column(Float, nullable=True)
