import argparse
from crewai import Crew, Process
from langfuse import get_client
import openlit

from agents.architect import architect_agent
from tasks.vision_tasks import analysis_task

from agents.surveyor import surveyor_agent
from tasks.query_tasks import query_task

# Initialize Langfuse callback handler
langfuse = get_client()

if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

# Initialize openlit
openlit.init()


def run_crew(image_path: str):
    """
        Initializes and runs the Crew with the provided image path
    """
    # Create a dictionary to pass the image_path to the task
    inputs = {'image_path': image_path}

    # Instantiate the Crew with the tasks module
    autonomous_crew = Crew(
        agents=[architect_agent, surveyor_agent],
        tasks=[analysis_task, query_task],
        process=Process.sequential,
        verbose=True
    )

    # Run the Crew with the provided inputs
    print(f"Starting crew to analyze: {image_path}\n")
    result = autonomous_crew.kickoff(inputs=inputs)

    print("Crew completed. Final output:")
    print(result)


if __name__ == "__main__":

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Run the autonomous DevOps agent crew."
    )

    parser.add_argument(
        "image_path",
        type=str,
        help="The file path to the architecture diagram PNG."
    )
    args = parser.parse_args()

    run_crew(args.image_path)
