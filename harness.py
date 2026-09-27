from pydantic import ValidationError
from tools import search_course, check_schedule, register_course, USERS
from schemas import SearchCourseInput, CheckScheduleInput, RegisterCourseInput

TOOL_PERMISSIONS = {
    "search_course": ["student", "admin"],
    "check_schedule": ["student", "admin"],
    "register_course": ["admin"]  # Strict permission rule
}

TOOL_REGISTRY = {
    "search_course": {
        "func": search_course,
        "schema": SearchCourseInput
    },
    "check_schedule": {
        "func": check_schedule,
        "schema": CheckScheduleInput
    },
    "register_course": {
        "func": register_course,
        "schema": RegisterCourseInput
    },
}


class SafeAgentHarness:
    def __init__(self, max_iterations=5):
        self.max_iterations = max_iterations
        self.iteration_count = 0

    def check_permission(self, user_id: int, tool_name: str) -> bool:
        user = USERS.get(user_id)
        if not user:
            return False

        user_role = user["role"]
        allowed_roles = TOOL_PERMISSIONS.get(tool_name, [])
        return user_role in allowed_roles

    def execute_tool(self, tool_name: str, raw_arguments: dict, current_user_id: int):
        self.iteration_count += 1
        if self.iteration_count > self.max_iterations:
            return {
                "success": False,
                "error": f"Max iteration limit ({self.max_iterations}) reached. Stopping execution."
            }

        if tool_name not in TOOL_REGISTRY:
            return {
                "success": False,
                "error": f"Unknown tool requested: {tool_name}"
            }

        if not self.check_permission(current_user_id, tool_name):
            return {
                "success": False,
                "error": f"Permission denied: Your role cannot execute '{tool_name}'."
            }

        tool_config = TOOL_REGISTRY[tool_name]
        schema_class = tool_config["schema"]
        func = tool_config["func"]

        try:
            validated_inputs = schema_class(**raw_arguments)
        except ValidationError as e:
            return {
                "success": False,
                "error": "Input validation failed. Please correct your arguments.",
                "details": str(e)
            }

        try:
            result = func(validated_inputs)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": "The tool encountered an internal error during execution.",
                "details": str(e)
            }

    def reset_loop(self):
        self.iteration_count = 0