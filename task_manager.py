class Task:
    def __init__(self, id: int, name: str, completed: bool = False):
        self.id = id
        self.name = name
        self.completed = completed


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def create_task(self, name):
        # task = {"id": self.next_id, "name": name, "completed": False}
        # La creación de la tarea pasa a encapsularse en una clase
        task = Task(self.next_id, name)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def update_task_status(self, task_id, completed=False) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                task.completed = completed
                return task
        # ejecuta excepcion al no encontrar la tareas
        raise ValueError(f"Task with ID {task_id} not found.")

    def delete_task(self, task_id) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def get_task(self, task_id) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task

        # ejecuta una excepción al no encontrar la tarea
        raise ValueError(f"Task with ID {task_id} not found.")
