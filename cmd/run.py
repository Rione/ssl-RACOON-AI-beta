#!/usr/bin/env python3.10

"""run.py

    This is the main script.
"""

from racoon_ai.models.robot.commands import SimCommands
from racoon_ai.networks.command_sender import CommandSender
from racoon_ai.networks.vision_receiver import VisionReceiver
from racoon_ai.strategy.attacker import Attacker

# from src.observer.observer import Observer


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None
    """
    try:
        # VisionReceiverのインスタンス
        vision = VisionReceiver()

        # RefereeReceiverのインスタンス
        # ref = RefereeReceiver()

        # observer = Observer(vision, ref) 出力例: observer.ball.speedのように

        # TODO: 同期型処理。VisionのFPSに依存するから、VisionのFPS下がったら処理やばいかも？
        while True:
            # 送信用のコマンドリストを初期化
            sim_cmds = SimCommands(isteamyellow=False)

            # CommandSenderのインスタンス
            sender = CommandSender()

            vision.receive()

            attacker = Attacker(vision)
            attacker.main()
            # defence = Defence(vision) ...

            sim_cmds.robot_commands += attacker.send_cmds
            sender.send(sim_cmds)

    finally:
        del vision
        del sender


if __name__ == "__main__":
    main()
