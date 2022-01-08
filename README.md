# RACOON-AI

Ri-one SSL Accurate Operation AI

## 使い方 Usage

### ランタイム要件

RACOON-AI は Windows でも動作しますが、grSim 等のインストール難易度が高いため、非推奨です。

- 64bit Ubuntu 21.04, macOS (M1 でも動作)
- Python 3.10.X
- [SSL-Vision](https://github.com/RoboCup-SSL/ssl-vision) (実機環境)
- [grSim](https://github.com/RoboCup-SSL/grSim) (シミュレーション環境)

### 推奨依存ソフトウェア

このソフトウェアを開発するにあたり、最適な環境を設定するには以下のパッケージをインストールすることを推奨します。

- [ssl-game-controller](https://github.com/RoboCup-SSL/ssl-game-controller)
- [TIGERs-Autoref](https://github.com/TIGERs-Mannheim/AutoReferee)

|   OS/Platform    |     SSL-Vision     |       grSim        | ssl-game-controller |   TIGERs-Autoref   |
| :--------------: | :----------------: | :----------------: | :-----------------: | :----------------: |
|     Windows      |        :x:         | :white_check_mark: | :white_check_mark:  | :white_check_mark: |
|   Ubuntu/Linux   | :white_check_mark: | :white_check_mark: | :white_check_mark:  | :white_check_mark: |
| macOS(M1, Intel) |        :x:         | :white_check_mark: | :white_check_mark:  | :white_check_mark: |

### 自分の環境にデプロイ

下記のコマンドの上２行は、ワークスペース(ws)の作成をしています。必要に応じて名前を変更してください。

```bash
mkdir ~/ws
cd ~/ws
git clone git@github.com:Rione-SSL/RACOON-AI
```

SSH キーなどの設定は、Rione-SSL の Notion を確認してください。

### 環境構築

Python のバージョンは 3.10 です。

既に別の Python を使用している場合は、[pyenv](https://github.com/pyenv/pyenv) などを使用して別途インストールしてください。
注意: Linux (Ubuntu) では python3-venv が必須です。 `sudo apt install -y python3-venv` でインストールできます。

なお、Windows では公式の Py ランチャーが使用できます。
二つ目以降の Python をインストールする際に項目を選択し、同時にインストールしてください。

依存関係管理とパッケージングには、[poetry](https://python-poetry.org) を使用します。

下記は ubuntu 環境でのコマンド例です。  
以下、Python3.10 環境下の前提でのコマンド例です。

```sh

# Uninstall old poetry
$ curl -sSL https://install.python-poetry.org | python - --uninstall

# Install poetry
$ curl -sSL https://install.python-poetry.org | python3.10

# Follow the description, add installed package to your PATH (Usually `~/.local/bin`)
$ export $PATH="$PATH:<PATH_TO_POETRY_BIN>"

# Check if poetry is installed
$ poetry --version
> Poetry version 1.1.12

# Enable tab completion (optional)
$ poetry completions bash > /etc/bash_completion.d/poetry.bash-completion

# Create a virtual environment (optional)
$ python3.10 -m venv .venv

# Install deps
$ make install

# Setup pre-commit hook
$ pre-commit install
```

### 実行

RACOON-AI を実行するには、以下のコマンドを実行してください。

```bash
# Only `make` is also available
# You can see the usage by `make help
$ make run
```

## 使用フック

- check-yaml (YAML の構文チェック)
- end-of-file-fixer (ファイルの最後に改行が一行になるように修正)
- mixed-line-ending (改行コードを LF に統一)
- no-commit-to-branch (master/main に commit するのを抑止)
- isort (import の順番を整える)
- flake8 (Python のコードを検証する)
- pylint (Python のコードを検証する)
- mypy (Python コードのデータ型を検証する)
- black (Python のコードを整形)

(参照: [Supported hooks - pre-commit](https://pre-commit.com/hooks.html))
