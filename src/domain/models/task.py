import enum
from sqlalchemy import Column, Enum, Integer, String, DateTime
from sqlalchemy.sql import func

from src.db import Base, engine

class TaskStatusEnum(enum.Enum):
    TODO = 'to-do'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100))
    description = Column(String(250))
    status = Column(Enum(TaskStatusEnum))
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return (f'<Task(id={self.id}, title={self.title}, '
                f'description={self.description}, status={self.status}, '
                f'created_at={self.created_at})>')


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
