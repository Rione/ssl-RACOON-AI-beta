#!/usr/bin/env python3.10
# pylint: disable-all

"""
    This is the main script.
"""

import sys
from logging import INFO, Formatter, StreamHandler, getLogger, shutdown
from typing import Any

from PyQt5.QtWidgets import QApplication  # type: ignore

from .gui.main import Gui  # type: ignore
from .models.robot import SimCommands
from .networks import CommandSender, VisionReceiver
from .observer.observer import Observer
from .strategy.offense import Offense
from .strategy.role import Role


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None
    """

    # Settings for logger
    fmt = Formatter("[%(levelname)s] %(asctime)s %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    hdlr = StreamHandler()
    hdlr.setFormatter(fmt)
    logger = getLogger("racoon_ai")
    logger.setLevel(INFO)
    logger.addHandler(hdlr)
    logger.debug("Logger initialized")

    # ここに通信可能なロボットIDを入力してください！
    # 通信できないロボットがいるとOSErrorになります（継続可）
    online_ids: list[int] = [1, 3]

    # 実機環境で実行するときにはTrueにしてください
    is_real: bool = True

    sender = CommandSender(is_real, online_ids)
    app: Any = QApplication(sys.argv)

    # TODO: 同期型処理。VisionのFPSに依存するから、VisionのFPS下がったら処理やばいかも？
    try:
        # VisionReceiverのインスタンス, receiveポートをportで変更可能
        vision = VisionReceiver(port=10025)

        # status = StatusReceiver()

        # RefereeReceiverのインスタンス
        # ref = RefereeReceiver()

        observer = Observer()

        role = Role()

        offense = Offense(observer)
        gui = Gui()
        # TODO: 同期型処理。VisionのFPSに依存するから、VisionのFPS下がったら処理やばいかも？

        sender = CommandSender(is_real, online_ids)

        logger.info("Roop started")

        while True:
            # 送信用のコマンドリストを初期化
            sim_cmds = SimCommands(isteamyellow=False)

            vision.receive()

            gui.vision_receive(vision)

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

            app.processEvents()

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received", exc_info=False)

    finally:
        logger.info("Cleaning up...")
        del vision
        del sender
        shutdown()


if __name__ == "__main__":
    main()
