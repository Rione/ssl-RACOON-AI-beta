# RACOON-AI

## Overview

**_NOTE: This instruction is for Linux (Ubuntu) and MacOS. (Windows need some modification)_**

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

- **[Installation](/INSTALL.md)**
  - [Prerequisites](/INSTALL.md#prerequisites)
    - [Setup ssh key](/INSTALL.md#set-up-ssh-key)
    - [Setup GitHub Command Line Tool](/INSTALL.md#setup-github-command-line-tool)
    - [Test SSH Connection](/INSTALL.md#test-ssh-connection)
    - [Setup anyenv](/INSTALL.md#setup-anyenv)
    - [Setup python 3.10.X](/INSTALL.md#setup-python-310X)
    - [Setup poetry](/INSTALL.md#setup-poetry)
    - [Setup Protobuf compiler](/INSTALL.md#setup-protoc)
  - [Getting Start With RACOON-AI](/INSTALL.md#getting-start-with-racoon-ai)
    - [Clone RACOON-AI](/INSTALL.md#clone-racoon-ai)
    - [Install dependencies](/INSTALL.md#install-dependencies)
    - [Enable Pre-commit hooks](/INSTALL.md#enable-pre-commit-hooks)
    - [Build RACOON-AI](/INSTALL.md#build-racoon-ai)
- **[Usage](#usage)**
- **[Related Tools](#related-tools)**

---

# Usage

## Compile and execute

```bash
make
```

Onece you have built with `make`, you can execute with:

```bash
poetry run python -m racoon_ai
```

Or

```bash
python -m racoon_ai
```

You need to run with `poetry run` if you have not switched to `venv` yet.

---

# Related Tools

- [grSim](https://github.com/RoboCup-SSL/grSim) - Simulator 
- [ssl-game-controller](https://github.com/RoboCup-SSL/ssl-game-controller) - Game controller
- [ssl-vision](https://github.com/RoboCup-SSL/ssl-vision/wiki) - Camera system (only support for Linux)
- [ssl-vision-client](https://github.com/RoboCup-SSL/ssl-vision-client) - Visualizer for `ssl-vision`
- [ssl-autorefs](https://github.com/RoboCup-SSL/ssl-autorefs) - Referee systems
