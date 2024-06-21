from fastapi import HTTPException
from pydantic import TypeAdapter
from src.domain.responses.task_response import TaskResponse
from src.domain.requests.task_request import TaskCreateRequest
from src.domain.models.task import Task
from src.repositories.task_repository import TaskRepository
from src.interfaces.base_service import IBaseService


class TaskService(IBaseService):
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create(self, obj: TaskCreateRequest):
        task = Task(**obj.model_dump())
        self.repository.create(task)
        
        return TypeAdapter(TaskResponse).validate_python(task)

    def get_by_id(self, id: int):
        task = self.repository.get_by_id(id)
        
        if not task:
            raise HTTPException(status_code=404, detail='Task not found')
        
        return TypeAdapter(TaskResponse).validate_python(task)

    def update(self, id: int, updated_data: dict):
        task = self.repository.get_by_id(id)
        
        if not task:
            raise HTTPException(status_code=404, detail='Task not found')
        
        updated_data = updated_data.model_dump(exclude_unset=True)
        updated_task = self.repository.update(task, updated_data)
        
        return TypeAdapter(TaskResponse).validate_python(updated_task)

    def delete_by_id(self, id: int):
        task = self.repository.get_by_id(id)
        
        if not task:
            raise HTTPException(status_code=404, detail='Task not found')
        
        return self.repository.delete_by_id(id)

    def find_all(self):
        tasks = self.repository.find_all()
        return [TypeAdapter(TaskResponse).validate_python(task) for task in tasks]
