import os
import openai
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean


from .tasks import TaskManager
from .database import DatabaseManager

Base = declarative_base()

class Planner:
    """
    The Planner class is responsible for managing the planning process. It interacts with the tasks and plan databases,
    allowing for tasks and plans to be created, updated, and retrieved.
    """

    def __init__(self, engine, task_manager=None):
        """
        Initialize a new Planner instance.

        Args:
            engine: The SQLAlchemy engine object.
            task_manager: An optional TaskManager instance. If not provided, a new one will be created.
        """
        self.engine = engine
        Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.task_manager = task_manager or TaskManager(engine)
        self.database_manager = DatabaseManager(engine)


    def run_initial_planning_cycle(self):
        """
        Run the initial planning cycle. This involves generating a new plan and task database, creating tasks based on the plan,
        and starting the execution of tasks.
        """
        # Generate plan and task databases
        if not self.generate_plan_database():
            raise Exception("Failed to generate plan database")
        if not self.generate_task_database():
            raise Exception("Failed to generate task database")

        # Generate plan and tasks
        plan = self.generate_plan()
        if not plan:
            raise Exception("Failed to generate plan")
        tasks = self.generate_tasks(plan)
        if not tasks:
            raise Exception("Failed to generate tasks")

        # Start execution of tasks
        for task in tasks:
            if not self.solve_task(task):
                raise Exception(f"Failed to solve task {task.id}")
            if not self.mark_task_complete(task):
                raise Exception(f"Failed to mark task {task.id} as complete")

    def generate_plan_database(self):
        """
        Generates a new plan database for future use.
        """
        result = self.database_manager.create_plan_database()
        if result is None:
            raise Exception("Failed to generate plan database")
        return result

    def generate_task_database(self):
        """
        Generate a new task database that contains all tasks available to the plugin. This database will not be overwritten.
        """
        result = self.database_manager.create_task_database()
        if result is None:
            raise Exception("Failed to generate task database")
        return result

    def construct_plan_prompt(self, goals):
        """
        Construct the plan prompt based on the given goals.

        Args:
            goals: The goals to be achieved.

        Returns:
            str: The constructed plan prompt.
        """
        if not isinstance(goals, list):
            raise TypeError("Goals must be a list")

        plan_prompt = "# Project Plan\n\n"

        # Append goals section
        plan_prompt += "## Goals:\n"
        for index, goal in enumerate(goals, start=1):
            plan_prompt += f"{index}. {goal}\n"
        plan_prompt += "\n"

        # Append tasks section
        plan_prompt += "## Tasks:\n"
        tasks = self.task_manager.get_all_tasks()  # Assuming you have a method to get all tasks
        for task in tasks:
            completed_status = "[x]" if task.completed else "[ ]"
            plan_prompt += f"- {completed_status} {task.description}\n"
        plan_prompt += "\n"

        # Append revised plan section
        plan_prompt += "## Revised Plan:\n\n"

        return plan_prompt

    def generate_plan(self, goals):
        """
        Generate a new plan based on the given goals. Includes generating an improved plan using ChatCompletion.

        Args:
            goals: The goals to be achieved.

        Returns:
            Plan: The generated plan.
        """
        if not isinstance(goals, list):
            raise TypeError("Goals must be a list")

        tasks = self.task_manager.get_all_tasks()  # Get all tasks

        prompt = self.construct_plan_prompt(goals, tasks)  # Pass the tasks to construct_plan_prompt

        model = os.getenv('PLANNER_MODEL', os.getenv('FAST_LLM_MODEL', 'gpt-3.5-turbo'))
        max_tokens = os.getenv('PLANNER_TOKEN_LIMIT', os.getenv('FAST_TOKEN_LIMIT', 1500))
        temperature = os.getenv('PLANNER_TEMPERATURE', os.getenv('TEMPERATURE', 0.5))

        # Call the OpenAI API for chat completion
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that improves and adds crucial points to plans in .md format.",
                },
                {
                    "role": "user",
                    "content": f"Update the following plan given the task status below, keep the .md format:\n{prompt}\n"
                               f"Include the current tasks in the improved plan, keep mind of their status and track them "
                               f"with a checklist:\n{tasks}\n Revised version should comply with the contents of the "
                               f"tasks at hand:",
                },
            ],
            max_tokens=int(max_tokens),
            n=1,
            temperature=float(temperature),
        )

        # Extract the improved plan from the response
        improved_plan = response.choices[0].message.content.strip()
        return improved_plan

    def generate_tasks(self, plan):
        """
        Generates unique tasks based on the new plan.
        """
        if not isinstance(plan, list):
            raise TypeError("Plan must be a list of tasks")
        if not plan:
            return []
        for task in plan:
            if not isinstance(task, dict):
                raise ValueError("Each task in the plan must be a dictionary")
            required_keys = ["id", "description", "priority", "completed"]
            if not all(key in task for key in required_keys):
                raise ValueError(f"A task in the plan is missing one or more required keys: {required_keys}")
        return self.task_manager.generate_tasks(plan)


    def solve_task(self, task):
        """
        Solve the task with the highest priority using the solve method.

        Args:
            task (Task): The task to be solved.
        """
        if not isinstance(task, dict):
            raise TypeError("Task must be a dictionary")
        required_keys = ["id", "description", "priority", "completed"]
        if not all(key in task for key in required_keys):
            raise ValueError(f"Task is missing one or more required keys: {required_keys}")
        return self.task_manager.solve_task(task)

    def mark_task_complete(self, task):
        """
        Mark the given task as complete.

        Args:
            task (Task): The task to be marked as complete.
        """
        if not isinstance(task, dict):
            raise TypeError("Task must be a dictionary")
        required_keys = ["id", "description", "priority", "completed"]
        if not all(key in task for key in required_keys):
            raise ValueError(f"Task is missing one or more required keys: {required_keys}")
        return self.task_manager.mark_task_complete(task)

    def update_task_database(self):
        """
        Updates the unique task database.
        """
        result = self.database_manager.update_task_database()
        if result is None:
            raise Exception("Failed to update task database")
        return result

    def complete_tasks_for_goal(self, goal):
        """
        Complete all tasks associated with a single goal.

        Args:
            goal (Goal): The goal to complete tasks for.
        """
        if not isinstance(goal, str):
            raise TypeError("Goal must be a string")
        tasks = self.task_manager.get_tasks_for_goal(goal)
        for task in tasks:
            if not self.solve_task(task):
                raise Exception(f"Failed to solve task {task['id']}")
            if not self.mark_task_complete(task):
                raise Exception(f"Failed to mark task {task['id']} as complete")

    def mark_goal_complete(self, goal):
        """
        Mark the given goal as complete.

        Args:
            goal (Goal): The goal to be marked as complete.
        """
        if not isinstance(goal, str):
            raise TypeError("Goal must be a string")
        result = self.database_manager.mark_goal_complete(goal)
        if result is None:
            raise Exception(f"Failed to mark goal '{goal}' as complete")
        return result

    def update_goals(self):
        """
        Updates the goals to complete the overall goal.
        """
        result = self.database_manager.update_goals()
        if result is None:
            raise Exception("Failed to update goals")
        return result
    
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
        Generate tasks based on the current plan and save them to the database.
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
        Retrieve a task based on its ID.

        Args:
            task_id (int): The ID of the task to be retrieved.

        Returns:
            Task: The retrieved task.
        """
        try:
            return self.task_manager.get_task(task_id)
        except Exception as e:
            raise Exception("Failed to get task: " + str(e))