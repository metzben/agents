from config import Config
from secret_manager import SecretManager
from clients.anthropic_models import AnthropicRequest, AnthropicResponse
import requests


class AnthropicClient:
    def __init__(
        self,
        config: Config,
        secret_mgr: SecretManager,
        model: str,
    ) -> None:
        self.config = config
        self.secret_mgr = secret_mgr
        self.model = model
        self.headers = self.build_headers()

    def build_headers(self) -> dict:
        anthropic_key = self.secret_mgr.get_secret(self.config.anthropic_key_path)

        return {
            "x-api-key": anthropic_key,
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "prompt-tools-2025-04-02",
        }

    def get(self, request: AnthropicRequest) -> AnthropicResponse:
        try:
            data = request.model_dump(exclude_none=True)
            url = "https://api.anthropic.com/v1/messages"
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            response_data = response.json()

            resp = AnthropicResponse(**response_data)
            return resp
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to send request to Anthropic API: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error in get method: {str(e)}")
