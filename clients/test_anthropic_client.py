from pathlib import Path
from typing import Optional, Dict, Any
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
import pytest
from config import Config
from secret_manager import SecretManager
from clients.anthropic_client import AnthropicClient
from clients.anthropic_models import (
    Message, AnthropicRequest, ToolChoice, ExecuteToolResult
)
import logging
logger = logging.getLogger()


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


def read_file(file_path: str, encoding: str = "utf-8") -> Optional[str]:
    try:
        return Path(file_path).read_text(encoding=encoding)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return None


@pytest.fixture
def anthropic_client():
    config = Config()
    secret_mgr = SecretManager(config.gcp_project_id)
    model = config.anthropic_model_sonnet
    return AnthropicClient(config, secret_mgr, model)


def test_get_request(anthropic_client):
    markdown_file = read_file(".claude/commands/example.md")
    toml_prompt = f"""
    <INSTRUCTIONS>
    Please convert the the `markdown_file` to TOML format.
    </INSTRUCTIONS>
    {markdown_file}
    """
    message = Message(role="user", content=toml_prompt)

    req = AnthropicRequest(
        model=anthropic_client.model,
        max_tokens=1024,
        messages=[message],
        tools=[tool_convert_markdown_to_toml_gemini],
        tool_choice=ToolChoice(type="auto"),
    )

    resp = anthropic_client.get(req)
    for content in resp.content:
        if hasattr(content, "type") and content.type == "tool_use":
            try:
                result = execute_tool(content.name, content.input)
                print(result)
            except Exception as e:
                print(f"Tool call failed with: {str(e)}")


session_id = "123-testing"


def execute_tool(
        tool_name: str,
        tool_input: Dict[str, Any]
) -> ExecuteToolResult:

    if tool_name not in tool_registry:
        available_tools = ", ".join(tool_registry.keys())
        raise ValueError(f"""Tool '{tool_name}' not found.
        Available tools: {available_tools}
        """)
    tool = tool_registry[tool_name]
    try:
        logger.info(
            "Executing tool:",
            extra={
                "tool_name": tool_name,
                "tool_arguments": list(tool_input.keys())
            }
        )
        result = tool(**tool_input)
        logger.info(
            "Tool execution completed:",
            extra={
                "tool_name": tool_name,
                "session_id": session_id,
            }
        )
        return ExecuteToolResult(
            success=True,
            tool_name=tool_name,
            session_id=session_id,
            tool_result=result
        )
    except TypeError as e:
        error_msg = f"Invalid params for tool: '{tool_name}': {str(e)}"
        logger.error(
            "Tool execution failed: invalid params",
            extra={
                "tool_name": tool_name,
                "session_id": session_id,
                "error": error_msg
            }
        )
        return ExecuteToolResult(
            success=False,
            tool_name=tool_name,
            session_id=session_id,
            error_msg=error_msg,
            tool_result=None
        )
    except Exception as e:
        error_msg = f"Tool '{tool_name}' execution failed: {str(e)}"
        logger.error(
            "Tool execution failed",
            extra={
                "tool_name": tool_name,
                "session_id": session_id,
                "error": error_msg,
                "error_type": type(e).__name__
            }
        )
        return ExecuteToolResult(
            success=False,
            tool_name=tool_name,
            session_id=session_id,
            error_msg=error_msg,
            tool_result=None
        )


def _execute_tool(tool_name: str, tool_input: Dict[str, Any]) -> str:
    tool_registry = {
        "convert_markdown_to_toml_gemini": convert_markdown_to_toml_gemini}
    if tool_name == "convert_markdown_to_toml_gemini":
        markdown_doc = tool_input["markdown_doc"]
        model = tool_input.get("model", "gemini-2.5-flash")

    result = tool_registry[tool_name](markdown_doc, model)
    return result
