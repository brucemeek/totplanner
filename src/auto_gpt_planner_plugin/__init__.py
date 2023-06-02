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
        """This method is called just after the generate_prompt is called,
            but actually before the prompt is generated.
        Args:
            prompt (PromptGenerator): The prompt generator.
        Returns:
            PromptGenerator: The prompt generator.
        """

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
