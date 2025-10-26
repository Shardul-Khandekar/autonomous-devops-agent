from crewai import Task
from agents.surveyor import surveyor_agent
from tasks.vision_tasks import analysis_task

query_task = Task(
    description=(
        "You have been given a JSON object with 'nodes' and 'edges' from the"
        " Architect. Your job is to create a new, enriched list of services."
        "\n\nHere is your workflow for EACH node in the 'nodes' list:"
        "\n1. Get the node's 'type' (e.g., 'Lambda', 'S3', 'ALB')."
        "\n2. Use your 'Get Questions for Service Type' tool to find out"
        "    what questions to ask for that *specific* type."
        "\n3. If the tool returns an empty list [], you don't need to ask"
        "    anything. Just copy the node's 'id' and 'type' to your final"
        "    list."
        "\n4. If the tool returns a list of questions, use your 'Ask User"
        "    for Input' tool to ask the user *each* question, one by one."
        "\n5. Collect all the answers for that node and add them to your"
        "    final list, along with the original 'id' and 'type'."
    ),
    expected_output=(
        "A single, enriched JSON array of all services. Each service"
        " must include its original 'id' and 'type'. If questions were"
        " asked, it must also include the user's answers."
        "\n\nExample:\n"
        "[\n"
        "  {\n"
        "    \"id\": \"lambda_processor\",\n"
        "    \"type\": \"Lambda\",\n"
        "    \"source_code_directory\": \"./src/my-function\",\n"
        "    \"runtime\": \"python3.11\",\n"
        "    \"build_command\": \"pip install -r requirements.txt\",\n"
        "    \"test_command\": \"pytest\"\n"
        "  },\n"
        "  {\n"
        "    \"id\": \"public_alb\",\n"
        "    \"type\": \"ALB\"\n"
        "  }\n"
        "]"
    ),
    agent=surveyor_agent,
    context=[analysis_task]  # To receive context and JSON from the architect
)