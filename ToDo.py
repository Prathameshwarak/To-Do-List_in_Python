"""
ToDo.py - Simple console-based persistent to-do list manager.

Commands:
    add <task>        Add a new task
    remove <number>   Remove task by its number (from list)
    list              Show all tasks
    clear             Remove all tasks
    help              Show this help
    exit / quit       Save and exit
"""

from pathlib import Path

# DATA_FILE will store tasks in a text file next to this script (e.g., ToDo.txt)
DATA_FILE = Path(__file__).with_suffix('.txt')


# ---------------------- Load tasks from file ----------------------
def load_tasks():
    """Load all saved tasks from the text file into a list."""
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open('r', encoding='utf-8') as f:
        # Strip newlines and ignore empty lines
        return [line.strip() for line in f if line.strip()]


# ---------------------- Save tasks to file ----------------------
def save_tasks(tasks):
    """Save the current list of tasks to the file."""
    with DATA_FILE.open('w', encoding='utf-8') as f:
        for t in tasks:
            f.write(t + '\n')


# ---------------------- List all tasks ----------------------
def list_tasks(tasks):
    """Display all tasks with numbering."""
    if not tasks:
        print("No tasks.")
        return
    for i, t in enumerate(tasks, start=1):
        print(f"{i}. {t}")


# ---------------------- Add a new task ----------------------
def add_task(tasks, text):
    """Add a new task to the list and save it."""
    text = text.strip()
    if not text:
        print("Cannot add an empty task.")
        return
    tasks.append(text)
    save_tasks(tasks)
    print("Task added.")


# ---------------------- Remove a task ----------------------
def remove_task(tasks, index_str):
    """Remove a specific task by its number."""
    try:
        idx = int(index_str)
    except ValueError:
        print("Provide the task number to remove, e.g. remove 2")
        return

    if not (1 <= idx <= len(tasks)):
        print("Task number out of range.")
        return

    removed = tasks.pop(idx - 1)
    save_tasks(tasks)
    print(f"Removed: {removed}")


# ---------------------- Clear all tasks ----------------------
def clear_tasks(tasks):
    """Delete all tasks after user confirmation."""
    confirm = input("Are you sure you want to delete all tasks? (y/N): ").strip().lower()
    if confirm == 'y':
        tasks.clear()
        save_tasks(tasks)
        print("All tasks cleared.")
    else:
        print("Canceled.")


# ---------------------- Show help ----------------------
def print_help():
    """Print help instructions (from the docstring)."""
    print(__doc__)


# ---------------------- Main Function ----------------------
def main():
    """Main loop: continuously accept user commands and perform actions."""
    tasks = load_tasks()
    print("Simple To-Do List (type 'help' for commands)")

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not raw:
            continue  # Ignore empty input

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in ('exit', 'quit'):
            break
        elif cmd == 'help':
            print_help()
        elif cmd == 'list':
            list_tasks(tasks)
        elif cmd == 'add':
            if arg:
                add_task(tasks, arg)
            else:
                todo = input("Task: ").strip()
                add_task(tasks, todo)
        elif cmd == 'remove':
            if arg:
                remove_task(tasks, arg)
            else:
                num = input("Task number to remove: ").strip()
                remove_task(tasks, num)
        elif cmd == 'clear':
            clear_tasks(tasks)
        else:
            print("Unknown command. Type 'help' for usage.")

    # Save tasks again before exiting
    save_tasks(tasks)
    print("Goodbye!")


# ---------------------- Program Entry Point ----------------------
if __name__ == "__main__":
    main()
