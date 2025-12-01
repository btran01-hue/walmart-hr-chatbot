"""Configuration management for the HR Chatbot."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Regular OpenAI (for simple setup)
    use_azure_openai: bool = True
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    # Walmart Element GenAI LLM Gateway (or Azure OpenAI)
    azure_openai_endpoint: str = "https://dummy.com"
    azure_openai_api_key: str = "dummy"
    azure_openai_deployment_name: str = "gpt-4.1-mini@2025-04-14"
    azure_openai_api_version: str = "2024-10-21"

    # Microsoft List
    microsoft_list_url: str

    # CORS
    allowed_origins: str = "http://localhost:3000"

    # Chatbot behavior
    confidence_threshold: float = 0.7
    max_tokens: int = 500
    temperature: float = 0.7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


settings = Settings()
