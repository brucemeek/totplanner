from .database import DatabaseManager
from .tasks import TaskManager

class Planner:
    def __init__(self):
        """
        Initializes the Planner class and creates new instances of the TaskManager and DatabaseManager.
        """
        self.task_manager = TaskManager()
        self.database_manager = DatabaseManager()

    def run_initial_planning_cycle(self):
        """
        Runs the initial planning cycle. This involves generating a new plan and task database, creating tasks based on the plan, and starting the execution of tasks.
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
        Generates a new task database that contains all tasks available to the plugin. This database will not be overwritten.
        """
        result = self.database_manager.create_task_database()
        if result is None:
            raise Exception("Failed to generate task database")
        return result

    def generate_plan(self, goals):
        """
        Generates a new plan based on the given goals.
        """
        if not isinstance(goals, list):
            raise TypeError("Goals must be a list")
        return self.task_manager.generate_plan(goals)

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
        Solves the task with the highest priority using the solve method.
        """
        if not isinstance(task, dict):
            raise TypeError("Task must be a dictionary")
        required_keys = ["id", "description", "priority", "completed"]
        if not all(key in task for key in required_keys):
            raise ValueError(f"Task is missing one or more required keys: {required_keys}")
        return self.task_manager.solve_task(task)

    def mark_task_complete(self, task):
        """
        Marks the given task as complete.
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
        Completes all tasks for a single goal.
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
        Marks the given goal as complete.
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
