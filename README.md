# RACOON-AI

## Overview

This is our strategy software for [RoboCup Soccer SSL](https://ssl.robocup.org/)  
`RACOON-AI` stands for Ri-one ssl Accurate Operation AI

## Minimal Requirements

- 64bit machienes (Tested on: x86_64, ARM64)
- Python 3.10.X (We recommend using `pyenv`)
- Poetry (Python's dependency manager)
- Protocol Buffer compiler (`protoc`)
- GNU Make (`make` command)
- Google Protobuffer Compiler (`protoc`) v3.19.1

---

Please follow the [installation guide](./INSTALL.md) to setup.

---

# Usage

Compile and execute (Recommended):

```bash
make
```

---

Onece you have built with `make` or `make build`, you can execute with:

```bash
make run
```

> **Warning**  
> You need to run with `poetry run` if you have not switched to `venv` yet.

---

# Related Tools

- [grSim](https://github.com/RoboCup-SSL/grSim) - Simulator 
- [ssl-game-controller](https://github.com/RoboCup-SSL/ssl-game-controller) - Game controller
- [ssl-vision](https://github.com/RoboCup-SSL/ssl-vision/wiki) - Camera system (only support for Linux)
- [ssl-vision-client](https://github.com/RoboCup-SSL/ssl-vision-client) - Visualizer for `ssl-vision`
- [ssl-autorefs](https://github.com/RoboCup-SSL/ssl-autorefs) - Referee systems
