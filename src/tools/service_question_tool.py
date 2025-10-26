from crewai.tools import BaseTool
from openai import OpenAI
import json

from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# Prompt template for generating service-related questions
QUESTION_GENERATOR_PROMPT = """
    You are a world-class, expert-level DevOps Solutions Architect.
    Your *only* job is to generate a list of questions needed to build a CI/CD pipeline for a specific cloud service.

    The user will provide a service type (e.g., "Lambda", "S3", "ALB").
    You must return a JSON list of simple, single-line questions.

    It is critical that you decide based on the service type what questions to ask, focusing on build and deployment steps.
    Here are some guidelines:

    - For compute services (like Lambda, ECS_Task, EC2), ask for source code,
    runtime, and build/test commands.
    - For services like S3 (if used for static hosting), ask for the
    build output directory.
    - For services like ALB, SQS, SNS, or CloudFront, no build/deploy
    steps are needed, so return an EMPTY list [].

    RULES:
    1.  Return *ONLY* the JSON list. No other text or explanation.
    2.  If no questions are needed, return an empty list: [].

    EXAMPLES:
    Input: Lambda
    Output:
    [
    "What is the source code directory for this Lambda? (e.g., './src/my-function')",
    "What is the runtime for this Lambda? (e.g., 'python3.11', 'nodejs20.x')",
    "What is the build command for this Lambda? (e.g., 'pip install -r requirements.txt')",
    "What is the test command for this Lambda? (e.g., 'pytest')"
    ]

    Input: ALB
    Output:
    []

"""

class ServiceQuestionTool(BaseTool):
    name: str = "Get Questions for Service Type"
    description: str = (
        "Use this tool to generate a list of necessary questions for"
        " a specific service type (e.g., 'Lambda', 'S3'). The input to this"
        " tool must be the 'type' string from the node."
    )

    def _run(self, service_type: str) -> str:
        """
        Dynamically generates questions by calling an LLM.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": QUESTION_GENERATOR_PROMPT},
                    {"role": "user", "content": service_type}
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
            )

            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Error generating questions for {service_type}: {e}")
            return "[]"  # Return empty list on error
        

# Instantiate the tool
service_question_tool = ServiceQuestionTool()