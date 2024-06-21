import pytest
from unittest.mock import Mock
from src.services.task_service import TaskService
from src.domain.requests.task_request import TaskCreateRequest, TaskUpdateRequest
from src.domain.responses.task_response import TaskResponse
from src.domain.models.task import Task


@pytest.fixture
def mock_task_repo():
    return Mock()


@pytest.fixture
def task_service(mock_task_repo):
    return TaskService(mock_task_repo)


def test_create_task(mock_task_repo, task_service):
    create_request = TaskCreateRequest(
        title='Test Task',
        description='This is a test task',
        status='done'
    )

    task = Task(
        id=1,
        title='Test Task',
        description='This is a test task',
        status='done'
    )
    mock_task_repo.create.return_value = task

    task_response = task_service.create(create_request)

    assert isinstance(task_response, TaskResponse)
    assert task_response.title == 'Test Task'
    assert task_response.description == 'This is a test task'


def test_get_by_id(mock_task_repo, task_service):
    task = Task(
        id=0,
        title='Test Task',
        description='This is a test task',
        status='done'
    )
    mock_task_repo.get_by_id.return_value = task

    task_response = task_service.get_by_id(task.id)

    assert isinstance(task_response, TaskResponse)
    assert task_response.title == 'Test Task'
    assert task_response.description == 'This is a test task'


def test_update_task(mock_task_repo, task_service):
    task = Task(
        id=0,
        title='Test Task',
        description='This is a test task',
        status='done'
    )
    mock_task_repo.get_by_id.return_value = task

    updated_data = TaskUpdateRequest(
        title='Updated Task',
        description='This is an updated task'
    )

    updated_task = Task(
        id=0,
        title='Updated Task',
        description='This is an updated task',
        status='done'
    )
    mock_task_repo.update.return_value = updated_task

    task_response = task_service.update(task.id, updated_data)

    assert isinstance(task_response, TaskResponse)
    assert task_response.title == 'Updated Task'
    assert task_response.description == 'This is an updated task'


def test_delete_by_id(mock_task_repo, task_service):
    task = Task(
        id=0,
        title='Test Task',
        description='This is a test task',
        status='done'
    )
    mock_task_repo.get_by_id.return_value = task
    mock_task_repo.delete_by_id.return_value = 0

    result = task_service.delete_by_id(task.id)
    
    assert result == 0


def test_find_all(mock_task_repo, task_service):
    tasks = [
        Task(id=0, title='Task 1', description='This is task 1', status='done'),
        Task(id=1, title='Task 2', description='This is task 2', status='done'),
        Task(id=2, title='Task 3', description='This is task 3', status='done'),
    ]
    mock_task_repo.find_all.return_value = tasks

    task_responses = task_service.find_all()

    assert len(task_responses) == 3
    for task_response in task_responses:
        assert isinstance(task_response, TaskResponse)
        assert task_response.title in [
            'Task 1',
            'Task 2',
            'Task 3'
        ]
        assert task_response.description in [
            'This is task 1',
            'This is task 2',
            'This is task 3'
        ]
