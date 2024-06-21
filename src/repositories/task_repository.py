from types import NoneType
from typing import List
from sqlalchemy.orm import Session
from src.domain.models.task import Task
from src.interfaces.base_repository import IBaseRepository


class TaskRepository(IBaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, obj: Task) -> Task:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_by_id(self, id: int) -> Task:
        return self.session.query(Task)\
            .filter(Task.id == id)\
            .first()

    def update(self, obj: Task, updated_data: dict) -> Task:
        for key, value in updated_data.items():
            setattr(obj, key, value)
        
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete_by_id(self, id: int) -> int:
        obj = self.get_by_id(id)
        
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return id

    def find_all(self) -> List[Task]:
        return self.session.query(Task).all()
