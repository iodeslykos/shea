# SHEA (a.k.a. "Bae")

**Simple Heuristic Entertainment Administrator**

## Overview.

This one's simple: A Discord bot initially dreamt up to serve the needs of the Feature Film Friday Posse. What will it become? No idea. But even if it doesn't grow to contain an exhaustive set of features, we hope it will serve its purpose.

## Installation.

> ##### A quick note:
> Being as this project is wholly written in Python3, we'd recommend installation of Python3. If you do not currently have a Python3 interpreter installed and do not know how to accomplish this, visit and read [the documentation for Python3](https://wiki.python.org/moin/BeginnersGuide). Or call the cops, *because you might be in trouble*.

### Setup.

We recommend creating a virtual environment since--after all--this Python we're dealing with. Stuff breaks.

There are two methods provided for setup.

#### Method 1: `Makefile` (Preferred)

To create a Python3 virtual environment and install all require modules, simply run:

```
make setup
```

To upgrade Python3 modules:

```
make upgrade
```

To remove the virtual environment and before running `make setup` again:

```
make clean
```

#### Method 2: `setup-venv.sh`

Running the [`setup-venv.sh`](scripts/setup-venv.sh) script included in this repository will automatically create a virtual environment and install the required packages for you.

```
./scripts/setup-venv.sh
```

Once the virtual environment is successfully created, you may activate it with the following command: 

`source .venv/bin/activate`

### Configuration.

Before running SHEA for the first time, create a copy of config.json.example, rename it to `config.json`, and then configure the contents to your liking.

You will need to specify a Discord API key at the very least. 

For more information, please visit the [Discord Developer Portal](https://discord.com/developers/docs/intro).



## Features / Roadmap.

- [X] Spaghetti wolf :spaghetti::wolf:.
- [X] Virtual environment installer for easy setup. 
- [ ] Feature Film Friday functionality.
- [ ] Better logging with adjustable verbosity and rotation.
- [ ] Administrative commands, overrides, and remote update capability.
- [ ] Better documentation and installation instructions.
  - [ ] `config.json` explanation.
  - [X] Explain installation options: `make` or `setup-venv.sh`.

### Wishlist.

- Ability to query and display plot synopses, ratings, and a list of services where requested content is available to stream.
- Image generation: fractals, quote cards, etc.
- Return dice rolls as an image instead of text block.
- Text-to-speech and other audio in voice channels.

## License.

The contents of this repository are covered under the MIT standard license. See [`LICENSE`](LICENSE) for details.

## Issues & Contributions.

Should you desire to contribute to or complain about the contents of this repository, feel free to open an Issue or submit a Pull Request. Additionally, we are open to the idea of expanding SHEA's functionality and welcome any requests or recommendations.

Though we cannot guarantee your satisfaction, all submissions will be considered.
