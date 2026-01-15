from pathlib import Path
import argparse

from models import Task, TaskStatus
from storage import TaskRepository

def get_next_id(tasks: list[Task]) -> int:
    next_id = max((task.id for task in tasks), default=0) + 1

    return next_id

def cmd_add(args: argparse.Namespace, repo: TaskRepository) -> None:
    tasks = repo.load()

    task = Task(
        id= get_next_id(tasks),
        title=args.title,
    )

    tasks.append(task)
    repo.save(tasks)

    print(f"Tâche ajoutée [{task.id} {task.title}]")

def cmd_remove(args: argparse.Namespace, repo: TaskRepository) -> None:
    tasks = repo.load()
    task_Id = args.id

    for task in tasks:
        if task.id == task_Id:
            tasks.remove(task)
            repo.save(tasks)
            print(f"Tâche {task_Id} supprimée avec succès")
            return
    
    print(f"Tâche {task_Id} introuvable..")

def cmd_list(args: argparse.Namespace, repo: TaskRepository) -> None:
    tasks = repo.load()

    if not tasks:
        print("Aucune tâches")
        return

    for task in tasks:
        status = "✔" if task.status == TaskStatus.DONE else " "
        print(f"[{task.id}] [{status}] {task.title}")
    
def cmd_done(args: argparse.Namespace, repo: TaskRepository) -> None:
    tasks = repo.load()

    for task in tasks:
        if task.id == args.id:
            task.status = TaskStatus.DONE
            repo.save(tasks)
            print(f"Tâche {task.id} marquée comme terminée")
            return
    print(f"Tâche {args.id} introuvable")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gestionnaire de tâches CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Ajouter une tâche")
    add_parser.add_argument("title", help="Titre de la tâche")
    add_parser.set_defaults(func=cmd_add)

    remove_parser = subparsers.add_parser("remove", help="Supprimer une tâche")
    remove_parser.add_argument("id", type=int, help="Identifiant de la tâche")
    remove_parser.set_defaults(func=cmd_remove)

    list_parser = subparsers.add_parser("list", help="Lister les tâches")
    list_parser.set_defaults(func=cmd_list)

    done_parser = subparsers.add_parser("done", help="Marquer une tâche comme terminée")
    done_parser.add_argument("id", type=int, help="ID de la tâche")
    done_parser.set_defaults(func=cmd_done)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    repo = TaskRepository(Path("tasks.json"))
    args.func(args, repo)

if __name__ == "__main__":
    main()