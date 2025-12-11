from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    app_env: str = "local"
    app_name: str = "DocuMind AI"
    app_port: int = 8000

    gemini_api_key: str = ""  # Will be required when we use Gemini
    gemini_model_name: str = "gemini-2.5-flash"
    gemini_embed_model: str = "models/embedding-001"

    database_url: str = "postgresql+psycopg://user:pass@localhost:5432/documind"  # Optional for now
    vector_db_dir: str = "./vector_store"
    aws_region: str = "us-east-1"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = AppSettings()