# pygico_imagegen/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    BLOG_PATH: str = './blog.txt'
    SERVER_ADDRESS: str = '127.0.0.1:8188'
    GIMP_PATH: str = 'gimp-console-2.10.exe'
    WORKFLOW_PATH: str = './workflow.json'
    OUTPUT_DIR: str = './output'

    model_config = SettingsConfigDict(
        env_file=Path('.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()
