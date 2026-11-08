# Project_CI-CD_Act7TDD

Este repositorio corresponde a la **Actividad 7 de la Unidad 5** de la asignatura de **Desarrollo Basado en Pruebas (TDD)**. El proyecto implementa un módulo robusto de gestión de tareas siguiendo estrictamente el ciclo TDD (*Red -> Green -> Refactor*) con el fin de aplicar los conocimientos sobre **CI** impartidos en la unidad.

## Características del Módulo

- **Creación de Tareas (`create_task`)**: Registro de nuevas tareas con ID autoincremental y estado inicial pendiente (`completed=False`).
- **Actualización de Estado (`update_task_status`)**: Permite modificar el estado de la tarea con manejo de excepciones si el ID no existe.
- **Eliminación de Tareas (`delete_task`)**: Remueve tareas de forma segura validando su existencia previa.
- **Pruebas Unitarias**: Cobertura completa utilizando `pytest`, evaluando tanto caminos felices como escenarios de error.

## Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **Testing:** Pytest
