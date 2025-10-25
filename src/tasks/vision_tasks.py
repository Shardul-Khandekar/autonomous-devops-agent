from crewai import Task
from agents.architect import architect_agent

analysis_task = Task(
    description=(
        "Analyze the architecture diagram located at '{image_path}'."
        " Use your 'Architecture Diagram Analyzer' tool to extract all"
        " nodes and edges into a clean JSON format."
    ),
    expected_output=(
        "A single JSON object containing 'nodes' and 'edges' keys."
        " This JSON must be clean and ready for parsing, with no"
        " extra conversational text or markdown formatting."
    ),
    agent=architect_agent
)
