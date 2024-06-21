from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db import get_db
from src.domain.requests.task_request import TaskCreateRequest, TaskUpdateRequest
from src.domain.responses.task_response import TaskResponse
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService

task_router = APIRouter(prefix='/tasks', tags=['Tasks'])


def get_task_repo(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


@task_router.post(
    '/',
    status_code=201,
    description='Cria uma nova task',
    response_model=TaskResponse
)
def create(
    request: TaskCreateRequest,
    task_repo: TaskRepository = Depends(get_task_repo)
):
    task_service = TaskService(task_repo)
    return task_service.create(request)


@task_router.get(
    '/{task_id}',
    status_code=200,
    description='Busca uma task pelo ID',
    response_model=TaskResponse
)
def find_by_id(
    task_id: int,
    task_repo: TaskRepository = Depends(get_task_repo)
):
    task_service = TaskService(task_repo)
    return task_service.get_by_id(task_id)


@task_router.get(
    '/',
    status_code=200,
    description='Busca todas as tasks',
    response_model=list[TaskResponse]
)
def find_all(
    task_repo: TaskRepository = Depends(get_task_repo)
):
    task_service = TaskService(task_repo)
    return task_service.find_all()


@task_router.put(
    '/{task_id}',
    status_code=200,
    description='Atualiza uma task',
    response_model=TaskResponse
)
def update(
    task_id: int,
    request: TaskUpdateRequest,
    task_repo: TaskRepository = Depends(get_task_repo)
):
    task_service = TaskService(task_repo)
    return task_service.update(task_id, request)


@task_router.delete(
    '/{task_id}',
    status_code=204,
    description='Deleta uma task'
)
def delete(
    task_id: int,
    task_repo: TaskRepository = Depends(get_task_repo)
):
    task_service = TaskService(task_repo)
    return task_service.delete_by_id(task_id)
