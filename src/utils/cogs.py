import os

from custom_types import AnyBot


def load_commands(bot: AnyBot):
    """Load extensions from src/miron/extensions/commands directory

    Args:
        bot (AnyBot): The bot instance
    """
    for filename in os.listdir("src/miron/extensions/commands"):
        if filename.endswith(".py") and not filename.startswith("__"):
            bot.load_extension(f"miron.extensions.commands.{filename[:-3]}")


def load_events(bot: AnyBot):
    """Load extensions from src/miron/extensions/events directory

    Args:
        bot (AnyBot): The bot instance
    """
    for filename in os.listdir("src/miron/extensions/events"):
        if filename.endswith(".py") and not filename.startswith("__"):
            bot.load_extension(f"miron.extensions.events.{filename[:-3]}")


def load_all_cogs(bot: AnyBot):
    """Load extensions from src/miron/extensions/commands and src/miron/extensions/events directories

    Args:
        bot (AnyBot): The bot instance
    """
    load_commands(bot)
    load_events(bot)
