from pathlib import Path
from typing import Optional
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
import uuid
import pytest
from config import Config
from secret_manager import SecretManager
from clients.anthropic_client import AnthropicClient

from agent import Agent
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


@pytest.mark.asyncio
async def test_get_request(anthropic_client):
    markdown_file = read_file(".claude/commands/example.md")
    toml_prompt = f"""
    <INSTRUCTIONS>
    Please convert the the `markdown_file` to TOML format.
    </INSTRUCTIONS>
    {markdown_file}
    """
    agent = Agent(
        session_id=str(uuid.uuid4()),
        aclient=anthropic_client,
        tools=[convert_markdown_to_toml_gemini],
        tool_registry=tool_registry,
        max_iters=10,
        timeout=30,
        logger=logger
    )

    result = await agent.run(toml_prompt)
    print(result)
