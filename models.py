from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class FileMeta(Base):
    __tablename__ = 'file_meta'

    id = Column(String, primary_key=True)
    filename = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime)
    token = Column(String)
