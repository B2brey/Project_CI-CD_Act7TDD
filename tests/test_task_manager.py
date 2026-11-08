import pytest

from task_manager import TaskManager


def test_create_task():
    manager = TaskManager()
    task = manager.create_task("Estudiar TDD")

    assert task.id == 1
    assert task.name == "Estudiar TDD"
    assert task.completed is False
    assert len(manager.tasks) == 1
