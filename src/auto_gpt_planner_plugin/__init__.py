from auto_gpt_plugin_template import AutoGPTPluginTemplate
from .planner import Planner
from .database import DatabaseManager
from .models import Task, Plan
from .tasks import TaskManager

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    role: str
    content: str
    
class AutoGPTPlannerPlugin:
    """
    This is the main class for the AutoGPT Planner Plugin. It integrates all the components of the plugin and provides
    the main interface for interacting with the plugin.
    """

    def __init__(self):
        """
        Initialize the AutoGPTPlannerPlugin with a Planner, DatabaseManager, and TaskManager instances.
        """
        self._name = "AutoGPT-Planner-Plugin"
        self._version = "0.1.0"
        self._description = "This is a task planner plugin for Auto-GPT. It manages tasks and plans for the user."

        # Initialize the database manager
        self.database_manager = DatabaseManager()

        # Initialize the task manager with the database manager
        self.task_manager = TaskManager(self.database_manager)

        # Initialize the planner with the task manager
        self.planner = Planner(self.task_manager)

    def start_planning_cycle(self):
        """
        Starts the planning cycle. This includes generating a new plan, creating tasks based on the plan,
        and executing tasks based on their priority.
        """
        try:
            self.planner.start_planning_cycle()
        except Exception as e:
            raise Exception("Failed to start planning cycle: " + str(e))

    def generate_plan(self):
        """
        Generates a new plan and saves it to the database.
        """
        try:
            self.planner.generate_plan()
        except Exception as e:
            raise Exception("Failed to generate plan: " + str(e))

    def generate_tasks(self):
        """
        Generates tasks based on the current plan and saves them to the database.
        """
        try:
            self.planner.generate_tasks()
        except Exception as e:
            raise Exception("Failed to generate tasks: " + str(e))

    def execute_task(self, task_id):
        """
        Executes a task based on its ID.

        Args:
            task_id (int): The ID of the task to execute.
        """
        try:
            self.task_manager.execute_task(task_id)
        except Exception as e:
            raise Exception("Failed to execute task: " + str(e))

    def mark_task_complete(self, task_id):
        """
        Marks a task as complete based on its ID.

        Args:
            task_id (int): The ID of the task to mark as complete.
        """
        try:
            self.task_manager.mark_task_complete(task_id)
        except Exception as e:
            raise Exception("Failed to mark task as complete: " + str(e))

    def update_plan(self):
        """
        Updates the current plan based on the completed tasks.
        """
        try:
            self.planner.update_plan()
        except Exception as e:
            raise Exception("Failed to update plan: " + str(e))

    def get_plan(self):
        """
        Retrieves the current plan from the database.

        Returns:
            Plan: The current plan.
        """
        try:
            return self.planner.get_plan()
        except Exception as e:
            raise Exception("Failed to get plan: " + str(e))

    def get_tasks(self):
        """
        Retrieves all tasks from the database.

        Returns:
            List[Task]: A list of all tasks.
        """
        try:
            return self.task_manager.get_tasks()
        except Exception as e:
            raise Exception("Failed to get tasks: " + str(e))

    def get_task(self, task_id):
        """
        Retrieves a task based on its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            Task: The task with the given ID.
        """
        try:
            return self.task_manager.get_task(task_id)
        except Exception as e:
            raise Exception("Failed to get task: " + str(e))

