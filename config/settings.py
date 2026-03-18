import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    google_api_key: str = os.getenv("GOOGLE_API_KEY")
    model_name: str = os.getenv("MODEL_NAME")
    temperature: float = 0.4

    # UI config
    app_title: str = "Bullet — Script Intelligence"
    app_icon: str = "🎬"
    max_script_length: int = 10_000

settings = Settings()
