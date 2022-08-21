"""
S.H.E.A. (aka Bae)

The simple heuristic entertainment administrator.
"""

import discord
from discord.ext import commands
import random
from datetime import datetime as time
import os
import json
import logging

# Global variables and logging configuration.

shea_version = "0.0.1"

CONFIG_FILE = open('config.json', 'r')
CONFIG = json.load(CONFIG_FILE)

BOT_TOKEN = CONFIG['bot_token']

LOG_DATE = time.now()
LOG_DIR = CONFIG['log_dir']
LOG_LEVEL = logging.DEBUG
LOG_FILE = LOG_DATE.strftime(os.path.join(LOG_DIR, "shea-bae_%Y%m%d.log"))
LOG_TIMESTAMP_FORMAT = CONFIG['timestamp_format']

try:
    os.makedirs(LOG_DIR, exist_ok=True)
except TypeError:
    print("[ERROR]: Unable to create log path.")
    exit(2)

logger = logging.getLogger('shea_bae')
logger.setLevel(LOG_LEVEL)
file_handler = logging.FileHandler(
    filename=LOG_FILE, encoding='utf-8', mode='a')
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - :[%(levelname)s] %(message)s', datefmt=LOG_TIMESTAMP_FORMAT))
logger.addHandler(file_handler)


########################################################################################################################

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bae = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)


@bae.event
async def on_ready():
    print(f"Logged in as {bae.user} (ID: {bae.user.id}")
    logger.info(f"Logged in as {bae.user} (ID: {bae.user.id}")


@bae.event
async def on_error():
    print(f"%s", bae)
    logger.fatal("%s", bae)
    exit(1)


@bae.command(name="roll")
async def dice_roll(self, n: int, x: int):
    self.roll_results = []
    for i in range(n - 1):
        roll_result = random.randrange(x)
        self.roll_results.append(roll_result)
    await self.send(self.roll_results)


@bae.command(name="spaghetti_wolf")
async def spaghetti_wolf(self):
    await self.send("`insert spaghetti wolf here`")


@bae.command(name="ping")
async def ping(self):
    await self.send(f"Received ping from {self.author.mention}. Ack?")


########################################################################################################################

description = """
SHEA: The simple heuristic entertainment administrator.

A Discord bot designed to help with the alignment and selection of films for the Feature Film Friday Posse of the Shea \
Discord Guild.
"""

# Commence.

try:
    bae.run(BOT_TOKEN)
except Exception as e:
    logger.fatal(e)
