import base64
from openai import OpenAI
from crewai.tools import BaseTool

from config import OPENAI_API_KEY

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Prompt template for vision tasks
VISION_PROMPT = """
Analyze this architecture diagram. Your goal is to identify every service
and the connections between them.

Output your findings as a simple JSON object with two keys:
1.  "nodes": A list of all identified services. Each item should be an
    object with "id" (a unique name, e.g., "lambda_processor") and 
    "type" (e.g., "Lambda", "S3", "SQS").
2.  "edges": A list of all connections. Each item should be an
    object with "from" (the id of the source service) and "to"
    (the id of the target service).

Example:
{
  "nodes": [
    { "id": "s3_bucket_source", "type": "S3" },
    { "id": "lambda_processor", "type": "Lambda" }
  ],
  "edges": [
    { "from": "s3_bucket_source", "to": "lambda_processor" }
  ]
}

JSON Response:
"""


def _encode_image(image_path: str) -> str:
    """Helper function to encode a local image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class VisionTool(BaseTool):
    name: str = "Architecture Diagram Analyzer"
    description: str = "Analyzes a PNG image of an architecture diagram and returns a JSON representation of its nodes and edges."

    def _run(self, image_path: str) -> str:
        """
        Tools main execution method. It takes a file path, encodes the image, and sends it to the vision model.
        """
        try:
            base64_image = _encode_image(image_path)

            # Pass the image and prompt to the OpenAI vision model
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": VISION_PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=1024,
            )

            # Return only the text content from the response
            return response.choices[0].message.content

        except FileNotFoundError:
            return f"Error: The file at {image_path} was not found."
        except Exception as e:
            return f"Error processing image: {str(e)}"


vision_tool = VisionTool()
