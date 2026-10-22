import argparse
import sys
from src.manager import TaskManager

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title")
    add_parser.add_argument("--priority", choices=["low", "medium", "high"], default="medium", help="Task priority level")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--all", action="store_true", help="Include completed tasks")

    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("id", type=int, help="Task ID")

    del_parser = subparsers.add_parser("rm", help="Delete task")
    del_parser.add_argument("id", type=int, help="Task ID")

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    mgr = TaskManager()

    if args.command == "add":
        task = mgr.add_task(args.title, priority=args.priority)
        print(f"Added task #{task.id}: {task.title} (priority: {task.priority})")
    elif args.command == "list":
        tasks = mgr.list_tasks(include_completed=args.all)
        if not tasks:
            print("No tasks found.")
            return
        for t in tasks:
            status = "[x]" if t.completed else "[ ]"
            print(f"{status} #{t.id} [{t.priority.upper()}]: {t.title}")
    elif args.command == "done":
        task = mgr.complete_task(args.id)
        if task:
            print(f"Task #{task.id} marked complete.")
        else:
            print(f"Task #{args.id} not found.", file=sys.stderr)
            sys.exit(1)
    elif args.command == "rm":
        if mgr.delete_task(args.id):
            print(f"Task #{args.id} deleted.")
        else:
            print(f"Task #{args.id} not found.", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
