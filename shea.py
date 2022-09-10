"""
S.H.E.A. (aka Bae)

The simple heuristic entertainment administrator.
"""
import datetime

import discord
from discord.ext import commands
from discord.ext import bridge
import secrets
from datetime import datetime as time
from datetime import timedelta
import os
import sys
import json
import logging
import git

# SHEA modules.
import views

########################################################################################################################
# Configuration.
########################################################################################################################

BOT_VERSION = "0.0.36"
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

global INIT_TIME

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

if 'bot_owner' in CONFIG:
    BOT_OWNER = CONFIG['bot_owner']
else:
    BOT_OWNER = None

# Configure logging.
LOG_DATE = time.now()
LOG_DIR = CONFIG['log_dir']
LOG_LEVEL = CONFIG['log_level']
LOG_FILE = LOG_DATE.strftime(os.path.join(LOG_DIR, "shea-bae_%Y%m%d.log"))
LOG_TIMESTAMP_FORMAT = CONFIG['timestamp_format']

logger = logging.getLogger('main')

try:
    print(f"[INFO]: Configuring logging.")
    logger.setLevel(LOG_LEVEL)
    # Desired format: TIMESTAMP LOGLEVEL USER USER_ID FUNC_NAME?
    logger_format = logging.Formatter('%(asctime)s [%(levelname)s] %(funcName)s: %(message)s',
                                      datefmt=LOG_TIMESTAMP_FORMAT)
    if CONFIG['log_stdout']:
        print(f"[INFO]: Enabling logging to console.")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logger_format)
        logger.addHandler(stream_handler)
    try:
        if os.path.exists(LOG_DIR):
            logger.info(f"Log directory already exists: {LOG_DIR}")
        else:
            logger.info(f"Log directory does not exist. Creating {LOG_DIR}")
            os.makedirs(LOG_DIR, exist_ok=True)
    except TypeError:
        logger.info(f"Unable to create log path: {LOG_DIR}")
        exit(2)
    file_handler = logging.FileHandler(
        filename=LOG_FILE, encoding='utf-8', mode='a')
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logger_format)
    logger.addHandler(file_handler)
except Exception as log_config_failure:
    print(f"[INFO]: Failed to configure logging.", log_config_failure)
    exit(1)

# Ensure media directory is present.
MEDIA_DIR = CONFIG['media_dir']

for directory in MEDIA_DIR:
    try:
        if os.path.exists(MEDIA_DIR[directory]):
            logger.debug(f"Media directory already exists: {MEDIA_DIR[directory]}")
        else:
            logger.info(f"Media directory does not exist. Creating {MEDIA_DIR[directory]}")
            os.makedirs(MEDIA_DIR[directory], exist_ok=True)
    except TypeError:
        logger.error(f"Unable to create media directory: {MEDIA_DIR[directory]}")
        exit(1)

# Ensure data directory is present.
DATA_DIR = CONFIG['data_dir']

try:
    if os.path.exists(DATA_DIR):
        logger.debug(f"Data directory already exists: {DATA_DIR}")
    else:
        logger.info(f"Data directory does not exist. Creating {DATA_DIR}")
        os.makedirs(DATA_DIR, exist_ok=True)
except TypeError:
    logger.error(f"Unable to create data directory: {DATA_DIR}")
    exit(1)

########################################################################################################################

logger.info(f"Initializing SHEA as {BOT_NAME}")

intents = discord.Intents.default()
bae = bridge.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)


########################################################################################################################
# Events and commands.
########################################################################################################################


@bae.event
async def on_ready():
    global INIT_TIME
    INIT_TIME = time.utcnow()
    logger.info(f"Logged in as {bae.user} (ID: {bae.user.id})")
    # Tell everyone that you're online, SHEA! Only sends to DEBUG channels.
    await startup_prompt(bae.user)


@bae.event
async def on_error():
    logger.fatal("%s", bae)
    exit(1)


@bae.slash_command()
async def gimme_the_buttons(self):
    """Provide the buttons. A test of buttons."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested some buttons!")
    func_view = views.GeneralResponseButtons()
    func_view.add_item(views.ButtonLinks.github)
    await self.respond("I provide for thee many buttons!", view=func_view, ephemeral=True)


@bae.bridge_command()
async def roll(self, dice: int, sides: int):
    """Roll the dice."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested a dice roll: Dice: {dice}, Sides: {sides}")
    nice_try = "lol Nice try. :alien: :middle_finger:"
    if dice > 99 or dice < 1 or sides > sys.maxsize or sides < 2:
        await self.respond(nice_try)
        logger.warning(f"User {self.author.name} (ID: {self.author.id}) exceeded dice roll parameters!")
    else:
        self.roll_results = []
        await self.respond(f"Rolling {dice} dice with {sides} sides for {self.author.mention}!")
        for i in range(dice):
            # randbelow() generates a number between 0 and n, so add one.
            roll_result = secrets.randbelow(sides) + 1
            self.roll_results.append(roll_result)
        logger.debug(f"User {self.author.name} (ID: {self.author.id}) got {self.roll_results}")
        # Should probably create an embed to display dice rolls.
        roll_output = "Was Lady Luck on your side?\n"
        for i in range(dice):
            roll_output = roll_output + f"\nRoll {i + 1}: {self.roll_results[i]}"
        await self.respond(f"{roll_output}")


@bae.bridge_command()
async def spaghetti_wolf(self):
    """Receive a spaghetti wolf."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested spaghetti_wolf")
    image_path = os.path.join(MEDIA_DIR['image'], "spaghetti-wolf")
    file = secrets.choice(os.listdir(image_path))
    file_path = os.path.join(image_path, file)
    try:
        await self.respond(file=discord.File(file_path))
        logger.debug(f"{self.author.name} (ID: {self.author.id}) was sent a spaghetti_wolf: {file}")
    except FileNotFoundError:
        logger.warning(f"{self.author.name} (ID: {self.author.id}) requested spaghetti wolf, but it was not found!"
                       f"{file_path}")
        await self.respond(":spaghetti::wolf: is the best I can do.")


@bae.bridge_command()
async def ping(self):
    """Confirm that the bot is running."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) sent a ping request")
    try:
        i = secrets.randbelow(3)
        if i == 0:
            await self.respond(
                f"Received ping from {self.author.mention}. Ack? \
                \n(Been alive since: {INIT_TIME}Z)")
        elif i == 1:
            await self.respond(
                f"Yes, I'm here. Thanks for asking, {self.author.mention}. \
                \n(Been alive since: {INIT_TIME}Z)")
        else:
            await self.respond(f"There is no \"why\", {self.author.mention}. \
                \n(Been alive since: {INIT_TIME}Z)")
        logger.debug(
            f"{self.author.name} (ID: {self.author.id}) was sent a reply with uptime. (Been alive since: {INIT_TIME}Z)")
    except Exception as ping_error:
        logger.error(f"Failed to respond to ping from {self.author.name} (ID: {self.author.id}!", ping_error)


@bae.slash_command(name="gimme_my_data")
async def gimme_my_data(self):
    """Request all of your yummy user data. Currently doesn't provide much. Sorry!"""
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested their user data")
    try:
        user_data = {
            'self': {
                'self.author.mention': self.author.mention,
                'self.author.id': self.author.id,
                'self.author.name': self.author.name,
            }
        }
        await self.respond("```" + json.dumps(user_data, indent=4) + "```", ephemeral=True)
        logger.info(f"{self.author.name} (ID: {self.author.id}) was sent their user data")
    except Exception as gimme_user_fail:
        logger.error(f"{self.author.name} (ID: {self.author.id}) did not receive their user data!", gimme_user_fail)


@bae.bridge_command()
async def steve(self):
    """Steve's stray stuff."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested some Steve")
    image_path = os.path.join(MEDIA_DIR['audio'], "steve")
    file = secrets.choice(os.listdir(image_path))
    file_path = os.path.join(image_path, file)
    try:
        await self.respond(file=discord.File(file_path))
        logger.debug(f"{self.author.name} (ID: {self.author.id}) was sent some Steve: {file}")
    except FileNotFoundError:
        logger.warning(f"{self.author.name} (ID: {self.author.id}) requested some Steve, but it was not found!"
                       f"{file_path}")
        await self.respond(":Steve: is the best I can do.")


@bae.bridge_command()
async def explain(self):
    """For now just check the README."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested an explanation")
    await self.respond(
        f"I am a work in progress. Currently, I am running `v{BOT_VERSION}`, but one day hope to hit v1.0.0!")


########################################################################################################################
# Administrative commands.
########################################################################################################################

@bae.slash_command()
async def shutdown(self):
    """BOT OWNER ONLY: Request remote shutdown."""
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested remote shutdown.")
    if str(self.author.id) == BOT_OWNER:
        logger.info(f"{self.author.name} (ID: {self.author.id}) is 'bot_owner'. Shutting down.")
        await self.respond(f"Shutting down...")
        try:
            await bae.close()
            print(f"{BOT_NAME} shut down gracefully.")
        except Exception as shutdown_error:
            logger.fatal("Failed to exit gracefully!", shutdown_error)
            exit(1)
    else:
        logger.warning(f"{self.author.name} (ID: {self.author.id}) is not 'bot_owner'! Shutdown denied.")
        await self.respond(f"I can't do that {self.author.name}.")


@bae.slash_command()
@commands.has_role("botmaster")
async def restart(self):
    """ADMINISTRATOR ONLY: Request remote restart."""
    await self.respond(f"Attempting restart.")
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested restart.")
    restart_bot()


@bae.slash_command()
@commands.has_role("botmaster")
async def update(self):
    """ADMINISTRATOR ONLY: Pull the latest version of SHEA."""
    await self.respond(f"SHEA update requested by {self.author.name}.")
    logger.info(f"{self.author.name} (ID: {self.author.id}) requested a SHEA update.")

    if time_lock("update", 30) is True:
        await self.send("Too soon to run an update! Wait 30 seconds.")
    else:
        git_repo = git.Repo('.')
        git_branch = "trunk"
        git_hash_current = git_repo.head.object.hexsha[:7]
        git_update_success = False

        if 'git' in CONFIG:
            git_repo = git.Repo(CONFIG['git']['dir'])
            git_branch = CONFIG['git']['branch']

        git_remote = git_repo.remotes['origin']

        try:
            logger.info(f"Attempting to fetch from origin: {git_remote}:{git_branch}")
            git_remote.fetch()
        except Exception as git_fetch_error:
            logger.info(f"Failed to fetch from origin!", git_fetch_error)
            await self.send(f"Failed to fetch from origin!", git_fetch_error)
        try:
            logger.info(f"Attempting to pull from origin: {git_remote}:{git_branch}")
            git_remote.pull()
            git_hash_update = git_repo.head.object.hexsha[:7]
            if git_hash_current != git_hash_update:
                await self.send(f"Updated from `{git_hash_current}` to `{git_hash_update}`.")
                git_update_success = True
            else:
                logger.info(f"SHEA `v{BOT_VERSION}@`{git_hash_current}` is current. No update required.")
                await self.send(f"SHEA `v{BOT_VERSION}@{git_hash_current}` is current. No update required.")
        except Exception as git_update_error:
            await self.respond(f"Error during update! Aborting! {git_update_error}")
            logger.error(f"Error during update! Aborting!", git_update_error)

        # Drop GitPython to avoid memory leak.
        logger.debug(f"Closing git repository instance: {git_repo.git}.")
        git_repo.__del__()

        if git_update_success is True:
            logger.info(f"Restarting SHEA to apply update.")
            await self.send(f"Restarting SHEA to apply update.")
            restart_bot()


########################################################################################################################
# Other functions.
########################################################################################################################


def restart_bot():
    try:
        os.execv(sys.executable, ['python3'] + sys.argv)
    except Exception as restart_error:
        raise restart_error


async def startup_prompt(bot_name):
    """Send message to selected channel to announce ready."""
    startup_messages_file = 'media/text/startup-messages.txt'
    if os.path.exists(startup_messages_file):
        if 'startup_prompt' in CONFIG:
            if CONFIG['startup_prompt'].lower() != 'false':
                try:
                    prompts = open(startup_messages_file, 'r').read().splitlines()
                    prompt = secrets.choice(prompts)
                except FileNotFoundError:
                    logger.warning(f"{startup_messages_file} not found! Using default message.")
                    prompt = f"Initialization of {bot_name} complete."
                try:
                    for guild in CONFIG['discord_guilds']:
                        debug_channels = CONFIG['discord_guilds'][guild]['channels']['debug']
                        guild_id = CONFIG['discord_guilds'][guild]['id']
                        for debug_channel in debug_channels:
                            logger.info(f"Announcing activation in guild \"{guild}\" (ID: {guild_id}, CHANNEL: "
                                        f"{debug_channel}): \"{prompt}\"")
                            await bae.get_channel(int(debug_channel)).send(f"```{BOT_BANNER}```\n\"{prompt}\"")
                except Exception as announce_error:
                    logger.error(f"Failed to announce activation!", announce_error)
            else:
                logger.info(f"Startup message disabled.")
        else:
            logger.warning(f"\'startup_prompt\' not present in {CONFIG_PATH}")
    else:
        logger.warning(f"File {startup_messages_file} could not be found!")


def time_lock(function_name, delay_in_seconds):
    time_locked = False
    lock_file_path = os.path.join(DATA_DIR, '.lock_file')
    time_now = time.now()

    # Attempt to open lock file.
    if os.path.isfile(lock_file_path) is True:
        logger.debug(f"Lock file found: {lock_file_path}")
        with open(lock_file_path, 'r+') as lock_file:
            lock_data = json.load(lock_file)
            time_run = time.fromisoformat(lock_data[function_name]['last_run'])
            time_delta = time_now - time_run
        if time_delta > timedelta(seconds=delay_in_seconds):
            with open(lock_file_path, 'w') as lock_file:
                logging.debug(f"Time since last run of {function_name} is > {delay_in_seconds}. Running.")
                lock_data[function_name]["last_run"] = time_now
                json.dump(lock_data, lock_file, indent=2, default=str)
        else:
            time_locked = True
            logging.debug(f"Time since last run of {function_name} is < {delay_in_seconds}. Not running.")
    else:
        logger.debug(f"Lock file not found. Creating: {lock_file_path}")
        lock_file = open(lock_file_path, 'x+')
        lock_init_dict = {function_name: {"last_run": time_now}}
        json.dump(lock_init_dict, lock_file, indent=2, default=str)

    lock_file.close()
    return time_locked


########################################################################################################################
# INIT
########################################################################################################################

try:
    logger.info("Attempting login to Discord.")
    bae.run(BOT_TOKEN)
except Exception as e:
    logger.fatal(e)
