from pydantic import BaseSettings


class Settings(BaseSettings):
    debug = True
    app_title = "cryptography"
    log_level = "INFO"

    class Config:
        case_sensitive = False
        env_file = '../.env'
        env_file_encoding = 'utf-8'


config = Settings()
