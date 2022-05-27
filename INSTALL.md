> **Warning**  
> On windows, please use Ubuntu 20.04 with Windows Subsystem for Linux (WSL) to run. (Windows native is not tested yet)

# Installation

- [Prepare GitHub](#prepare-github)
  - [(Optional) Generate SSH key manually](#optional-generate-ssh-key)
  - [Setup GitHub Command Line Tool](#setup-github-command-line-tool)
    - [Test SSH Connection](#test-ssh-connection)
- [Clone RACOON-AI](#clone-racoon-ai)
- [Setup Protobuf compiler](#setup-protoc)
- [Prepare Python environment](#prepare-python-environment)
  - [Setup anyenv](#setup-anyenv)
  - [Setup python 3.10.X with Pyenv](#setup-python-310x-with-pyenv)
  - [Setup poetry](#setup-poetry)
- [Enable pre-commit hooks](#enable-pre-commit-hooks)
- [Build RACOON-AI](#build-racoon-ai)


## Prerequisites

- [OpenSSH client](https://www.openssh.com) - For SSH connection
- [GitHub command line tool](https://github.com/cli/cli) - For working with GitHub (`gh` command)
- [anyenv](https://github.com/anyenv/anyenv) - For managing version management tools
- [pyenv](https://github.com/pyenv/pyenv) - For managing python versions
- [Poetry](https://github.com/python-poetry/poetry) - For managing python dependencies
- [Protoc](https://github.com/protocolbuffers/protobuf) - For compiling `.proto` files

We know Python version 3.10.X is still in development, isntalling with version management tool is recommended.
Here, we use `pyenv` with `anyenv` since its simplicity.

## Prepare GitHub

### (optional) Generate `ssh` key

> **Note**  
> This step is for those who want to costomize SSH key.  
> (GitHub CLI can generate `id_ed25519` automatically)

From the security perspective, we recommend to use SSH key.
Please refer to [GitHub documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

```bash
ssh-keygen -t ed25519 -C "<Your GitHub Email>"
```

---

### Setup GitHub Command Line Tool

0. Create a GitHub account

Please register from this page: [GitHub](https://github.com/signup)

1. Install GitHub Command Line Tool

Please follow the official [installation](https://github.com/cli/cli#installation).  
For ubuntu (Linux) users: [Instructions for Linux](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)

2. Login with your GitHub account

> **Note**  
> Select the `SSH` option, and upload your SSH key

```bash
gh auth login
```

---

### Test SSH connection

0. Write configuration file

Please add following to your `~/.ssh/config` file.

```text
Host *
  AddKeysToAgent yes
  
  # Only for MacOS (10.12.2 or later)
  UseKeychain yes
  
  # Recommended for the security reason
  PasswordAuthentication no  

# For GitHub
Host github.com
  HostName github.com
  IdentityFile ~/.ssh/<Your Secret Key File>
```

1. Connect to GitHub

```bash
ssh -T git@github.com
```

> **Note**  
> If you get an error about the connection to the ssh-agent, please retry after the following command

```bash
eval $(ssh-agent -s)
```

## Clone RACOON-AI

Clone to your local workspace.

```bash
gh repo clone Rione/ssl-RACOON-AI ~/ws/ssl-racoon-ai && cd $_
```

## Setup Protoc

See also the [Official Guide](https://github.com/protocolbuffers/protobuf/blob/v3.19.1/src/README.md)

0. Install build requirements (if not installed)

- autoconf
- automake
- libtool (GNU libtool)
- make
- g++
- unzip


On MacOS native, install with [Homebrew](https://brew.sh/) is recommended:

```bash
brew install autoconf automake libtool
```

If you use ubuntu (Debian):

```bash
sudo apt update && sudo apt install -y build-essential automake autoconf libtool unzip
```

1. Clone the protobuf repository

```bash
gh repo clone protocolbuffers/protobuf ${HOME}/.local/opt/protobuf -- -b v3.19.1 --depth=1 --recurse-submodules --shallow-submodules
```

3. Cd into the repo & run setup script

```bash
cd ${HOME}/.local/opt/protobuf && ./autogen.sh
```

4. Configure to your environment

```bash
./configure --prefix=${HOME}/.local/opt/protobuf
```

5. Build the code

> **Note**  
> You can speed up by using make with `-j` option.

```bash
make
```

6. Test the compilation

```bash
make check
```

7. Install

```bash
make install
```

8. Link protoc to your bin directory

```bash
mkdir -p ${HOME}/.local/bin && ln -s ${HOME}/.local/opt/protobuf/bin/* ${HOME}/.local/bin/
```

9. Test the installation

```bash
protoc --version
```

You would get `libprotoc 3.19.1`.

> **Note**  
> If you get an error about the command not found, 
> please add following to your `~/.zshrc` or `~/.bashrc` file, and retry after source it.

Example (bash):

```bash
echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ~/.bashrc && . ~/.bashrc
```

10. Add to your `$PKG_CONFIG_PATH`

Please add the following to your `~/.zshrc` or `~/.bashrc`, and source it.

Example (bash):

```bash
echo 'export PKG_CONFIG_PATH="${HOME}/.local/opt/protobuf/lib/pkgconfig:${PKG_CONFIG_PATH}"' >> ~/.bashrc && . ~/.bashrc
```

## Prepare Python environment

### Setup anyenv

Since the ease of installation, we recommend using with [anyenv](https://github.com/anyenv/anyenv). 
`anyenv` is a tool to manage multiple version management tools, include `pyenv`. 
The tool is provided in Homebrew (`brew install anyenv`). 
If you prefer to use Homebrew, please skip the following steps. 

1. Clone `anyenv` from GitHub

```bash
gh repo clone anyenv/anyenv ~/.local/opt/anyenv
```

2. Set environment variable

Add following to your `~/.zshrc` or `~/.bashrc` file.

```bash
export ANYENV_ROOT="${HOME}/.local/opt/anyenv"
if [ -d $ANYENV_ROOT ]; then
  export PATH="${ANYENV_ROOT}/bin:${PATH}"
  eval "$(anyenv init -)"
  test -e "${PYENV_ROOT}/plugins/pyenv-virtualenv" && eval "$(pyenv virtualenv-init -)"
fi
```

3. Install manifests

```bash
anyenv install --init https://github.com/anyenv/anyenv-install.git
```

Test the installation:

```bash
anyenv install -l
```

---

### Setup Python 3.10.X with Pyenv

0. Install Python build dependencies

See also [Suggested build environment](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)

On MacOS native (with Homebrew):

```bash
brew install openssl@1.1 readline
```

On Ubuntu:

```bash
sudo apt update && sudo apt install -y libbz2-dev libssl-dev  libreadline-dev libsqlite3-dev llvm tk-dev libxmlsec1-dev
```

1. Install `pyenv`

```bash
anyenv install pyenv
```
> **Note**  
> Restart terminal is recommended after installing `pyenv`

2. Search for the available versions

```bash
pyenv install -l | grep 3.10
```

3. Install Python

```bash
pyenv install <Your Selected Version> && pyenv rehash
```

---

### Setup Poetry

0. Install build dependencies

On Ubuntu:

```bash
sudo apt update && sudo apt install -y python3-dev python3-pip python3-venv
```

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
poetry --version
```
You would get `Poetry version X.X.X`

4. Enable Tab completion (optional)

Please follow the following guide.

NOTE: You can check your shell by `echo $SHELL` or `echo $0` (current shell)
 
Guide: https://python-poetry.org/docs/master#enable-tab-completion-for-bash-fish-or-zsh

---

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

Ex) `poetry install -E pygame`

---

### Setup Git commit template


```bash
cd $(git rev-parse --show-toplevel) && git config commit.template .gitmessage.txt
```

## Enable pre-commit hooks

> **Note**  
> After `poetry install`, you need to checkout to the .venv with `pyenv shell --unset && poetry shell`.

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

## Build RACOON-AI

Compile proto files, build python package to `dist` directory and execute.

```bash
make
```
