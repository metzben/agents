from dotenv import load_dotenv
import os
from secret_manager import SecretManager


class Config:
    # Load .env first, then .env.local (which will override .env values)
    load_dotenv()  # Load .env
    load_dotenv(".env.local", override=True)  # Load .env.local with override

    def __init__(self) -> None:
        self.port = os.getenv("PORT")
        self.db_path = os.getenv("DB_PATH", "data/agents.db")
        self.github_url = os.getenv("GITHUB_URL", "")
        self.gcp_project_id = os.getenv("GCP_PROJECT_ID")

        # Secret Manager integration (optional)
        self.secret_manager = None
        if self.gcp_project_id:
            try:
                self.secret_manager = SecretManager(self.gcp_project_id)
            except Exception as e:
                print(f"Warning: Could not initialize SecretManager: {e}")

        # Example secret paths - customize as needed
        self.api_key_path = os.getenv("API_KEY_PATH")
        self.anthropic_key_path = os.getenv("ANTHROPIC_API_KEY_PATH")
        self.anthropic_model_sonnet = os.getenv("ANTHROPIC_MODEL_SONNET")
        self.anthropic_model_opus = os.getenv("ANTHROPIC_MODEL_OPUS")
        self.gemini_api_key_path = os.getenv("GEMINI_API_KEY_PATH")

    def get_secret(self, secret_path: str) -> str:
        """Get a secret from Google Cloud Secret Manager"""
        if self.secret_manager and secret_path:
            try:
                return self.secret_manager.get_secret(secret_path)
            except Exception as e:
                print(f"Error getting secret from {secret_path}: {e}")
        return None
