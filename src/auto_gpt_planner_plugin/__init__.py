from sqlalchemy import create_engine
from auto_gpt_plugin_template import AutoGPTPluginTemplate
from .planner import Planner
from .database import DatabaseManager
from .models import Task, Plan
from .tasks import TaskManager
from typing import Any, Dict, List, Optional, Tuple, TypeVar, TypedDict

PromptGenerator = TypeVar("PromptGenerator")


class Message(TypedDict):
    role: str
    content: str


class AutoGPTPlannerPlugin(AutoGPTPluginTemplate):
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
        database_name = "autogpt_database"  # Replace "your_database_name" with your desired database name
        self.database_manager = DatabaseManager(database_name)

        # Create the SQLAlchemy engine
        db_path = f"sqlite:///autogpt_database.db"  # Replace "autogpt_database" with your desired database name
        engine = create_engine(db_path)

        # Initialize the task manager with the engine
        self.task_manager = TaskManager(engine)

        # Initialize the planner with the task manager
        self.planner = Planner()

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

    def can_handle_on_response(self) -> bool:
        return True

    def on_response(self, response: str, *args, **kwargs) -> str:
        pass

    def can_handle_post_prompt(self) -> bool:
        return True

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        pass

    def can_handle_on_planning(self) -> bool:
        return True

    def on_planning(self, prompt: PromptGenerator, messages: List[Message]) -> Optional[str]:
        pass

    def can_handle_post_planning(self) -> bool:
        return True

    def post_planning(self, response: str) -> str:
        pass

    def can_handle_pre_instruction(self) -> bool:
        return True

    def pre_instruction(self, messages: List[Message]) -> List[Message]:
        pass

    def can_handle_on_instruction(self) -> bool:
        return True

    def on_instruction(self, messages: List[Message]) -> Optional[str]:
        pass

    def can_handle_post_instruction(self) -> bool:
        return True

    def post_instruction(self, response: str) -> str:
        pass

    def can_handle_pre_command(self) -> bool:
        return True

    def pre_command(self, command_name: str, arguments: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        pass

    def can_handle_post_command(self) -> bool:
        return True

    def post_command(self, command_name: str, response: str) -> str:
        pass

    def can_handle_chat_completion(
        self, messages: Dict[Any, Any], model: str, temperature: float, max_tokens: int
    ) -> bool:
        return True

    def handle_chat_completion(
        self, messages: List[Message], model: str, temperature: float, max_tokens: int
    ) -> str:
        pass

    def can_handle_text_embedding(
        self, text: str
    ) -> bool:
        return True

    def handle_text_embedding(
        self, text: str
    ) -> list:
        pass

    def can_handle_user_input(self, user_input: str) -> bool:
        return True

    def user_input(self, user_input: str) -> str:
        pass

    def can_handle_report(self) -> bool:
        return True

    def report(self, message: str) -> None:
        pass
