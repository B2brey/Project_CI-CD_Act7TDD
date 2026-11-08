import pytest

from task_manager import TaskManager


def test_create_task():
    manager = TaskManager()
    task = manager.create_task("Estudiar TDD")

    assert task.id == 1
    assert task.name == "Estudiar TDD"
    assert task.completed is False
    assert len(manager.tasks) == 1


def test_update_task_status():
    manager = TaskManager()
    task = manager.create_task("Comprar café")
    task_id = task.id

    updated_task = manager.update_task_status(task_id, completed=True)

    assert updated_task.completed is True
    assert manager.tasks[0].completed is True


# Prueba el caso de que la tareas no es encontrada
def test_update_task_not_found():
    manager = TaskManager()
    with pytest.raises(ValueError, match="Task with ID 999 not found."):
        manager.update_task_status(999, completed=True)


def test_delete_task():
    manager = TaskManager()
    task = manager.create_task("Revisar código")
    task_id = task.id

    assert len(manager.tasks) == 1

    manager.delete_task(task_id)

    assert len(manager.tasks) == 0
