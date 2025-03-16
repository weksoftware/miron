import os
from dotenv import load_dotenv


def load_env(dotenv_path: str = ".env"):
    """Load environment variables from .env file

    Args:
        dotenv_path (str, optional): Path to .env file. Defaults to ".env".
    """
    load_dotenv(dotenv_path)


def verify_env():
    """Verify required environment variables

    Raises:
        ValueError: If any of the required environment variables is not set
    """
    required_environment_variables = ["BOT_TOKEN", "TASKS_API_TOKEN", "OWNER_IDS"]

    for variable in required_environment_variables:
        if not os.getenv(variable):
            raise ValueError(f"{variable} is not set")


def load_and_verify_env(dotenv_path: str = ".env"):
    """Load environment variables from .env file and verify required

    Args:
        dotenv_path (str, optional): Path to .env file. Defaults to ".env".
    """
    load_env(dotenv_path)
    verify_env()
