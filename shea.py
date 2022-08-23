"""
S.H.E.A. (aka Bae)

The simple heuristic entertainment administrator.
"""

import discord
from discord.ext import commands
from discord.ext import bridge
import secrets
from datetime import datetime as time
from time import sleep
import os
import sys
import json
import logging

########################################################################################################################
# Configuration.
########################################################################################################################

BOT_VERSION = "0.0.10"
BOT_BANNER = (f"""  _________ ___ ______________   _____   
 /   _____//   |   \\_   _____/  /  _  \\  
 \\_____  \\/    ~    \\    __)_  /  /_\\  \\ 
 /        \\    Y    /        \\/    |    \\
/_______  /\\___|_  /_______  /\\____|__  /
        \\/       \\/        \\/         \\/
Simple Heuristic Entertainment Administrator 
v{BOT_VERSION}
""")

# Commence!

print(f"{BOT_BANNER}")

CONFIG = {}
CONFIG_PATH = 'config.json'

try:
    CONFIG_FILE = open(CONFIG_PATH, 'r')
    CONFIG = json.load(CONFIG_FILE)
    print(f"[INFO]: Loaded configuration file: \'{CONFIG_PATH}\'")
except FileNotFoundError:
    print(f"[ERROR] Unable to load configuration file: \'{CONFIG_PATH}\'")
    exit(1)

BOT_TOKEN = CONFIG['bot_token']
BOT_NAME = CONFIG['bot_name']

LOG_DATE = time.now()
LOG_DIR = CONFIG['log_dir']
LOG_LEVEL = CONFIG['log_level']
LOG_FILE = LOG_DATE.strftime(os.path.join(LOG_DIR, "shea-bae_%Y%m%d.log"))
LOG_TIMESTAMP_FORMAT = CONFIG['timestamp_format']

try:
    if os.path.exists(LOG_DIR):
        print(f"[INFO]: Log directory already exists: {LOG_DIR}")
    else:
        print(f"[INFO]: Log directory does not exist. {LOG_DIR} Creating...")
        os.makedirs(LOG_DIR, exist_ok=True)
except TypeError:
    print(f"[ERROR]: Unable to create log path: {LOG_DIR}")
    exit(2)

try:
    print(f"[INFO]: Configuring logging.")
    logger = logging.getLogger('main')
    logger.setLevel(LOG_LEVEL)
    logger_format = logging.Formatter('%(asctime)s [%(levelname)s] %(funcName)s: %(message)s',
                                      datefmt=LOG_TIMESTAMP_FORMAT)
    file_handler = logging.FileHandler(
        filename=LOG_FILE, encoding='utf-8', mode='a')
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logger_format)
    logger.addHandler(file_handler)
    if CONFIG['log_stdout']:
        print(f"[INFO]: Enabling logging to console.")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logger_format)
    logger.addHandler(stream_handler)
except Exception as log_config_failure:
    print(f"[INFO]: Failed to configure logging.", log_config_failure)

MEDIA_DIR = CONFIG['media_dir']

for directory in MEDIA_DIR:
    try:
        if os.path.exists(MEDIA_DIR[directory]):
            print(f"[INFO]: Media directory already exists: {MEDIA_DIR[directory]}")
        else:
            print(f"[INFO]: Media directory does not exist. {MEDIA_DIR[directory]} Creating...")
            os.makedirs(MEDIA_DIR[directory], exist_ok=True)
    except TypeError:
        print(f"[ERROR] Unable to create media directory: {MEDIA_DIR[directory]}")
        exit(1)


########################################################################################################################

print(f"[INFO]: Initializing SHEA as {BOT_NAME}")

intents = discord.Intents.default()
bae = bridge.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

########################################################################################################################
# Events and commands.
########################################################################################################################


@bae.event
async def on_ready():
    print(f"[ OK ]: Logged in as {bae.user} (ID: {bae.user.id})")
    logger.info(f"Logged in as {bae.user} (ID: {bae.user.id})")


@bae.event
async def on_error():
    print(f"%s", bae)
    logger.fatal("%s", bae)
    exit(1)


@bae.bridge_command()
async def roll(self, dice: int, sides: int):
    """Roll the dice."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested a dice roll: Dice: {dice}, Sides: {sides}")
    nice_try = "lol Nice try. :alien: :middle_finger:"
    if dice > 25 or dice < 1 or sides > sys.maxsize or sides < 1:
        await self.respond(nice_try)
        logger.warning(f"User {self.author.name} (ID: {self.author.id}) requested too many dice!")
    else:
        self.roll_results = []
        await self.respond(f"Rolling {dice} dice with {sides} sides for {self.author.mention}!")
        for i in range(dice):
            # randbelow() generates a number between 0 and n, so add one.
            roll_result = secrets.randbelow(sides) + 1
            self.roll_results.append(roll_result)
        logger.debug(f"User {self.author.name} (ID: {self.author.id}) got {self.roll_results}")
        for i in range(dice):
            await self.respond(f"Die #{i+1}: {self.roll_results[i]}")
            sleep(0.5)


@bae.bridge_command()
async def spaghetti_wolf(self):
    """Receive a spaghetti wolf."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested spaghetti_wolf")
    try:
        image_path = os.path.join(MEDIA_DIR['image'], "_spaghetti_wolf.png")
        await self.respond(file=discord.File(image_path))
        logger.debug(f"{self.author.name} (ID: {self.author.id}) was sent a spaghetti_wolf")
    except FileNotFoundError:
        logger.warning(f"{self.author.name} (ID: {self.author.id}) requested spaghetti wolf, but it was not found!")
        await self.respond(":spaghetti::wolf: is the best I can do.")
    finally:
        sleep(0.5)


@bae.bridge_command()
async def ping(self):
    f"""Confirm that the bot is running."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) sent a ping request")
    try:
        i = secrets.randbelow(3)
        if i == 0:
            await self.respond(f"Received ping from {self.author.mention}. Ack?")
        elif i == 1:
            await self.respond(f"Yes, I'm here. Thanks for asking, {self.author.mention}.")
        else:
            await self.respond(f"There is no \"why\", {self.author.mention}.")
        logger.debug(f"{self.author.name} (ID: {self.author.id}) was sent a reply.")
    except Exception as ping_error:
        logger.error(f"Failed to respond to ping from {self.author.name} (ID: {self.author.id}!", ping_error)


@bae.slash_command(name="gimme_my_data")
async def gimme_my_data(self):
    """Request all of your yummy user data."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested their user data")
    try:
        user_data = {
            'self': {
                'self.author.mention': self.author.mention,
                'self.author.id': self.author.id,
                'self.author.name': self.author.name,
            }
        }
        await self.respond("```" + json.dumps(user_data, indent=4) + "```")
        logger.info(f"{self.author.name} (ID: {self.author.id} was sent their user data")
    except Exception as gimme_user_fail:
        logger.error(f"{self.author.name} (ID: {self.author.id}) did not receive their user data!", gimme_user_fail)


@bae.bridge_command()
async def explain(self):
    """For now just check the README."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested an explanation")
    await self.respond(f"There is no \"why\".")

########################################################################################################################
# INIT
########################################################################################################################

try:
    print(f"[INFO]: Attempting login to Discord.")
    bae.run(BOT_TOKEN)
except Exception as e:
    logger.fatal(e)
