#!/usr/bin/env python3.10

"""run.py

    This is the main script.
"""

from racoon_ai.networks import CommandSender, VisionReceiver
from racoon_ai.observer.observer import Observer
from racoon_ai.strategy.attacker import Attacker
from racoon_ai.strategy.role import Role

# from src.observer.observer import Observer


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None
    """
    sender = CommandSender()
    try:
        # VisionReceiverのインスタンス
        vision = VisionReceiver()

        # RefereeReceiverのインスタンス
        # ref = RefereeReceiver()

        observer = Observer()
        role = Role()
        attacker = Attacker(observer, role)

        # CommandSenderのインスタンス

        # TODO: 同期型処理。VisionのFPSに依存するから、VisionのFPS下がったら処理やばいかも？
        while True:
            # 送信用のコマンドリストを初期化
            # sim_cmds = SimCommands(isteamyellow=False)

            vision.receive()

            observer.vision_receiver(vision)
            observer.ball_status()

            role.vision_receive(vision, attacker)
            role.decide_role()

            attacker.vision_receive(vision)
            sender.send(attacker.main())

    # except KeyboardInterrupt:

    finally:
        sender.stop_robots()

        del vision
        del sender


if __name__ == "__main__":
    main()
