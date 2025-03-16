import os
import disnake
from disnake.ext import commands

from utils import (
    setup_logger,
    load_all_cogs,
    load_and_verify_env,
)

def main():
    load_and_verify_env()
    setup_logger()
    
    intents = disnake.Intents.all()
    bot = commands.InteractionBot(
        intents=intents,
        owner_ids=set([int(str_id) for str_id in os.environ["OWNER_IDS"].split(",")]), 
        reload=os.getenv("RELOAD", "False") == "True",
    )
    
    load_all_cogs(bot)
    
    bot.run(os.environ["BOT_TOKEN"])


if __name__ == "__main__":
    main()
