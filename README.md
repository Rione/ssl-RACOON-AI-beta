# RACOON-AI

## Overview

**_NOTE: This instruction is for Ubuntu and MacOS. (Windows need some modification)_**

This is our strategy software for [RoboCup Soccer SSL](https://ssl.robocup.org/)  
`RACOON-AI` stands for Ri-one ssl Accurate Operation AI

### Minimal Requirements

- 64bit machienes (Tested on: x86_64, ARM64)
- Python 3.10.X (We recommend using `pyenv`)
- Poetry (Python's dependency manager)
- GNU Make (`make` command)
- Google Protobuffer Compiler (`protoc`) v3.19.1

---

## Table of Contents

- **[Installation](#installation)**
  - [Prerequisites](#prerequisites)
    - [Setup ssh key](#set-up-ssh-key)
    - [Setup GitHub Command Line Tool](#setup-github-command-line-tool)
    - [Test SSH Connection](#test-ssh-connection)
    - [Setup anyenv](#setup-anyenv)
    - [Setup python 3.10.X](#setup-python-310X)
    - [Setup poetry](#setup-poetry)
  - [Getting Start With RACOON-AI](#getting-start-with-racoon-ai)
    - [Clone RACOON-AI](#clone-racoon-ai)
    - [Install dependencies](#install-dependencies)
    - [Enable Pre-commit hooks](#enable-pre-commit-hooks)
    - [Build RACOON-AI](#build-racoon-ai)
- **[Usage](#usage)**
- **[Related Tools](#related-tools)**

---

# Installation

We know Python version 3.10.X is still in development, isntalling with version management tool is recommended.
Here, we use `pyenv` with `anyenv` since its simplicity.

## Prerequisites

NOTE: On windows, you can use `py` command instead of `pyenv` (with `anyenv`).

- ssh
- [GitHub command line tool](https://github.com/cli/cli) - For working with GitHub (`gh` command)
- [anyenv](https://github.com/anyenv/anyenv) - For managing version management tools
- [pyenv](https://github.com/pyenv/pyenv) - For managing python versions
- [Poetry](https://github.com/python-poetry/poetry) - For managing python dependencies

### Setup `ssh` key

From the security perspective, we recommend to use SSH key.
Please refer to [GitHub documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

1. Generate a Private/Public key

```bash
ssh-keygen -t ed25519 -C "<Your GitHub Email>"
```

2. Add to ssh-agent

On MacOS (10.12.2 or later), you can use Keychain Access to add the key to ssh-agent.
Please add following to your `~/.ssh/config` file.

```text
Host *
  AddKeysToAgent yes
  UseKeychain yes
```

Add the key to ssh-agent.
(Use `-K` option to use Keychain on MacOS.)

```bash
ssh-add ~/.ssh/<Your Key File>
```

**_NOTE:
If you get an error, about the connection to the ssh-agent,
please retry with the following command._**

```bash
eval $(ssh-agent -s) && ssh-add ~/.ssh/<Your Key File>
```

### Setup GitHub Command Line Tool

1. Install GitHub Command Line Tool

Please follow the official [installation](https://github.com/cli/cli#installation).  
On linux see: [Instructions for Linux](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)

2. Login with your GitHub account

_NOTE: Select the `SSH` option, and add your SSH key._

```bash
gh auth login
```

### Test SSH connection

```bash
ssh -T git@github.com
```

### Setup `anyenv`

Since the ease of installation, we recommend using with [anyenv](https://github.com/pyenv/pyenv).
`anyenv` is a tool to manage multiple version management tools, include `pyenv`.
The tool is provided in Homebrew.
If you prefer to use Homebrew, please skip the following steps.

1. Clone `anyenv` from GitHub

```bash
gh repo clone anyenv/anyenv ~/.tools/anyenv
```

2. Set environment variable

Add following to your `~/.zshrc` or `~/.bashrc` file.

```bash:
if [ -d $HOME/.tools/anyenv ]; then
  export PATH="$HOME/.tools/anyenv/bin:$PATH"
  eval "$(anyenv init -)"
fi
```

3. Install manifests

```bash
anyenv install --init git@github.com:anyenv/anyenv-install.git
```

Test the installation:

```bash
anyenv install -l
```

### Setup Python 3.10.X

0. Install build dependencies

Please follow the [Suggested build environment](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)

1. Install `pyenv`

```bash
anyenv install pyenv
```

2. Search for the available versions

```bash
pyenv install -l | grep 3.10
```

3. Install Python

```bash
pyenv install <Your Selected Version>
```

### Setup Poetry

1. Checkout to Python 3.10.x

```bash
pyenv shell <Your Selected Version>
```

2. Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3.10 -
```

Follow the installation guide, and add to your `$PATH`

3. Check if Poetry is installed

```bash
$ poetry --version
> Poetry version X.X.X
```

4. Enable Tab completion (optional)

Guide: https://github.com/python-poetry/poetry#enable-tab-completion-for-bash-fish-or-zsh


## Getting Start With RACOON-AI

### Clone RACOON-AI

Clone to your local workspace.

```bash
gh repo clone Rione-SSL/RACOON-AI ~/ws/racoon-ai && cd $_
```

### Install dependencies

0. (Optional) Activate virtual environment

If you are not in the python3.10 environment, please follow the following

```bash
pyenv shell <Your Selected Version>
```

1. Install dependencies

```bash
poetry install
```

NOTE: If you need extra dependencies, please specify with `-E` option.


### Enable pre-commit hooks

```bash
pre-commit install
```

Used hooks:
- check-yaml
- end-of-file-fixer - Corrected line breaks to be on one line at the end of the file
- mixed-line-ending - Unify line feed code to `LF`
- no-commit-to-branch - Prohibit committing to branches `master`, `main` and `dev` 
- isort - Ordering import
- flake8 - Python code style checker
- pylint - Python code linter
- mypy - Python type checker
- black - Python code formatter
(See also: [Supported hooks - pre-commit](https://pre-commit.com/hooks.html))


### Build RACOON-AI

Compile proto files, and build python package to `dist` directory.

```bash
make
```

---

# Usage

## Execute

```bash
poetry run python -m racoon_ai
```

NOTE: If you are in the virtual environment, you can use `python` instead of `poetry run python`.

---

# Related Tools

- [grSim](https://github.com/RoboCup-SSL/grSim) - Simulator 
- [ssl-game-controller](https://github.com/RoboCup-SSL/ssl-game-controller) - Game controller
- [ssl-vision](https://github.com/RoboCup-SSL/ssl-vision/wiki) - Camera system (only support for Linux)
- [ssl-vision-client](https://github.com/RoboCup-SSL/ssl-vision-client) - Visualizer for `ssl-vision`
- [ssl-autorefs](https://github.com/RoboCup-SSL/ssl-autorefs) - Referee systems
