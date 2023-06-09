from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define the Task model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean)

# Define the Plan model
class Plan(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True)
    goal = Column(String)
    completed = Column(Boolean)

# DatabaseManager class
class DatabaseManager:
    """
    The DatabaseManager class is responsible for managing the SQL databases. It interacts with the SQLAlchemy ORM to create, update, and retrieve data from the databases.
    """
    def __init__(self, engine):
        """
        Initialize a new DatabaseManager instance.
        Args:
            engine (Engine): The SQLAlchemy engine instance.
        """
        try:
            Base.metadata.create_all(engine)
            self.Session = scoped_session(sessionmaker(bind=engine))
        except Exception as e:
            raise Exception("Failed to initialize DatabaseManager: " + str(e))

    def create_task(self, task):
        """
        Create a new task in the database.
        Args:
            task (Task): The task to be added to the database.
        """
        try:
            session = self.Session()
            session.add(task)
            session.commit()
        except Exception as e:
            raise Exception("Failed to create task: " + str(e))

    def get_task(self, task_id):
        """
        Retrieve a task from the database.
        Args:
            task_id (int): The ID of the task to be retrieved.
        Returns:
            Task: The retrieved task.
        """
        try:
            session = self.Session()
            task = session.query(Task).filter_by(id=task_id).first()
            return task
        except Exception as e:
            raise Exception("Failed to get task: " + str(e))

    def update_task(self, task):
        """
        Update a task in the database.
        Args:
            task (Task): The task to be updated in the database.
        """
        try:
            session = self.Session()
            session.merge(task)
            session.commit()
        except Exception as e:
            raise Exception("Failed to update task: " + str(e))

    def delete_task(self, task_id):
        """
        Delete a task from the database.
        Args:
            task_id (int): The ID of the task to be deleted.
        """
        try:
            session = self.Session()
            task = session.query(Task).filter_by(id=task_id).first()
            session.delete(task)
            session.commit()
        except Exception as e:
            raise Exception("Failed to delete task: " + str(e))

    def create_plan(self, plan):
        """
        Create a new plan in the database.
        Args:
            plan (Plan): The plan to be added to the database.
        """
        try:
            session = self.Session()
            session.add(plan)
            session.commit()
        except Exception as e:
            raise Exception("Failed to create plan: " + str(e))

    def get_plan(self, plan_id):
        """
        Retrieve a plan from the database.
        Args:
            plan_id (int): The ID of the plan to be retrieved.
        Returns:
            Plan: The retrieved plan.
        """
        try:
            session = self.Session()
            plan = session.query(Plan).filter_by(id=plan_id).first()
            return plan
        except Exception as e:
            raise Exception("Failed to get plan: " + str(e))

    def update_plan(self, plan):
        """
        Update a plan in the database.
        Args:
            plan (Plan): The plan to be updated in the database.
        """
        try:
            session = self.Session()
            session.merge(plan)
            session.commit()
        except Exception as e:
            raise Exception("Failed to update plan: " + str(e))

    def delete_plan(self, plan_id):
        """
        Delete a plan from the database.

        Args:
            plan_id (int): The ID of the plan to be deleted.
        """
        try:
            session = self.Session()
            plan = session.query(Plan).filter_by(id=plan_id).first()
            if plan:
                session.delete(plan)
                session.commit()
        except Exception as e:
            raise Exception("Failed to delete plan: " + str(e))

    def mark_task_complete(self, task_id):
        """
        Marks the given task as complete in the database.

        Args:
            task_id (int): The ID of the task to be marked as complete.
        """
        try:
            session = self.Session()
            task = session.query(Task).filter_by(id=task_id).first()
            if task:
                task.completed = True
                session.commit()
        except Exception as e:
            raise Exception("Failed to mark task complete: " + str(e))

    def mark_goal_complete(self, goal):
        """
        Marks the given goal as complete in the database.

        Args:
            goal (str): The goal to be marked as complete.
        """
        try:
            session = self.Session()
            plan = session.query(Plan).filter_by(goal=goal).first()
            if plan:
                plan.completed = True
                session.commit()
        except Exception as e:
            raise Exception("Failed to mark goal complete: " + str(e))

    def update_goals(self):
        """
        Updates the goals to complete the overall goal. This could involve changing the status of the goal, adding new tasks, or other updates as needed.
        """
        try:
            session = self.Session()
            # Retrieve all plans
            plans = session.query(Plan).all()
            for plan in plans:
                # Check if all tasks for this plan are completed
                tasks = session.query(Task).filter_by(plan_id=plan.id).all()
                if all(task.completed for task in tasks):
                    # If all tasks are completed, mark the plan as completed
                    plan.completed = True
            session.commit()
        except Exception as e:
            raise Exception("Failed to update goals: " + str(e))