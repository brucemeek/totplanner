from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()

# Define the Task model
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean)

# TaskManager class
class TaskManager:
    """
    The TaskManager class is responsible for managing tasks. It interacts with the tasks database,
    allowing for tasks to be created, updated, and retrieved.
    """

    def __init__(self, engine):
        """
        Initialize a new TaskManager instance.

        Args:
            engine: The SQLAlchemy engine object.
        """
        self.engine = engine
        Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def create_task(self, task):
        """
        Create a new task in the database.

        Args:
            task (Task): The task to be added to the database.
        """
        session = self.Session()
        try:
            session.add(task)
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception("Failed to create task: " + str(e))

    def get_task(self, task_id):
        """
        Retrieve a task from the database.

        Args:
            task_id (int): The ID of the task to be retrieved.

        Returns:
            Task: The retrieved task.
        """
        session = self.Session()
        task = session.query(Task).filter_by(id=task_id).first()
        if task is None:
            raise Exception(f"Task with id {task_id} does not exist")
        return task

    def update_task(self, task):
        """
        Update a task in the database.

        Args:
            task (Task): The task to be updated in the database.
        """
        session = self.Session()
        try:
            session.merge(task)
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception("Failed to update task: " + str(e))

    def delete_task(self, task_id):
        """
        Delete a task from the database.

        Args:
            task_id (int): The ID of the task to be deleted.
        """
        session = self.Session()
        task = session.query(Task).filter_by(id=task_id).first()
        if task is None:
            raise Exception(f"Task with id {task_id} does not exist")
        try:
            session.delete(task)
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception("Failed to delete task: " + str(e))

    def get_all_tasks(self):
        """
        Retrieve all tasks from the database.

        Returns:
            List[Task]: The list of all tasks.
        """
        session = self.Session()
        tasks = session.query(Task).all()
        if tasks is None:
            raise Exception("Failed to retrieve tasks")
        return tasks

    def get_incomplete_tasks(self):
        """
        Retrieve all incomplete tasks from the database.

        Returns:
            List[Task]: The list of all incomplete tasks.
        """
        session = self.Session()
        tasks = session.query(Task).filter_by(completed=False).all()
        if tasks is None:
            raise Exception("Failed to retrieve incomplete tasks")
        return tasks

    def mark_task_complete(self, task_id):
        """
        Mark a task as complete in the database.

        Args:
            task_id (int): The ID of the task to be marked as complete.
        """
        session = self.Session()
        task = session.query(Task).filter_by(id=task_id).first()
        if task is None:
            raise Exception(f"Task with id {task_id} does not exist")
        try:
            task.completed = True
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception("Failed to mark task as complete: " + str(e))

    def get_highest_priority_task(self):
        """
        Retrieve the highest priority task from the database.

        Returns:
            Task: The highest priority task.
        """
        session = self.Session()
        task = session.query(Task).filter_by(completed=False).order_by(Task.priority.desc()).first()
        if task is None:
            raise Exception("No incomplete tasks found")
        return task

    def complete_tasks_for_goal(self, goal_id):
        """
        Complete all tasks associated with a single goal.

        Args:
            goal_id (int): The ID of the goal.
        """
        session = self.Session()
        tasks = session.query(Task).filter_by(goal_id=goal_id).all()
        if tasks is None:
            raise Exception(f"No tasks found for goal id {goal_id}")
        for task in tasks:
            try:
                task.completed = True
                session.commit()
            except Exception as e:
                session.rollback()
                raise Exception("Failed to complete tasks for goal: " + str(e))

    def update_goals_for_overall_goal(self, overall_goal_id):
        """
        Update the goals in the plan database to complete the overall goal.

        Args:
            overall_goal_id (int): The ID of the overall goal.
        """
        # This method will depend on how your goals are structured in your database.
        # You'll need to implement this method based on your specific requirements.
        pass
