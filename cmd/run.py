#!/usr/bin/env python3.10

"""run.py

    This is the main script.
"""

from racoon_ai.models.robot.commands import SimCommands
from racoon_ai.networks import CommandSender, VisionReceiver
from racoon_ai.observer.observer import Observer
from racoon_ai.strategy.offense import Offense
from racoon_ai.strategy.role import Role


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None`
    """
    sender = CommandSender(port=20025)
    try:
        # VisionReceiverのインスタンス
        vision = VisionReceiver(port=10025)
        # status = StatusReceiver()

        # RefereeReceiverのインスタンス
        # ref = RefereeReceiver()

        observer = Observer()
        role = Role()
        offense = Offense(observer, role)

        # TODO: 同期型処理。VisionのFPSに依存するから、VisionのFPS下がったら処理やばいかも？
        while True:
            sim_cmds = SimCommands(isteamyellow=False)

            vision.receive()
            # status.receive()

            observer.vision_receiver(vision)
            observer.ball_status()

            # Roleの処理
            role.vision_receive(vision)
            role.decide_role()

            # offenseの処理
            offense.vision_receive(vision)
            offense.main()

            # Simulation又はRobotに送信
            sim_cmds.robot_commands += offense.send_cmds
            sender.send(sim_cmds)
    finally:
        sender.stop_robots()

        del vision
        del sender


if __name__ == "__main__":
    main()
