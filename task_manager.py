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
