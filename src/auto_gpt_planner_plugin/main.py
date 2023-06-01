from .database import DatabaseManager
from .planner import Planner
from .tasks import TaskManager
from .utils import Utils

def main():
    """
    The main function of the AutoGPT Planner Plugin.
    """

    # Create a new database
    db_name = "autogpt_planner"
    try:
        engine = Utils.create_database(db_name)
    except Exception as e:
        raise Exception("Failed to create database: " + str(e))

    # Create a new Session
    try:
        session = Utils.create_session(engine)
    except Exception as e:
        raise Exception("Failed to create session: " + str(e))

    # Create a new DatabaseManager
    try:
        db_manager = DatabaseManager(session)
    except Exception as e:
        raise Exception("Failed to create DatabaseManager: " + str(e))

    # Create a new Planner
    try:
        planner = Planner(db_manager)
    except Exception as e:
        raise Exception("Failed to create Planner: " + str(e))

    # Create a new TaskManager
    try:
        task_manager = TaskManager(db_manager)
    except Exception as e:
        raise Exception("Failed to create TaskManager: " + str(e))

    # Start up and run the initial planning cycle
    try:
        planner.initial_planning_cycle()
    except Exception as e:
        raise Exception("Failed to run initial planning cycle: " + str(e))

    # Generate a new plan SQL database to use for future use
    try:
        db_manager.generate_plan_database()
    except Exception as e:
        raise Exception("Failed to generate plan database: " + str(e))

    # Generate task SQL database that contains all task available to the plugin
    try:
        db_manager.generate_task_database()
    except Exception as e:
        raise Exception("Failed to generate task database: " + str(e))

    # Generate a new plan based on the goals given to AutoGPT
    try:
        planner.generate_plan()
    except Exception as e:
        raise Exception("Failed to generate plan: " + str(e))

    # Generate unique task based on the new plan
    try:
        task_manager.generate_tasks()
    except Exception as e:
        raise Exception("Failed to generate tasks: " + str(e))

    # Solve the first task with the highest priority using the solve method
    try:
        task_manager.solve_highest_priority_task()
    except Exception as e:
        raise Exception("Failed to solve highest priority task: " + str(e))

    # Mark the task complete
    try:
        task_manager.mark_task_complete()
    except Exception as e:
        raise Exception("Failed to mark task complete: " + str(e))

    # Update the unique task SQL database
    try:
        db_manager.update_task_database()
    except Exception as e:
        raise Exception("Failed to update task database: " + str(e))

    # Complete tasks until done with a single goal
    try:
        task_manager.complete_tasks()
    except Exception as e:
        raise Exception("Failed to complete tasks: " + str(e))

    # Once all tasks are complete, it marks the goal done
    try:
        planner.mark_goal_done()
    except Exception as e:
        raise Exception("Failed to mark goal done: " + str(e))

    # Once a goal is done, it updates the goals to complete the overall goal
    try:
        planner.update_goals()
    except Exception as e:
        raise Exception("Failed to update goals: " + str(e))

if __name__ == "__main__":
    main()
