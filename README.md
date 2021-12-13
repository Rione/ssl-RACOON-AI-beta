# RACOON-AI

Ri-one SSL Accurate Operation AI

## 使い方 Usage

### ランタイム要件

RACOON-AIはWindowsで動作すると思われますが、grSim等のインストール難易度が高いため、非推奨です。

* 64bit Ubuntu 21.04, macOS (M1でも動作)
* Latest Python 3
* [SSL-Vision](https://github.com/RoboCup-SSL/ssl-vision)（実機環境）
* [grSim](https://github.com/RoboCup-SSL/grSim)（シミュレーション環境）

### 推奨依存ソフトウェア

このソフトウェアを開発するにあたり、最適な環境を設定するには以下のパッケージをインストールすることを推奨します。

* [ssl-game-controller](https://github.com/RoboCup-SSL/ssl-game-controller)
* [TIGERs-Autoref](https://github.com/TIGERs-Mannheim/AutoReferee)

|   OS/Platform    |     SSL-Vision     |       grSim        | ssl-game-controller |   TIGERs-Autoref   |
| :--------------: | :----------------: | :----------------: | :-----------------: | :----------------: |
|     Windows      |        :x:         |     :question:     | :white_check_mark:  | :white_check_mark: |
|   Ubuntu/Linux   | :white_check_mark: | :white_check_mark: | :white_check_mark:  | :white_check_mark: |
| macOS(M1, Intel) |        :x:         | :white_check_mark: | :white_check_mark:  | :white_check_mark: |

### 自分の環境にデプロイ

下記のコマンドの上２行は、ワークスペース(ws)の作成をしています。必要に応じて名前を変更してください。

```bash
mkdir ~/ws
cd ~/ws
git clone git@github.com:Rione-SSL/RACOON-AI
```

SSHキーなどの設定は、Rione-SSLのNotionを確認してください。

### 実行

RACOON-AIを実行するには、以下のコマンドを実行してください。

```bash
./run.sh
```


