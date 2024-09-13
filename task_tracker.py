import json
import os
import sys
from datetime import datetime

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    task = {
        'id': len(tasks) + 1,
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Tarea '{description}' agregada.")

def list_tasks(status=None):
    tasks = load_tasks()
    for task in tasks:
        if status is None or task['status'] == status:
            print(f"{task['id']}: {task['description']} [{task['status']}]")

def update_task(task_id, description=None, status=None):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            if description:
                task['description'] = description
            if status:
                task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Tarea {task_id} actualizada.")
            return
    print(f"Tarea {task_id} no encontrada.")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f"Tarea {task_id} eliminada.")

def mark_task_as_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'done'
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Tarea {task_id} marcada como 'done'.")
            return
    print(f"Tarea {task_id} no encontrada.")

def main():
    if len(sys.argv) < 2:
        print("Uso: python task_tracker.py <comando> [<args>]")
        return

    command = sys.argv[1]

    if command == 'add':
        description = ' '.join(sys.argv[2:])
        add_task(description)
    elif command == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status)
    elif command == 'update':
        task_id = int(sys.argv[2])
        description = sys.argv[3] if len(sys.argv) > 3 else None
        status = sys.argv[4] if len(sys.argv) > 4 else None
        update_task(task_id, description, status)
    elif command == 'delete':
        task_id = int(sys.argv[2])
        delete_task(task_id)
    elif command == 'done':
        task_id = int(sys.argv[2])
        mark_task_as_done(task_id)
    elif command == 'in-progress':
        list_tasks('in-progress')
    else:
        print("Comando no reconocido.")

if __name__ == '__main__':
    main()