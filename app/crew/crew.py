# This file contains the task functions that are used to run, train, replay, and test the crew.
import sys
from app.crew.agents_tasks import LeadProcessingCrew

def run(inputs):
    """
    Run the crew with dynamic inputs.
    """
    result = LeadProcessingCrew().crew().kickoff(inputs=inputs)
    return result

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"feature": "As a user, I want to add items to a shopping cart."}
    try:
        LeadProcessingCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LeadProcessingCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"feature": "As a user, I want to add items to a shopping cart."}
    try:
        LeadProcessingCrew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
