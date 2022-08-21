# SHEA (a.k.a. "Bae")

## Overview.

### The simple heuristic entertainment administrator.

This one's simple: A Discord bot initially dreamt of to serve the needs of the Feature Film Friday Posse. What will it become? No idea. But even if it doesn't grow to contain an exhaustive set of features, we hope it will serve its purpose.

## Installation.

#### A quick note:

Being as this project is wholly written in Python3, we'd recommend installation of Python3. If you do not currently have a Python3 interpreter installed and do not know how to accomplish this, visit [the documentation for Python3](https://wiki.python.org/moin/BeginnersGuide) or call the cops, because you might be in trouble.

Inside of [`requirements.txt`](requirements.txt) you'll find a list of requirements (just as the file name implies).

We recommend creating a virtual environment since--after all--this Python we're dealing with. Stuff breaks.

```
# python3 -m venv ".venv"
# pip3 install -r requirements.txt
```

Before running SHEA for the first time, create a copy of config.json.example, remove the `.example` suffix, and then configure to your liking. You will need to acquire a Discord API key at the very least.

## Features / Roadmap.

- [ ] Spaghetti wolf.
- [ ] Film selection.
  - [ ] Create lists of submissions on a per-user basis.
    - [ ] Allow users to add, remove, and prioritize their selections.
- [ ] Determine if user is present/allow a "raised hand" to signal participation. 
- [ ] Better logging with adjustable verbosity.
- [ ] Administrative commands and overrides.

### Wishlist.

- Ability to query and display plot synopses, ratings, and service where films are hosted.

## License.

The contents of this repository are covered under the MIT standard license. See [`LICENSE.md`](LICENSE.md) for details.

## Issues & Contributions.

Should you desire to contribute to or complain about the contents of this repository, feel free to open an Issue or submit a Pull Request. Additionally, we are open to the idea of expanding SHEA's functionality should any new ideas arise

Though we cannot guarantee your satisfaction, all submissions will be considered.
