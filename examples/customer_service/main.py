import shlex
import argparse
from src.swarm.swarm import Swarm
from src.tasks.task import Task
from configs.general import Colors, test_file_path, engine
from src.validator import validate_all_tools, validate_all_assistants
from src.arg_parser import parse_args

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("description", nargs='?', type=str, help="Description of the task.")
    parser.add_argument("--evaluate", action="store_true", help="Set the evaluate flag for the new task.")
    parser.add_argument("--iterate", action="store_true", help="Set the iterate flag for the new task.")
    parser.add_argument("--assistant", type=str, help="Specify the assistant for the new task.")

    return parser

def main():
    args = parse_args()

    # Initialize the Swarm instance
    swarm = Swarm(engine=args.engine)

    # Load predefined tasks if any
    swarm.load_tasks()

    # Deploy the Swarm for predefined tasks
    swarm.deploy()

    # Interactive mode for adding tasks
    while True:
        print("Enter a task (or 'exit' to quit):")
        task_input = input()

        # Check for exit command
        if task_input.lower() == 'exit':
            break

        # Use shlex to parse the task description and arguments
        task_args = shlex.split(task_input)
        task_parser = argparse.ArgumentParser()
        task_parser.add_argument("description", type=str, nargs='?', default="")
        task_parser.add_argument("--iterate", action="store_true", help="Set the iterate flag for the new task.")
        task_parser.add_argument("--evaluate", action="store_true", help="Set the evaluate flag for the new task.")
        task_parser.add_argument("--assistant", type=str, default="user_interface", help="Specify the assistant for the new task.")

        # Parse the task arguments
        task_parsed_args = task_parser.parse_args(task_args)

        # Create and add the new task
        new_task = Task(description=task_parsed_args.description,
                        iterate=task_parsed_args.iterate,
                        evaluate=task_parsed_args.evaluate,
                        assistant=task_parsed_args.assistant)
        swarm.add_task(new_task)
        print(swarm.tasks)

        # Deploy the Swarm with the new task
        swarm.deploy()

if __name__ == "__main__":
    main()
