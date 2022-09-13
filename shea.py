"""
S.H.E.A. (aka Bae)

The simple heuristic entertainment administrator.
"""
import datetime

import discord
from discord.ext import commands
from discord.ext import bridge
import secrets
from datetime import datetime
from datetime import timedelta
import time
import os
import sys
import json
import logging
from logging import handlers
import git

# SHEA modules.
import views

########################################################################################################################
# Configuration.
########################################################################################################################

BOT_VERSION = "0.0.45"
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

# Track initialization time.
INIT_TIME = {
    'unix': int(time.mktime(datetime.now().utctimetuple())),
    'local': datetime.now(),
    'utc': datetime.utcnow()
}

print(f"{BOT_BANNER}")

CONFIG = {}
CONFIG_PATH = 'config.json'

try:
    CONFIG_FILE = open(CONFIG_PATH, 'r')
    CONFIG = json.load(CONFIG_FILE)
    print(f"[INIT]: Loaded configuration file: {CONFIG_PATH}")
except FileNotFoundError:
    print(f"[ERROR] Unable to load configuration file: {CONFIG_PATH}")
    exit(1)

BOT_TOKEN = CONFIG['bot_token']
BOT_NAME = CONFIG['bot_name']

if 'bot_owner' in CONFIG:
    BOT_OWNER = CONFIG['bot_owner']
else:
    BOT_OWNER = None

########################################################################################################################
# INIT
########################################################################################################################

# Configure logging.
_log = logging.getLogger('discord')

try:
    print("[INIT]: Configuring logging.")
    LOG_DIR = CONFIG['log_dir']
    LOG_LEVEL = CONFIG['log_level']
    LOG_FILE = os.path.join(LOG_DIR, f"shea-{str(BOT_NAME).lower()}.log")
    LOG_TIMESTAMP_FORMAT = CONFIG['timestamp_format']
    # Desired format: TIMESTAMP LOGLEVEL USER USER_ID FUNC_NAME?
    logger_format = logging.Formatter('%(asctime)s [%(levelname)s] %(funcName)s: %(message)s',
                                      datefmt=LOG_TIMESTAMP_FORMAT)
    _log.setLevel(LOG_LEVEL)

    # Console log handler.
    if CONFIG['log_stdout']:
        print(f"[INFO]: Enabling logging to console.")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logger_format)
    _log.addHandler(stream_handler)

    # Ensure that LOG_DIR exists.
    try:
        if os.path.exists(LOG_DIR):
            _log.info(f"Log directory already exists: {LOG_DIR}")
        else:
            _log.info(f"Log directory does not exist. Creating: {LOG_DIR}")
            os.makedirs(LOG_DIR, exist_ok=True)
    except OSError:
        _log.info(f"Unable to create log path: {LOG_DIR}")
        exit(2)

    # Rotating log handler.
    file_handler = logging.handlers.TimedRotatingFileHandler(filename=LOG_FILE,
                                                             when='midnight',
                                                             encoding='utf-8',
                                                             atTime=None,
                                                             backupCount=30)
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logger_format)
    _log.addHandler(file_handler)
except Exception as log_config_failure:
    print(f"[CRITICAL]: Failed to configure logging.", log_config_failure)
    exit(1)

# Ensure media directory is present.
MEDIA_DIR = CONFIG['media_dir']

for directory in MEDIA_DIR:
    try:
        if os.path.exists(MEDIA_DIR[directory]):
            _log.debug(f"Media directory already exists: {MEDIA_DIR[directory]}")
        else:
            _log.info(f"Media directory does not exist. Creating {MEDIA_DIR[directory]}")
            os.makedirs(MEDIA_DIR[directory], exist_ok=True)
    except TypeError:
        _log.error(f"Unable to create media directory: {MEDIA_DIR[directory]}")
        exit(1)

# Ensure data directory is present.
DATA_DIR = CONFIG['data_dir']

try:
    if os.path.exists(DATA_DIR):
        _log.debug(f"Data directory already exists: {DATA_DIR}")
    else:
        _log.info(f"Data directory does not exist. Creating {DATA_DIR}")
        os.makedirs(DATA_DIR, exist_ok=True)
except TypeError:
    _log.error(f"Unable to create data directory: {DATA_DIR}")
    exit(1)

########################################################################################################################

_log.info(f"Initializing SHEA as {BOT_NAME}")
intents = discord.Intents(
    guild_reactions=True,
    guilds=True,
    members=True,
    messages=True,
    message_content=True,
    reactions=True
)
bae = bridge.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)


########################################################################################################################
# Events and commands.
########################################################################################################################

@bae.event
async def on_ready():
    _log.info(f"Logged in as {bae.user} (ID: {bae.user.id})")
    # Tell everyone that you're online, SHEA! Only sends to DEBUG channels.
    await startup_message(bae.user)


@bae.event
async def on_error():
    _log.fatal("%s", bae)
    exit(1)


@bae.bridge_command(name="roll")
async def roll(ctx, dice: int, sides: int):
    """Roll the dice."""
    _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) requested a dice roll: Dice: {dice}, Sides: {sides}")
    nice_try = "lol Nice try. :alien: :middle_finger:"
    if dice > 99 or dice < 1 or sides > sys.maxsize or sides < 2:
        await ctx.respond(nice_try)
        _log.warning(f"User {ctx.author.name} (ID: {ctx.author.id}) exceeded dice roll parameters!")
    else:
        ctx.roll_results = []
        await ctx.respond(f"Rolling {dice} dice with {sides} sides for {ctx.author.mention}!")
        for i in range(dice):
            # randbelow() generates a number between 0 and n, so add one.
            roll_result = secrets.randbelow(sides) + 1
            ctx.roll_results.append(roll_result)
        _log.debug(f"User {ctx.author.name} (ID: {ctx.author.id}) got {ctx.roll_results}")
        # Should probably create an embed to display dice rolls.
        roll_output = "Was Lady Luck on your side?\n"
        for i in range(dice):
            roll_output = roll_output + f"\nRoll {i + 1}: {ctx.roll_results[i]}"
        await ctx.respond(f"{roll_output}")


@bae.bridge_command(name="spaghettiwolf")
async def spaghetti_wolf(ctx):
    """Receive a spaghetti wolf."""
    _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) requested spaghetti_wolf")
    image_path = os.path.join(MEDIA_DIR['image'], "spaghetti-wolf")
    file = secrets.choice(os.listdir(image_path))
    file_path = os.path.join(image_path, file)
    # Need to test this. Not sure if it's due to latency or a timeout, but the image fails to send via self.respond().
    # May be due to upload speeds being abysmal at the current time, so an ephemeral response will suffice for now.
    try:
        await ctx.respond("LUPINE PASTA INCOMING", ephemeral=True)
        await ctx.send(file=discord.File(file_path))
        _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) was sent a spaghetti_wolf: {file}")
    except FileNotFoundError:
        await ctx.respond(":spaghetti::wolf: is the best I can do.")
        _log.warning(f"{ctx.author.name} (ID: {ctx.author.id}) requested spaghetti wolf, but it was not found!"
                     f"{file_path}")


@bae.bridge_command(name="ping")
async def ping(ctx):
    """Confirm that the bot is running."""
    _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) sent a ping request")
    time_unix = INIT_TIME['unix']
    msg_time_alive = f"\n\nBy the way: I've been alive since <t:{time_unix}:R>."
    try:
        i = secrets.randbelow(3)
        if i == 0:
            await ctx.respond(
                f"Received ping from {ctx.author.mention}. Ack? {msg_time_alive}", ephemeral=True)
        elif i == 1:
            await ctx.respond(
                f"Yes, I'm here. Thanks for asking, {ctx.author.mention}. {msg_time_alive}", ephemeral=True)
        else:
            await ctx.respond(f"There is no \"why\", {ctx.author.mention}. {msg_time_alive}", ephemeral=True)
        _log.debug(f"{ctx.author.name} (ID: {ctx.author.id}) was sent a reply with uptime. ")
    except Exception as ping_error:
        _log.error(f"Failed to respond to ping from {ctx.author.name} (ID: {ctx.author.id}!", ping_error)


@bae.bridge_command(name="gimmemydata")
async def gimme_my_data(ctx):
    """Request all of your yummy user data. Currently doesn't provide much. Sorry!"""
    _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) requested their user data")
    try:
        user_data = {
            'ctx.author': {
                'ctx.author.name': ctx.author.name,
                'ctx.author.id': ctx.author.id,
                'ctx.author.mention': ctx.author.mention,
            }
        }
        await ctx.respond("```" + json.dumps(user_data, indent=4) + "```", ephemeral=True)
        _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) was sent their user data")
    except Exception as gimme_user_fail:
        _log.error(f"{ctx.author.name} (ID: {ctx.author.id}) did not receive their user data!", gimme_user_fail)


@bae.bridge_command(name="steve")
async def steve(ctx):
    """Steve's stray stuff."""
    if time_lock(ctx, "steve", 15) is True:
        await ctx.respond("You can only handle so much Steve!")
    else:
        _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) requested some Steve")
        image_path = os.path.join(MEDIA_DIR['audio'], "steve")
        file = secrets.choice(os.listdir(image_path))
        file_path = os.path.join(image_path, file)
        try:
            await ctx.respond(file=discord.File(file_path))
            _log.debug(f"{ctx.author.name} (ID: {ctx.author.id}) was sent some Steve: {file}")
        except FileNotFoundError:
            _log.warning(f"{ctx.author.name} (ID: {ctx.author.id}) requested some Steve, but it was not found!"
                         f"{file_path}")
            await ctx.respond(":Steve: is the best I can do.")


@bae.bridge_command(name="explain")
async def explain(ctx):
    """For now just check the README."""
    _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) requested an explanation")
    bot_info = {
        "bot_name": BOT_NAME,
        "bot_version": BOT_VERSION,
        "running_since": f"{INIT_TIME['utc']}Z"
    }
    msg = f"Hi, I'm Bae and I am a work in progress. \n```{json.dumps(bot_info, indent=2)}```"
    await ctx.respond(msg, ephemeral=True)
    _log.debug("Explanation sent.", msg)


@bae.bridge_command(name="buttontest")
async def button_test(self):
    """Provide the buttons. A test of buttons."""
    _log.info(f"{self.author.name} (ID: {self.author.id}) requested some buttons!")
    button_test_view = views.GeneralResponseButtons()
    button_test_view.add_item(views.ButtonLinks.github)
    await self.respond("I provide for thee many buttons!", view=button_test_view, ephemeral=True)


########################################################################################################################
# Administrative commands.
########################################################################################################################

@bae.slash_command()
@commands.has_role("botmaster")
async def clear_locks(ctx):
    """ADMINISTRATOR ONLY: Clear all function locks."""
    _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) requested to clear function locks.")
    await ctx.respond(f"Clearing function locks.")
    lock_file_path = os.path.join(DATA_DIR, 'lock_file.json')
    with open(lock_file_path, 'r') as lock_file:
        _log.debug(f"Opening lock file: {lock_file_path}")
        lock_data = lock_file.read()
        await ctx.respond(f"```{lock_data}```", ephemeral=True)
        _log.debug(f"Closing lock file: {lock_file_path}")
        lock_file.close()
    try:
        os.remove(lock_file_path)
        _log.info(f"Function locks cleared.")
    except OSError:
        _log.error(f"Failed to clear function lock file! {lock_file_path}")


@bae.slash_command()
async def shutdown(ctx):
    """BOT OWNER ONLY: Request remote shutdown."""
    _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) requested remote shutdown.")
    if await bae.is_owner(ctx.guild.owner):
        _log.info(f"Shutting down...")
        await ctx.respond(f"Shutting down...")
        try:
            await bae.close()
        except Exception as shutdown_error:
            _log.fatal("Failed to exit gracefully!", shutdown_error)
            exit(1)
    else:
        _log.warning(f"{ctx.author.name} (ID: {ctx.author.id}) is not guild owner! Warning.")
        await ctx.respond(f"I can't do that, {ctx.author.name}. You aren't the owner of {ctx.guild.name}.")


@bae.slash_command()
@commands.has_role("botmaster")
async def restart(ctx):
    """ADMINISTRATOR ONLY: Request remote restart."""
    await ctx.respond(f"Restarting now!")
    _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) requested restart.")
    restart_bot()


@bae.slash_command()
@commands.has_role("botmaster")
async def update(ctx):
    """ADMINISTRATOR ONLY: Pull the latest version of SHEA."""
    await ctx.respond(f"SHEA update requested by {ctx.author.name}.")
    _log.info(f"{ctx.author.name} (ID: {ctx.author.id}) requested a SHEA update.")

    if time_lock(ctx, "update", 30) is True:
        await ctx.send("An update was run recently. Please wait and try again.")
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
            _log.info(f"Attempting to fetch from origin: {git_remote}:{git_branch}")
            git_remote.fetch()
        except Exception as git_fetch_error:
            _log.info(f"Failed to fetch from origin!", git_fetch_error)
            await ctx.send(f"Failed to fetch from origin!", git_fetch_error)
        try:
            _log.info(f"Attempting to pull from origin: {git_remote}:{git_branch}")
            git_remote.pull()
            git_hash_update = git_repo.head.object.hexsha[:7]
            if git_hash_current != git_hash_update:
                await ctx.send(f"Updated from `{git_hash_current}` to `{git_hash_update}`.")
                git_update_success = True
            else:
                _log.info(f"SHEA `v{BOT_VERSION}@{git_hash_current}` is current. No update required.")
                await ctx.send(f"SHEA `v{BOT_VERSION}@{git_hash_current}` is current. No update required.")
        except Exception as git_update_error:
            await ctx.respond(f"Error during update! Aborting! {git_update_error}")
            _log.error(f"Error during update! Aborting!", git_update_error)

        # Drop GitPython to avoid memory leak.
        _log.debug(f"Closing git repository instance: {git_repo.git}.")
        git_repo.__del__()

        if git_update_success is True:
            _log.info(f"Restarting SHEA to apply update.")
            await ctx.send(f"Restarting SHEA to apply update.")
            restart_bot()


########################################################################################################################
# Other functions.
########################################################################################################################

def restart_bot():
    try:
        os.execv(sys.executable, ['python3'] + sys.argv)
    except Exception as restart_error:
        raise restart_error


async def startup_message(bot_name):
    """Send message to selected channel to announce ready."""
    startup_messages_file = 'media/text/startup-messages.txt'
    if os.path.exists(startup_messages_file):
        if 'startup_message' in CONFIG:
            if CONFIG['startup_message'].lower() != 'false':
                try:
                    prompts = open(startup_messages_file, 'r').read().splitlines()
                    prompt = secrets.choice(prompts)
                except FileNotFoundError:
                    _log.warning(f"{startup_messages_file} not found! Using default message.")
                    prompt = f"Initialization of {bot_name} complete."
                try:
                    for guild in CONFIG['discord_guilds']:
                        debug_channels = CONFIG['discord_guilds'][guild]['channels']['debug']
                        guild_id = CONFIG['discord_guilds'][guild]['id']
                        for debug_channel in debug_channels:
                            _log.info(f"Announcing activation in guild \"{guild}\" (ID: {guild_id}, CHANNEL: "
                                      f"{debug_channel}): \"{prompt}\"")
                            await bae.get_channel(int(debug_channel)).send(f"```{BOT_BANNER}```\n\"{prompt}\"")
                except Exception as announce_error:
                    _log.error(f"Failed to announce activation!", announce_error)
            else:
                _log.info(f"Startup message disabled.")
        else:
            _log.warning(f"Key 'startup_message' not present in {CONFIG_PATH}")
    else:
        _log.warning(f"File {startup_messages_file} could not be found!")


def time_lock(ctx, function_name, delay_in_seconds: int):
    time_locked = False
    lock_file_path = os.path.join(DATA_DIR, 'lock_file.json')
    time_now = datetime.now()
    last_user_id = ctx.author.id
    last_user_name = ctx.author.name

    # If the lock file doesn't exist or is empty, create first entry with this:
    lock_init_dict = {function_name: {"last_run": time_now}}

    # Attempt to open lock file.
    if os.path.isfile(lock_file_path) is True:
        _log.debug(f"Lock file found: {lock_file_path}")
        with open(lock_file_path, 'r') as lock_file:
            _log.debug(f"Opened {lock_file_path}")
            lock_data = json.load(lock_file)
        if function_name in lock_data:
            time_run = datetime.fromisoformat(lock_data[function_name]['last_run'])
            time_delta = time_now - time_run
            if time_delta > timedelta(seconds=delay_in_seconds):
                logging.info(f"Time since last run of {function_name} is > {delay_in_seconds}. Running.")
                lock_data[function_name]["last_run"] = time_now
                lock_data[function_name]["last_user_id"] = last_user_id
                lock_data[function_name]["last_user_name"] = last_user_name
                with open(lock_file_path, 'w') as lock_file:
                    _log.info(f"Writing lock data for {function_name} to {lock_file_path}:\n", json.dumps(lock_data))
                    json.dump(lock_data, lock_file, indent=2, default=str)
            else:
                time_locked = True
                logging.info(f"Time since last run of {function_name} is < {delay_in_seconds}. Not running.")
        else:
            lock_data |= lock_init_dict
            with open(lock_file_path, 'w') as lock_file:
                json.dump(lock_data, lock_file, indent=2, default=str)

    else:
        _log.warning(f"Lock file not found. Creating {lock_file_path}")
        lock_file = open(lock_file_path, 'x+')
        json.dump(lock_init_dict, lock_file, indent=2, default=str)

    lock_file.close()
    _log.debug(f"Closed {lock_file_path}")
    return time_locked


########################################################################################################################
# START SHEA
########################################################################################################################

try:
    _log.info("Attempting login to Discord.")
    bae.run(BOT_TOKEN)
except Exception as e:
    _log.fatal(e)

########################################################################################################################
# END
########################################################################################################################
