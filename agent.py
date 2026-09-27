import json
from openai import OpenAI
from harness import SafeAgentHarness


LLM_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_course",
            "description": "Search for a course by keyword",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search for a course name or description"
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_schedule",
            "description": "Check the schedule for a specific course by its numeric ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "ID of the course to check"
                    }
                },
                "required": ["course_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "register_course",
            "description": "Register a user for a course. Requires admin role.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "ID of the course"
                    },
                    "user_id": {
                        "type": "integer",
                        "description": "ID of the user registering"
                    }
                },
                "required": ["course_id", "user_id"]
            }
        }
    }
]


class StudentAssistantAgent:
    def __init__(self, user_id: int, model: str = "llama3.2:1b"):
        self.harness = SafeAgentHarness(max_iterations=5)
        self.current_user_id = user_id
        self.model = model

        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )

    def run(self, user_prompt: str):
        self.harness.reset_loop()

        messages = [
            {
                "role": "system",
                "content": (
                    f"You are a helpful university student assistant. "
                    f"The currently logged-in user has user_id={self.current_user_id}. "
                    "Use available tools to find courses and check schedules before answering. "
                    "If a tool call returns an error or permission denial, explain it clearly to the user."
                )
            },
            {"role": "user", "content": user_prompt}
        ]

        print(f"\n[Agent] Starting loop with local Ollama ({self.model})...")

        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=LLM_TOOLS,
                tool_choice="auto"
            )

            assistant_msg = response.choices[0].message
            messages.append(assistant_msg)

            if not assistant_msg.tool_calls:
                return assistant_msg.content

            for tool_call in assistant_msg.tool_calls:
                tool_name = tool_call.function.name

                try:
                    raw_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    raw_args = {}

                print(f"[Agent] Model called tool: '{tool_name}' with args: {raw_args}")

                result = self.harness.execute_tool(
                    tool_name=tool_name,
                    raw_arguments=raw_args,
                    current_user_id=self.current_user_id
                )

                print(f"[System] Harness observation: {result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })