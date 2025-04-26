#!/usr/bin/env python3

import os
import json
import argparse
from datetime import datetime, timedelta
import uuid
import tabulate

# Constants
DEFAULT_TASKS_FILE = "tasks.json"
PRIORITIES = ["low", "medium", "high", "critical"]
STATUSES = ["pending", "in_progress", "completed", "cancelled"]

def load_tasks(tasks_file=DEFAULT_TASKS_FILE):
    """Load tasks from the tasks file"""
    if os.path.exists(tasks_file):
        try:
            with open(tasks_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {tasks_file} is corrupted. Creating a new tasks file.")
            return []
    return []

def save_tasks(tasks, tasks_file=DEFAULT_TASKS_FILE):
    """Save tasks to the tasks file"""
    with open(tasks_file, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(title, description="", priority="medium", due_date=None, tags=None, tasks_file=DEFAULT_TASKS_FILE):
    """Add a new task to the tasks list"""
    tasks = load_tasks(tasks_file)
    
    # Validate priority
    if priority.lower() not in PRIORITIES:
        print(f"Invalid priority: {priority}. Using 'medium' instead.")
        priority = "medium"
    
    # Create a new task
    task = {
        "id": str(uuid.uuid4())[:8],  # Generate a short unique ID
        "title": title,
        "description": description,
        "priority": priority.lower(),
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "due_date": due_date,
        "completed_at": None,
        "tags": tags or []
    }
    
    # Add the task to the list
    tasks.append(task)
    
    # Save the updated tasks list
    save_tasks(tasks, tasks_file)
    
    print(f"Task added with ID: {task['id']}")
    return task["id"]

def list_tasks(status=None, priority=None, tag=None, sort_by="created_at", tasks_file=DEFAULT_TASKS_FILE):
    """List tasks with optional filtering and sorting"""
    tasks = load_tasks(tasks_file)
    
    # Filter tasks if needed
    if status:
        if status.lower() not in STATUSES:
            print(f"Invalid status: {status}")
            return
        tasks = [task for task in tasks if task["status"] == status.lower()]
    
    if priority:
        if priority.lower() not in PRIORITIES:
            print(f"Invalid priority: {priority}")
            return
        tasks = [task for task in tasks if task["priority"] == priority.lower()]
    
    if tag:
        tasks = [task for task in tasks if tag.lower() in [t.lower() for t in task["tags"]]]
    
    # Sort tasks
    if sort_by in ["created_at", "due_date", "priority"]:
        if sort_by == "priority":
            priority_order = {p: i for i, p in enumerate(PRIORITIES)}
            tasks = sorted(tasks, key=lambda x: priority_order.get(x["priority"], 0), reverse=True)
        else:
            tasks = sorted(tasks, key=lambda x: x[sort_by] if x[sort_by] is not None else "")
    
    if not tasks:
        print("No tasks found")
        return
    
    # Prepare data for tabulate
    table_data = []
    for task in tasks:
        # Format due date
        due_date = task["due_date"] if task["due_date"] else ""
        
        # Format status with color indicators
        status = task["status"]
        status_display = status
        
        # Format priority with color indicators
        priority = task["priority"]
        priority_display = priority
        
        # Truncate description if too long
        description = task["description"]
        if description and len(description) > 30:
            description = description[:27] + "..."
        
        # Format tags
        tags = ", ".join(task["tags"]) if task["tags"] else ""
        
        table_data.append([
            task["id"],
            task["title"],
            description,
            priority_display,
            status_display,
            due_date,
            tags
        ])
    
    # Print the table
    headers = ["ID", "Title", "Description", "Priority", "Status", "Due Date", "Tags"]
    print("\n" + tabulate.tabulate(table_data, headers=headers, tablefmt="grid"))
    print(f"\nTotal: {len(tasks)} tasks\n")

def update_task(task_id, title=None, description=None, priority=None, status=None, due_date=None, tags=None, tasks_file=DEFAULT_TASKS_FILE):
    """Update an existing task"""
    tasks = load_tasks(tasks_file)
    
    # Find the task by ID
    for task in tasks:
        if task["id"] == task_id:
            # Update task fields if provided
            if title is not None:
                task["title"] = title
            
            if description is not None:
                task["description"] = description
            
            if priority is not None:
                if priority.lower() not in PRIORITIES:
                    print(f"Invalid priority: {priority}. Keeping the current priority.")
                else:
                    task["priority"] = priority.lower()
            
            if status is not None:
                if status.lower() not in STATUSES:
                    print(f"Invalid status: {status}. Keeping the current status.")
                else:
                    old_status = task["status"]
                    task["status"] = status.lower()
                    
                    # Update completed_at if the task is being marked as completed
                    if task["status"] == "completed" and old_status != "completed":
                        task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    elif task["status"] != "completed":
                        task["completed_at"] = None
            
            if due_date is not None:
                task["due_date"] = due_date
            
            if tags is not None:
                task["tags"] = tags
            
            # Save the updated tasks list
            save_tasks(tasks, tasks_file)
            
            print(f"Task {task_id} updated successfully")
            return True
    
    print(f"Task with ID {task_id} not found")
    return False

def delete_task(task_id, tasks_file=DEFAULT_TASKS_FILE):
    """Delete a task by ID"""
    tasks = load_tasks(tasks_file)
    
    # Find the task by ID
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            # Remove the task
            removed_task = tasks.pop(i)
            
            # Save the updated tasks list
            save_tasks(tasks, tasks_file)
            
            print(f"Task {task_id} ({removed_task['title']}) deleted successfully")
            return True
    
    print(f"Task with ID {task_id} not found")
    return False

def view_task(task_id, tasks_file=DEFAULT_TASKS_FILE):
    """View detailed information about a task"""
    tasks = load_tasks(tasks_file)
    
    # Find the task by ID
    for task in tasks:
        if task["id"] == task_id:
            print("\n" + "="*50)
            print(f"Task ID: {task['id']}")
            print("="*50)
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Priority: {task['priority']}")
            print(f"Status: {task['status']}")
            print(f"Created: {task['created_at']}")
            
            if task["due_date"]:
                print(f"Due Date: {task['due_date']}")
            
            if task["completed_at"]:
                print(f"Completed: {task['completed_at']}")
            
            if task["tags"]:
                print(f"Tags: {', '.join(task['tags'])}")
            
            print("="*50 + "\n")
            return True
    
    print(f"Task with ID {task_id} not found")
    return False

def main():
    parser = argparse.ArgumentParser(description="Simple task manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add task command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-d", "--description", default="", help="Task description")
    add_parser.add_argument("-p", "--priority", default="medium", choices=PRIORITIES, help="Task priority")
    add_parser.add_argument("--due", default=None, help="Due date (YYYY-MM-DD)")
    add_parser.add_argument("-t", "--tags", default="", help="Comma-separated list of tags")
    
    # List tasks command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("-s", "--status", choices=STATUSES, help="Filter by status")
    list_parser.add_argument("-p", "--priority", choices=PRIORITIES, help="Filter by priority")
    list_parser.add_argument("-t", "--tag", help="Filter by tag")
    list_parser.add_argument("--sort", default="created_at", choices=["created_at", "due_date", "priority"], help="Sort by field")
    
    # View task command
    view_parser = subparsers.add_parser("view", help="View task details")
    view_parser.add_argument("id", help="Task ID")
    
    # Update task command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", help="Task ID")
    update_parser.add_argument("-i", "--title", help="New task title")
    update_parser.add_argument("-d", "--description", help="New task description")
    update_parser.add_argument("-p", "--priority", choices=PRIORITIES, help="New task priority")
    update_parser.add_argument("-s", "--status", choices=STATUSES, help="New task status")
    update_parser.add_argument("--due", help="New due date (YYYY-MM-DD)")
    update_parser.add_argument("-t", "--tags", help="New comma-separated list of tags")
    
    # Delete task command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", help="Task ID")
    
    # File option for all commands
    for p in [add_parser, list_parser, view_parser, update_parser, delete_parser]:
        p.add_argument("-f", "--file", default=DEFAULT_TASKS_FILE, help=f"Tasks file (default: {DEFAULT_TASKS_FILE})")
    
    args = parser.parse_args()
    
    if args.command == "add":
        # Parse tags
        tags = [tag.strip() for tag in args.tags.split(",")] if args.tags else []
        add_task(args.title, args.description, args.priority, args.due, tags, args.file)
    
    elif args.command == "list":
        list_tasks(args.status, args.priority, args.tag, args.sort, args.file)
    
    elif args.command == "view":
        view_task(args.id, args.file)
    
    elif args.command == "update":
        # Parse tags if provided
        tags = None
        if args.tags is not None:
            tags = [tag.strip() for tag in args.tags.split(",")] if args.tags else []
        
        update_task(args.id, args.title, args.description, args.priority, args.status, args.due, tags, args.file)
    
    elif args.command == "delete":
        delete_task(args.id, args.file)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
