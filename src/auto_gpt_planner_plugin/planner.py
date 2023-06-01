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
        self.generate_plan_database()
        self.generate_task_database()

        # Generate plan and tasks
        plan = self.generate_plan()
        tasks = self.generate_tasks(plan)

        # Start execution of tasks
        for task in tasks:
            self.solve_task(task)

    def generate_plan_database(self):
        """
        Generates a new plan database for future use.
        """
        self.database_manager.create_plan_database()

    def generate_task_database(self):
        """
        Generates a new task database that contains all tasks available to the plugin. This database will not be overwritten.
        """
        self.database_manager.create_task_database()

    def generate_plan(self, goals):
        """
        Generates a new plan based on the given goals.
        """
        return self.task_manager.generate_plan(goals)

    def generate_tasks(self, plan):
        """
        Generates unique tasks based on the new plan.
        """
        return self.task_manager.generate_tasks(plan)

    def solve_task(self, task):
        """
        Solves the task with the highest priority using the solve method.
        """
        self.task_manager.solve_task(task)

    def mark_task_complete(self, task):
        """
        Marks the given task as complete.
        """
        self.task_manager.mark_task_complete(task)

    def update_task_database(self):
        """
        Updates the unique task database.
        """
        self.database_manager.update_task_database()

    def complete_tasks_for_goal(self, goal):
        """
        Completes all tasks for a single goal.
        """
        tasks = self.task_manager.get_tasks_for_goal(goal)
        for task in tasks:
            self.solve_task(task)
            self.mark_task_complete(task)

    def mark_goal_complete(self, goal):
        """
        Marks the given goal as complete.
        """
        self.database_manager.mark_goal_complete(goal)

    def update_goals(self):
        """
        Updates the goals to complete the overall goal.
        """
        self.database_manager.update_goals()