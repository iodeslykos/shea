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
import sys
import json
import logging

# Global variables and logging configuration.

shea_version = "0.0.2"

try:
    CONFIG_FILE = open('config.json', 'r')
    CONFIG = json.load(CONFIG_FILE)
except TypeError:
    print(f"[ERROR] Unable to load configuration file: \'config.json\'")
    exit(1)

LOG_DATE = time.now()
LOG_DIR = CONFIG['log_dir']
LOG_LEVEL = CONFIG['log_level']
LOG_FILE = LOG_DATE.strftime(os.path.join(LOG_DIR, "shea-bae_%Y%m%d.log"))
LOG_TIMESTAMP_FORMAT = CONFIG['timestamp_format']

try:
    os.makedirs(LOG_DIR, exist_ok=True)
except TypeError:
    print(f"[ERROR]: Unable to create log path: {LOG_DIR}")
    exit(2)

logger = logging.getLogger('shea_bae')
logger.setLevel(LOG_LEVEL)
file_handler = logging.FileHandler(
    filename=LOG_FILE, encoding='utf-8', mode='a')
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - :[%(levelname)s] %(message)s', datefmt=LOG_TIMESTAMP_FORMAT))
logger.addHandler(file_handler)

BOT_TOKEN = CONFIG['bot_token']

MEDIA_DIR = CONFIG['media_dir']
for directory in MEDIA_DIR:
    try:
        os.makedirs(MEDIA_DIR[directory], exist_ok=True)
    except TypeError:
        print(f"[ERROR] Unable to create media directory: {MEDIA_DIR[directory]}")
        exit(1)


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
async def dice_roll(self, dice: int, sides: int):
    """Rolls the dice."""
    nice_try = f"I can't do that, {self.author.mention}."
    if dice > 25 or sides > sys.maxsize:
        await self.respond(nice_try)
        logger.warning(f"User {self.author}'s request was out of bounds: DICE: {dice}, SIDES: {sides}.")
    else:
        self.roll_results = []
        for i in range(dice):
            roll_result = random.randint(1, sides)
            self.roll_results.append(roll_result)
        for i in range(dice):
            await self.respond(f"Die #{i+1}: {self.roll_results[i]}")
            sleep(0.25)


@bae.slash_command()
async def roll(self, dice: int, sides: int):
    """Roll the dice."""
    nice_try = "lol Nice try. :alien: :middle_finger:"
    if dice > 25 or sides > sys.maxsize:
        await self.respond(nice_try)
        logger.warning(f"{self.author.mention}'s request was out of bounds: DICE: {dice}, SIDES: {sides}.")
    else:
        self.roll_results = []
        for i in range(dice):
            roll_result = random.randint(1, sides)
            self.roll_results.append(roll_result)
        await self.respond(f"Rolling {dice} dice with {sides} sides for {self.author.mention}!")
        for i in range(dice):
            await self.respond(f"Die #{i+1}: {self.roll_results[i]}")
            sleep(0.5)


@bae.command(name="spaghetti_wolf")
async def spaghetti_wolf(self):
    """Receive a spaghetti wolf."""
    logger.info(f"{self.author.id} requested spaghetti_wolf")
    try:
        image_path = os.path.join(MEDIA_DIR['image'], "_spaghetti_wolf.png")
        await self.send(file=discord.File(image_path))
    except FileNotFoundError:
        logger.warning(f"{self.author.id} requested spaghetti wolf, but it was not found!")
        await self.respond(":spaghetti::wolf: is the best I can do.")
    finally:
        sleep(0.5)


@bae.slash_command()
async def spaghetti_wolf(self):
    """Receive a spaghetti wolf."""
    logger.info(f"{self.author.id} requested spaghetti_wolf")
    try:
        image_path = os.path.join(MEDIA_DIR['image'], "_spaghetti_wolf.png")
        await self.respond(file=discord.File(image_path))
    except FileNotFoundError:
        logger.warning(f"{self.author.id} requested spaghetti wolf, but it was not found!")
        await self.respond(":spaghetti::wolf: is the best I can do.")
    finally:
        sleep(0.5)


@bae.command(name="ping")
async def ping(self):
    """Confirm that the bot is running."""
    await self.send(f"Received ping from {self.author.mention}. Ack?")


@bae.slash_command(name="ping")
async def ping(self):
    f"""Confirm that the bot is running."""
    i = random.randint(0, 1)
    if i == 0:
        await self.respond(f"Received ping from {self.author.mention}. Ack?")
    elif i == 1:
        await self.respond(f"Yes, I'm here. Thanks for asking, {self.author.mention}.")
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
