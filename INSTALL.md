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
> This step is for those who want to specify the path of the key file.

From the security perspective, we recommend to use SSH key.
Please refer to [GitHub documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

0. Generate a Private/Public key

```bash
ssh-keygen -t ed25519 -C "<Your GitHub Email>"
```

1. Add to ssh-agent

```bash
ssh-add ~/.ssh/<Your Secret Key File>
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
  UseKeychain yes            # Only for MacOS (10.12.2 or later)
  PasswordAuthentication no  # Recommended for the security reason

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
sudo apt install -y build-essential automake autoconf libtool unzip
```

1. Clone the protobuf repository

```bash
gh repo clone protocolbuffers/protobuf $HOME/.local/opt/protobuf -- -b v3.19.1 --depth=1 --recurse-submodules --shallow-submodules
```

3. Cd into the repo & run setup script

```bash
cd ${HOME}/.local/opt/protoc && ./autogen.sh
```

4. Configure to your environment

```bash
./configure --prefix=${HOME}/.local/protobuf
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
mkdir -p ${HOME}/.local/bin && ln -s ${HOME}/.local/opt/protobuf/bin/protoc ${HOME}/.local/bin/
```

9. Test the installation

```bash
protoc --version
```

You would get `libprotoc 3.19.1`.

> **Note**  
> If you get an error about the command not found, 
> please add following to your `~/.zshrc` or `~/.bashrc` file, and retry after source it.

```bash
export PATH="${HOME}/.local/bin:${PATH}"
```

10. Add to your `$PKG_CONFIG_PATH`

Please add the following to your `~/.zshrc` or `~/.bashrc`, and source it.

```bash
export PKG_CONFIG_PATH="${HOME}/.local/opt/protobuf/lib/pkgconfig:${PKG_CONFIG_PATH}"
```

## Prepare Python environment

### Setup anyenv

Since the ease of installation, we recommend using with [anyenv](https://github.com/pyenv/pyenv).
`anyenv` is a tool to manage multiple version management tools, include `pyenv`.
The tool is provided in Homebrew.
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
anyenv install --init git@github.com:anyenv/anyenv-install.git
```

Test the installation:

```bash
anyenv install -l
```

---

### Setup Python 3.10.X with Pyenv

0. Install build dependencies

See also [Suggested build environment](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)

On MacOS native (with Homebrew):

```bash
brew install openssl@1.1 readline
```

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

---

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
poetry --version
```
You would get `Poetry version X.X.X`

4. Enable Tab completion (optional)

Please follow the following guide.

NOTE: You can check your shell by `echo $SHELL`
 
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


## Enable pre-commit hooks

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
