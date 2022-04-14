# Installation

- [Prerequisites](#prerequisites)
  - [Setup ssh key](#set-up-ssh-key)
  - [Setup GitHub Command Line Tool](#setup-github-command-line-tool)
  - [Test SSH Connection](#test-ssh-connection)
  - [Setup anyenv](#setup-anyenv)
  - [Setup python 3.10.X](#setup-python-310X)
  - [Setup poetry](#setup-poetry)
  - [Setup Protobuf compiler](#setup-protoc)

---

We know Python version 3.10.X is still in development, isntalling with version management tool is recommended.
Here, we use `pyenv` with `anyenv` since its simplicity.

## Prerequisites

NOTE: On windows, you can use `py` command instead of `pyenv` (with `anyenv`).

- ssh
- [GitHub command line tool](https://github.com/cli/cli) - For working with GitHub (`gh` command)
- [anyenv](https://github.com/anyenv/anyenv) - For managing version management tools
- [pyenv](https://github.com/pyenv/pyenv) - For managing python versions
- [Poetry](https://github.com/python-poetry/poetry) - For managing python dependencies
- [Protoc](https://github.com/protocolbuffers/protobuf) - For compiling `.proto` files

### Setup `ssh` key

From the security perspective, we recommend to use SSH key.
Please refer to [GitHub documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

1. Generate a Private/Public key

```bash
ssh-keygen -t ed25519 -C "<Your GitHub Email>"
```

2. Add to ssh-agent

Please add following to your `~/.ssh/config` file.

```text
Host *
  AddKeysToAgent yes
  UseKeychain yes            # Only for MacOS (10.12.2 or later)
  PasswordAuthentication no  # Recommended for the security reason

# For GitHub
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/<Your Secret Key File>
```

### Setup GitHub Command Line Tool

0. Create a GitHub account

Please register from this page: [GitHub](https://github.com/signup)

1. Install GitHub Command Line Tool

Please follow the official [installation](https://github.com/cli/cli#installation).  
For linux users: [Instructions for Linux](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)

2. Login with your GitHub account

_NOTE: Select the `SSH` option, and upload your SSH key._

```bash
gh auth login
```

### Test SSH connection

```bash
ssh -T git@github.com
```

**_NOTE:
If you get an error, about the connection to the ssh-agent,
please retry with the following command._**

```bash
eval $(ssh-agent -s) && ssh-add ~/.ssh/<Your Secet Key File>
```

### Setup `anyenv`

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
poetry --version
```
You would get `Poetry version X.X.X`

If you get an error about the command not found, 
please add following to your `~/.zshrc` or `~/.bashrc` file.

```bash
export PATH="${HOME}/.local/bin:${PATH}"
```

4. Enable Tab completion (optional)

Please follow the following guide.

NOTE: You can check your shell by `echo $SHELL`
 
Guide: https://python-poetry.org/docs/master#enable-tab-completion-for-bash-fish-or-zsh


### Setup Protoc

See also the [Official Guide](https://github.com/protocolbuffers/protobuf/blob/v3.19.1/src/README.md)

**NOTE: Please modify the prefix path if you use another version of protoc.**

0. Install build requirements (if not installed)

NOTE: that GNU libtool is required here.

- autoconf
- automake
- libtool
- make
- g++
- unzip

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
./configure --prefix=$HOME/.local
```

5. Build and test

NOTE: You can speed up by using make with `-j` option.

```bash
make && make check
```

6. Install

```bash
make install
```

7. Test

```bash
protoc --version
```

You would get `libprotoc 3.19.1`.

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

Ex) `poetry install -E pygame`


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

Compile proto files, build python package to `dist` directory and execute.

```bash
make
```
