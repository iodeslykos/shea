"""
S.H.E.A. (aka Bae)

The simple heuristic entertainment administrator.
"""

import discord
from discord.ext import commands
import random
from datetime import datetime as time
from time import sleep
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
    print(f"Logged in as {bae.user} (ID: {bae.user.id})")
    logger.info(f"Logged in as {bae.user} (ID: {bae.user.id})")


@bae.event
async def on_error():
    print(f"%s", bae)
    logger.fatal("%s", bae)
    exit(1)


@bae.command(name="roll")
async def dice_roll(self, n: int, x: int):
    nice_try = f"I can't do that, {self.author.mention}."
    if n > 25 or x > 9999999999:
        await self.respond(nice_try)
    else:
        self.roll_results = []
        for i in range(n):
            roll_result = random.randint(1, x)
            self.roll_results.append(roll_result)
        for i in range(n):
            await self.send(f"Die #{i+1}: {self.roll_results[i]}")
            sleep(0.5)


@bae.slash_command()
async def roll(self, n: int, x: int):
    nice_try = "lol Nice try. :alien: :middle_finger:"
    if n > 25:
        await self.respond(nice_try)
    if x > 9999999999:
        await self.respond(nice_try)
    else:
        self.roll_results = []
        for i in range(n):
            roll_result = random.randint(1, x)
            self.roll_results.append(roll_result)
        await self.respond(f"Rolling {n} dice with {x} sides for {self.author.mention}!")
        for i in range(n):
            await self.respond(f"Die #{i+1}: {self.roll_results[i]}")
            sleep(0.5)


@bae.command(name="spaghetti_wolf")
async def spaghetti_wolf(self):
    await self.send("`insert spaghetti wolf here`")


@bae.slash_command()
async def spaghetti_wolf(self):
    await self.respond(":spaghetti::wolf:")
    await self.respond("^^^ Placeholder until I learn to attach images.")


@bae.command(name="pingg")
async def ping(self):
    await self.send(f"Received ping from {self.author.mention}. Ack?")


@bae.slash_command(name="ping")
async def ping(self):
    i = random.randint(0, 1)
    if i == 0:
        await self.respond(f"Received ping from {self.author.mention}. Ack?")
    elif i == 1:
        await self.respond(f"Yes, I'm here {self.author.mention}.")
    else:
        await self.respond(f"There is no \"why\", {self.author.mention}.")

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
