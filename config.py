from dotenv import load_dotenv
import os


class Config:
    # Load .env first, then .env.local (which will override .env values)
    load_dotenv()  # Load .env
    load_dotenv(".env.local", override=True)  # Load .env.local with override

    def __init__(self) -> None:
        self.port = os.getenv("PORT")
        self.gcp_project_id = os.getenv("GCP_PROJECT_ID")
        self.db_path = os.getenv("DB_PATH")
        self.anthropic_key_path = os.getenv("ANTHROPIC_API_KEY_PATH")
        self.anthropic_model_sonnet = os.getenv("ANTHROPIC_MODEL_SONNET")
        self.anthropic_model_opus = os.getenv("ANTHROPIC_MODEL_OPUS")
        self.github_url = os.getenv("GITHUB_URL", "")
