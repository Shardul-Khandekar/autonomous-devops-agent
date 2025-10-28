import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import json

from agents.architect import architect_agent
from tools.service_question_tool import service_question_tool
from tasks.vision_tasks import analysis_task
from crewai import Task, Crew, Process

# Initialize FastAPI app
app = FastAPI(
    title="Autonomous DevOps Agent API",
    description="API for analyzing architecture diagrams and generating pipeline questions."
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/analyze-diagram")
async def analyze_diagram(file: UploadFile = File(...)):
    """
    This endpoint:
    1. Receives an uploaded PNG file.
    2. Runs the ArchitectAgent (Agent 1) to get the nodes/edges.
    3. Runs the ServiceQuestionTool to get questions for each node.
    4. Returns a JSON object for the UI to build a form.
    """

    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        # --- Run Agent 1: Architect ---
        task_inputs = {
            'image_path': temp_file_path
        }

        architect_crew = Crew(
            agents=[architect_agent],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=True
        )

        diagram_json_str = architect_crew.kickoff(inputs=task_inputs)
        diagram_data = json.loads(diagram_json_str)

        enriched_nodes = []
        for node in diagram_data.get("nodes", []):
            service_type = node.get("type")
            if service_type:
                questions_json_str = service_question_tool._run(service_type)
                questions = json.loads(questions_json_str)

                node["questions"] = questions
            enriched_nodes.append(node)

        diagram_data["nodes"] = enriched_nodes
        return diagram_data

    except Exception as e:
        return {"error": str(e)}
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)