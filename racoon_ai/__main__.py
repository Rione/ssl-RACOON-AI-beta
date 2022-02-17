#!/usr/bin/env python3.10

"""
    This is the main script.
"""

from .models.robot.commands import SimCommands
from .networks import CommandSender, VisionReceiver
from .strategy.attacker import Attacker

# from .observer import Observer


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None
    """

    # VisionReceiverのインスタンス
    vision = VisionReceiver()

    # RefereeReceiverのインスタンス
    # ref = RefereeReceiver()

    # observer = Observer(vision, ref) 出力例: observer.ball.speedのように

    # CommandSenderのインスタンス
    sender = CommandSender()

    # TODO: 同期型処理。VisionのFPSに依存するから、VisionのFPS下がったら処理やばいかも？
    try:
        while True:
            # 送信用のコマンドリストを初期化
            sim_cmds = SimCommands(isteamyellow=False)

            vision.receive()

            attacker = Attacker(vision)
            attacker.main()

            # defence = Defence(vision) ...

            sim_cmds.robot_commands += attacker.send_cmds
            sender.send(sim_cmds)

    except KeyboardInterrupt:
        pass

    del vision
    del sender


if __name__ == "__main__":
    main()
