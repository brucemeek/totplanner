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

        # Initialize the planner with the engine
        self.planner = Planner(engine, self.task_manager)

    def can_handle_on_response(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_response method.
        Returns:
            bool: True if the plugin can handle the on_response method."""
        return True

    def on_response(self, response: str, *args, **kwargs) -> str:
        """This method is called when a response is received from the model."""

    def can_handle_post_prompt(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_prompt method.
        Returns:
            bool: True if the plugin can handle the post_prompt method."""
        return True

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        """
        This method is called after the prompt has been generated but before it is sent to the model.
        It is used to perform actions related to task planning and management.

        The method performs the following steps:

        1. Starts the planning cycle by calling the `start_planning_cycle` method of the `Planner` class.
        This involves generating a new plan and task database, creating tasks based on the plan, and starting the execution of tasks.

        2. Generates a new plan by calling the `generate_plan` method of the `Planner` class. The plan is saved to the database.

        3. Generates tasks based on the current plan by calling the `generate_tasks` method of the `Planner` class. The tasks are saved to the database.

        4. Retrieves all tasks from the database by calling the `get_all_tasks` method of the `DatabaseManager` class.

        5. Iterates over the retrieved tasks. For each task, it performs the following actions:
        - Retrieves the task ID.
        - Executes the task by calling the `execute_task` method of the `TaskManager` class, passing the task ID as an argument.
        - Marks the task as complete by calling the `mark_task_complete` method of the `TaskManager` class, passing the task ID as an argument.
        - Retrieves the task based on its ID by calling the `get_task` method of the `TaskManager` class, passing the task ID as an argument.

        6. Updates the current plan based on the completed tasks by calling the `update_plan` method of the `Planner` class.

        7. Retrieves the current plan from the database by calling the `get_plan` method of the `Planner` class.

        8. Retrieves all tasks from the database by calling the `get_tasks` method of the `TaskManager` class.

        If any of the steps fail, an exception is raised and its message is printed to the console.

        Args:
            prompt (PromptGenerator): The prompt generator.

        Returns:
            PromptGenerator: The prompt generator.
        """
        # Call the methods here
        try:
            self.start_planning_cycle()
            self.generate_plan()
            self.generate_tasks()  # Generate the tasks and store them in the database

            # Retrieve all tasks from the database
            tasks = self.database_manager.get_all_tasks()

            # Iterate over the tasks and use the task IDs
            for task in tasks:
                task_id = task.id  # Get the task ID
                self.execute_task(task_id)
                self.mark_task_complete(task_id)
                self.get_task(task_id)

            self.update_plan()
            self.get_plan()
            self.get_tasks()

        except Exception as e:
            print(str(e))

        # Return the prompt
        return prompt

    def can_handle_on_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_planning method.
        Returns:
            bool: True if the plugin can handle the on_planning method."""
        return True

    def on_planning(
            self, prompt: PromptGenerator, messages: List[str]
    ) -> Optional[str]:
        """This method is called before the planning chat completeion is done.
        Args:
            prompt (PromptGenerator): The prompt generator.
            messages (List[str]): The list of messages.
        """

    def can_handle_post_planning(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_planning method.
        Returns:
            bool: True if the plugin can handle the post_planning method."""
        return True

    def post_planning(self, response: str) -> str:
        """This method is called after the planning chat completeion is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """

    def can_handle_pre_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_instruction method.
        Returns:
            bool: True if the plugin can handle the pre_instruction method."""
        return True

    def pre_instruction(self, messages: List[str]) -> List[str]:
        """This method is called before the instruction chat is done.
        Args:
            messages (List[str]): The list of context messages.
        Returns:
            List[str]: The resulting list of messages.
        """

    def can_handle_on_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the on_instruction method.
        Returns:
            bool: True if the plugin can handle the on_instruction method."""
        return True

    def on_instruction(self, messages: List[str]) -> Optional[str]:
        """This method is called when the instruction chat is done.
        Args:
            messages (List[str]): The list of context messages.
        Returns:
            Optional[str]: The resulting message.
        """

    def can_handle_post_instruction(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_instruction method.
        Returns:
            bool: True if the plugin can handle the post_instruction method."""
        return True

    def post_instruction(self, response: str) -> str:
        """This method is called after the instruction chat is done.
        Args:
            response (str): The response.
        Returns:
            str: The resulting response.
        """

    def can_handle_pre_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the pre_command method.
        Returns:
            bool: True if the plugin can handle the pre_command method."""
        return True

    def pre_command(
            self, command_name: str, arguments: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        """This method is called before the command is executed.
        Args:
            command_name (str): The command name.
            arguments (Dict[str, Any]): The arguments.
        Returns:
            Tuple[str, Dict[str, Any]]: The command name and the arguments.
        """

    def can_handle_post_command(self) -> bool:
        """This method is called to check that the plugin can
        handle the post_command method.
        Returns:
            bool: True if the plugin can handle the post_command method."""
        return True

    def post_command(self, command_name: str, response: str) -> str:
        """This method is called after the command is executed.
        Args:
            command_name (str): The command name.
            response (str): The response.
        Returns:
            str: The resulting response.
        """

    def can_handle_chat_completion(
            self,
            messages: list[Dict[Any, Any]],
            model: str,
            temperature: float,
            max_tokens: int,
    ) -> bool:
        """This method is called to check that the plugin can
        handle the chat_completion method.
        Args:
            messages (Dict[Any, Any]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
        Returns:
            bool: True if the plugin can handle the chat_completion method."""
        return True

    def handle_chat_completion(
            self,
            messages: list[Dict[Any, Any]],
            model: str,
            temperature: float,
            max_tokens: int,
    ) -> str:
        """This method is called when the chat completion is done.
        Args:
            messages (Dict[Any, Any]): The messages.
            model (str): The model name.
            temperature (float): The temperature.
            max_tokens (int): The max tokens.
        Returns:
            str: The resulting response.
        """
        return None

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
