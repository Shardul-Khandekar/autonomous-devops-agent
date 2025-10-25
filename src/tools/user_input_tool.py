from crewai.tools import BaseTool

class UserInputTool(BaseTool):
    name: str = "Ask User for Input"
    description: str = (
        "Use this tool to ask the user a specific question and get their"
        " answer. The input to this tool should be the question you"
        " want to ask."
    )

    def _run(self, question: str) -> str:
        """
        Pauses the execution and asks the user for input
        """
        print(f"[AGENT QUESTION] {question}")
        answer = input("Your answer: ")
        return answer

user_input_tool = UserInputTool()