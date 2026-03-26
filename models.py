from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    status = Column(String,default="pending", nullable=False)
    priority = Column(Integer, default=5, nullable=False)
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)