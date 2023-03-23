from pathlib import Path
from pydantic import BaseSettings, ValidationError, validator
from loguru import logger
from json import JSONDecodeError


class Settings(BaseSettings):
    api_token: str = ""
    name: str = ""
    base_dir: Path = Path(__file__).parent.parent.parent
    log_dir: Path | str = ""
    db_dir: Path | str = ""
    admins: list[int | None] = []
    users: list[int | None] = []

    @validator("log_dir", "db_dir")
    def validate_fullpath(cls, v: str, values: dict) -> Path:
        return Path(values["base_dir"] / v)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_config(path: Path) -> Settings:
    try:
        logger.debug(f"Log file path - {path}")
        config = Settings.parse_file(path)
        create_tech_dirs([config.log_dir, config.db_dir])
        logger.debug("Settings file was loads correctly.")
        return config
    except (FileNotFoundError, ValidationError):
        logger.critical("Settings file 'settings.json' not found or corrupt!")
        exit()
    except JSONDecodeError:
        logger.critical("Something went wrong when load 'settings.json' file!")
        exit()


def create_tech_dirs(dirs: list[Path]) -> None:
    for dir in dirs:
        if not dir.exists():
            dir.mkdir(parents=True)
