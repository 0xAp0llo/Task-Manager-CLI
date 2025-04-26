# 📝 Task Manager CLI

A simple yet powerful command-line task manager that helps you organize and track your tasks efficiently.

## ✨ Features

- ➕ Add tasks with title, description, priority, due date, and tags
- 📋 List tasks with flexible filtering and sorting options
- 🔍 View detailed information about specific tasks
- ✏️ Update task information (title, description, priority, status, due date, tags)
- ❌ Delete tasks when they're no longer needed
- 🏷️ Organize tasks with tags for better categorization
- 🔄 Track task status (pending, in progress, completed, cancelled)
- 🔝 Set task priorities (low, medium, high, critical)

## 📋 Requirements

- Python 3.6 or higher
- tabulate library

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/task-manager-cli.git
cd task-manager-cli
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage
```bash
python main.py <command> [options]
```

## ⚙️ Commands

- `add`: Add a new task
- `list`: List tasks
- `view`: View task details
- `update`: Update a task
- `delete`: Delete a task

### Add Command Options
- `title`: Task title (required)
- `-d, --description`: Task description
- `-p, --priority`: Task priority (low, medium, high, critical)
- `--due`: Due date (YYYY-MM-DD)
- `-t, --tags`: Comma-separated list of tags

### List Command Options
- `-s, --status`: Filter by status (pending, in_progress, completed, cancelled)
- `-p, --priority`: Filter by priority (low, medium, high, critical)
- `-t, --tag`: Filter by tag
- `--sort`: Sort by field (created_at, due_date, priority)

### View Command Options
- `id`: Task ID (required)

### Update Command Options
- `id`: Task ID (required)
- `-i, --title`: New task title
- `-d, --description`: New task description
- `-p, --priority`: New task priority
- `-s, --status`: New task status
- `--due`: New due date (YYYY-MM-DD)
- `-t, --tags`: New comma-separated list of tags

### Delete Command Options
- `id`: Task ID (required)

### Global Options
- `-f, --file`: Tasks file (default: tasks.json)

## 📝 Examples

### Add a new task:
```bash
python main.py add "Complete project report" -d "Finish the quarterly report" -p high --due 2023-09-30 -t "work,reports,urgent"
```

### List all tasks:
```bash
python main.py list
```

### List only high priority tasks:
```bash
python main.py list -p high
```

### List tasks with a specific tag:
```bash
python main.py list -t urgent
```

### List completed tasks:
```bash
python main.py list -s completed
```

### Sort tasks by due date:
```bash
python main.py list --sort due_date
```

### View a specific task:
```bash
python main.py view abc123
```

### Update a task:
```bash
python main.py update abc123 -s in_progress -p high
```

### Delete a task:
```bash
python main.py delete abc123
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
