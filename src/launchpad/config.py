from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = Field(default='Project Launchpad')
    max_file_size_bytes: int = Field(default=1_000_000)
    default_scan_root: str = Field(default='.')
    report_limit: int = Field(default=50)


settings = Settings()
