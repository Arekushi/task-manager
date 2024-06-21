from http.client import HTTPException
from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.controllers.task_controller import task_router, get_task_repo
from src.domain.requests.task_request import TaskCreateRequest, TaskUpdateRequest
from src.domain.responses.task_response import TaskResponse
from src.domain.models.task import Task
from src.services.task_service import TaskService


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(task_router)
    return TestClient(app)


@pytest.fixture
def mock_task_service():
    mock = Mock(spec=TaskService)
    return mock


@pytest.fixture
def mock_task_repo(mock_task_service):
    mock_repo = Mock()
    mock_repo.return_value = mock_task_service
    return mock_repo


def test_create_task_endpoint(
    client,
    mock_task_service
):
    client.app.dependency_overrides[TaskService] = lambda: mock_task_service
    task_request = TaskCreateRequest(
        title='Test Task',
        description='This is a test task',
        status='DONE'
    )
    mock_task_service.create.return_value = task_request

    response = client.post(
        '/tasks/',
        json={
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'DONE'
        }
    )

    assert response.status_code == 201
    assert response.json()['title'] == 'Test Task'


def test_find_task_by_id_not_found(
    client,
    mock_task_service
):
    client.app.dependency_overrides[TaskService] = lambda: mock_task_service
    mock_task_service.get_by_id.return_value = None

    response = client.get(
        '/tasks/999'
    )

    assert response.status_code == 404


def test_update_task_success(
    client,
    mock_task_service
):
    client.app.dependency_overrides[TaskService] = lambda: mock_task_service
    task_update = TaskUpdateRequest(title='Updated Task')
    updated_task = TaskResponse(
        title='Updated Task',
        description='This is an updated task',
        status='done'
    )
    mock_task_service.update.return_value = updated_task

    response = client.put(
        '/tasks/1',
        json=task_update.model_dump(exclude_unset=True)
    )

    assert response.status_code == 200
    assert response.json()['title'] == 'Updated Task'


def test_update_task_not_found(
    client,
    mock_task_service
):
    client.app.dependency_overrides[TaskService] = lambda: mock_task_service
    task_update = TaskUpdateRequest(title='Updated Task')
    mock_task_service.update.side_effect = HTTPException(BaseException)

    response = client.put(
        '/tasks/999',
        json=task_update.model_dump(exclude_unset=True)
    )

    assert response.status_code == 404
    assert 'Task not found' in response.json()['detail']


def test_find_all_tasks(
    client,
    mock_task_repo,
    mock_task_service
):
    client.app.dependency_overrides[TaskService] = lambda: mock_task_service
    client.app.dependency_overrides[get_task_repo] = lambda: mock_task_repo

    mock_tasks = [
        Task(id=1, title='Task 1', description='This is task 1', status='done'),
        Task(id=2, title='Task 2', description='This is task 2', status='done'),
    ]

    mock_tasks_responses = [
        TaskResponse(title='Task 1', description='This is task 1', status='done'),
        TaskResponse(title='Task 2', description='This is task 2', status='done'),
    ]
    mock_task_repo.find_all.return_value = mock_tasks
    mock_task_service.find_all.return_value = mock_tasks_responses
    
    response = client.get(
        '/tasks'
    )

    assert response.status_code == 200
    response_data = response.json()
    
    assert len(response_data) == 2
    assert response_data[0]['title'] == 'Task 1'
    assert response_data[1]['title'] == 'Task 2'
