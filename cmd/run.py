#!/usr/bin/env python3.10
# type: ignore
# pylint: disable-all
"""run.py

    This is the main script.
"""
import sys

from PyQt5.QtWidgets import QApplication

from racoon_ai.gui.main import Gui
from racoon_ai.models.robot.commands import SimCommands
from racoon_ai.networks import CommandSender, VisionReceiver
from racoon_ai.observer.observer import Observer
from racoon_ai.strategy.offense import Offense
from racoon_ai.strategy.role import Role


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None
    """

    # ここに通信可能なロボットIDを入力してください！
    # 通信できないロボットがいるとOSErrorになります（継続可）
    online_id: list[int] = [1, 3]

    # 実機環境で実行するときにはTrueにしてください
    real_mode: bool = False

    sender = CommandSender()
    app = QApplication(sys.argv)
    try:

        # VisionReceiverのインスタンス, receiveポートをportで変更可能
        vision = VisionReceiver(port=10007)
        # status = StatusReceiver()

        # RefereeReceiverのインスタンス
        # ref = RefereeReceiver()

        observer = Observer()
        role = Role()
        offense = Offense(observer, role)
        gui = Gui()
        # TODO: 同期型処理。VisionのFPSに依存するから、VisionのFPS下がったら処理やばいかも？

        while True:
            sim_cmds = SimCommands(isteamyellow=False)

            vision.receive()
            # status.receive()

            gui.vision_receive(vision)

            observer.vision_receiver(vision)
            observer.ball_status()

            # Roleの処理
            role.vision_receive(vision, offense)
            role.decide_role()

            # offenseの処理
            offense.vision_receive(vision)
            offense.main()

            # Simulation又はRobotに送信
            sim_cmds.robot_commands += offense.send_cmds
            sender.send(sim_cmds, online_id, real_mode)

            app.processEvents()

    finally:
        sender.stop_robots(online_id, real_mode)
        del vision
        del sender
        app.close()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
