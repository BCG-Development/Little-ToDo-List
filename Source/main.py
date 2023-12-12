import json
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDateEdit
from datetime import datetime


class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Todo List")
        self.setGeometry(100, 100, 600, 400)

        # Central Widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Task Name
        label_task_name = QLabel("Task Name:")
        self.entry_task_name = QLineEdit()
        layout.addWidget(label_task_name)
        layout.addWidget(self.entry_task_name)

        # Description
        label_description = QLabel("Description:")
        self.entry_description = QLineEdit()
        layout.addWidget(label_description)
        layout.addWidget(self.entry_description)

        # Date to Do
        label_date_to_do = QLabel("Date to Do:")
        self.entry_date_to_do = QDateEdit()
        layout.addWidget(label_date_to_do)
        layout.addWidget(self.entry_date_to_do)

        # Date to Complete
        label_date_to_complete = QLabel("Date to Complete:")
        self.entry_date_to_complete = QDateEdit()
        layout.addWidget(label_date_to_complete)
        layout.addWidget(self.entry_date_to_complete)

        # Priority
        label_priority = QLabel("Priority (1-5):")
        self.entry_priority = QLineEdit()
        layout.addWidget(label_priority)
        layout.addWidget(self.entry_priority)

        # Add Task Button
        button_add_task = QPushButton("Add Task", self)
        button_add_task.clicked.connect(self.add_task)
        layout.addWidget(button_add_task)

        # Show Tasks Button
        button_show_tasks = QPushButton("Show Tasks for Today", self)
        button_show_tasks.clicked.connect(self.show_tasks_for_today)
        layout.addWidget(button_show_tasks)

        # Set layout
        central_widget.setLayout(layout)

        # Create todo files if they don't exist
        for priority in range(1, 6):
            file_name = f"Source/todo_p{priority}.json"
            if not os.path.exists(file_name):
                with open(file_name, 'w') as f:
                    json.dump([], f, indent=4)

    def add_task(self):
        task_name = self.entry_task_name.text()
        description = self.entry_description.text()
        date_to_do = self.entry_date_to_do.date().toString("dd/MM/yyyy")
        date_to_complete = self.entry_date_to_complete.date().toString("dd/MM/yyyy")
        priority = int(self.entry_priority.text())

        task = {
            'Task Name': task_name,
            'Description': description,
            'Date to Do': date_to_do,
            'Date to Complete': date_to_complete
        }

        file_name = f"Source/todo_p{priority}.json"

        with open(file_name, 'r') as f:
            tasks = json.load(f)

        tasks.append(task)

        with open(file_name, 'w') as f:
            json.dump(tasks, f, indent=4)

        QMessageBox.information(self, "Task Added", "Task has been added successfully!")

    def show_tasks_for_today(self):
        today = datetime.today().strftime('%d/%m/%Y')
        tasks_for_today = []

        for priority in range(1, 6):
            file_name = f"Source/todo_p{priority}.json"
            with open(file_name, 'r') as f:
                tasks = json.load(f)
                for task in tasks:
                    if task['Date to Do'] == today:
                        task_with_priority = f"Priority {priority}: {task['Task Name']} - {task['Description']}"
                        tasks_for_today.append(task_with_priority)

        if not tasks_for_today:
            QMessageBox.information(self, "No Tasks", "No tasks for today.")
        else:
            task_list = "\n".join(tasks_for_today)
            QMessageBox.information(self, "Tasks for Today", task_list)


def run_app():
    app = QApplication([])
    window = TodoApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    run_app()
