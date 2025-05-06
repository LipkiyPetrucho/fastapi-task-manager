import enum
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    pending = "pending"
    done = "done"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)

    tasks = relationship("Task", back_populates="owner", cascade="all, delete")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending, index=True)
    priority = Column(Integer, default=0, index=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User", back_populates="tasks")
