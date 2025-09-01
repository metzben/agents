from clients.anthropic_client import AnthropicClient
import logging
from clients.anthropic_models import Message, Tool, ExecuteToolResult
from typing import List, Optional, Dict, Any
import uuid
from clients.tools import (
    tool_convert_markdown_to_toml_gemini,
    tool_convert_markdown_to_toml_claude_code,
    tool_validate_toml,
    tool_process_errors_claude,
    convert_markdown_to_toml_gemini,
    convert_markdown_to_toml_claude_code,
    validate_toml,
    process_errors_claude
)

tools = [
    tool_convert_markdown_to_toml_gemini,
    tool_convert_markdown_to_toml_claude_code,
    tool_validate_toml,
    tool_process_errors_claude,
]

tool_registry = {
    "convert_markdown_to_toml_gemini": convert_markdown_to_toml_gemini,
    "convert_markdown_to_toml_claude_code": convert_markdown_to_toml_claude_code,
    "validate_toml": validate_toml,
    "process_errors_claude": process_errors_claude,
}


class Agent:
    def __init__(
        self,
        session_id: Optional[str],
        aclient: AnthropicClient,
        tools: List[Tool],
        tool_registry: Dict[str, Any],
        max_iters: int = 20,
        timout: int = 300,
        logger: logging.Logger = None
    ) -> None:
        self.session_id = session_id or str(uuid.uuid4())
        self.aclient = aclient
        self.tools = tools
        self.tool_registry = tool_registry
        self.max_iters = max_iters
        self.timout = timout
        self.messages: List[Message] = []
        self.logger = logger or logging.getLogger(__name__)

    async def run(self, prompt: str):
        print(prompt)

    def execute_tool(
            self,
            tool_name: str,
            tool_input: Dict[str, Any]
    ) -> ExecuteToolResult:

        if tool_name not in self.tool_registry:
            available_tools = ", ".join(self.tool_registry.keys())
            raise ValueError(f"""Tool '{tool_name}' not found.
            Available tools: {available_tools}
            """)
        tool = self.tool_registry[tool_name]
        try:
            self.logger.info(
                "Executing tool:",
                extra={
                    "tool_name": tool_name,
                    "session_id": self.session_id,
                    "tool_arguments": list(tool_input.keys())
                }
            )
            result = tool(**tool_input)
            self.logger.info(
                "Tool execution completed:",
                extra={
                    "tool_name": tool_name,
                    "session_id": self.session_id,
                }
            )
            return ExecuteToolResult(
                success=True,
                tool_name=tool_name,
                session_id=self.session_id,
                tool_result=result
            )
        except TypeError as e:
            error_msg = f"Invalid params for tool: '{tool_name}': {str(e)}"
            self.logger.error(
                "Tool execution failed: invalid params",
                extra={
                    "tool_name": tool_name,
                    "session_id": self.session_id,
                    "error": error_msg
                }
            )
            return ExecuteToolResult(
                success=False,
                tool_name=tool_name,
                session_id=self.session_id,
                error_msg=error_msg,
                tool_result=None
            )
        except Exception as e:
            error_msg = f"Tool '{tool_name}' execution failed: {str(e)}"
            self.logger.error(
                "Tool execution failed",
                extra={
                    "tool_name": tool_name,
                    "session_id": self.session_id,
                    "error": error_msg,
                    "error_type": type(e).__name__
                }
            )
            return ExecuteToolResult(
                success=False,
                tool_name=tool_name,
                session_id=self.session_id,
                error_msg=error_msg,
                tool_result=None
            )
