from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default='user')
    profile_picture = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class ScheduledPost(Base):
    __tablename__ = 'scheduled_posts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    caption = Column(Text, nullable=True)
    media_url = Column(String(500), nullable=True)
    platform = Column(String(50), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(String(50), default='scheduled')
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    platform = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(50), default='active')
    created_at = Column(DateTime, default=func.now())

class PostAnalytics(Base):
    __tablename__ = 'post_analytics'
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, nullable=True)
    campaign_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=False)
    platform = Column(String(50), nullable=False)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    views = Column(Integer, default=0)
    recorded_at = Column(DateTime, default=func.now())