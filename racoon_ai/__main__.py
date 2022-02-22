#!/usr/bin/env python3.10

"""
    This is the main script.
"""
from logging import INFO, Formatter, StreamHandler, getLogger, shutdown

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
    online_id: list[int] = [1, 3]

    # 実機環境で実行するときにはTrueにしてください
    real_flag: bool = True
    sender = CommandSender(is_real=real_flag)

    # TODO: 同期型処理。VisionのFPSに依存するから、VisionのFPS下がったら処理やばいかも？
    try:
        # VisionReceiverのインスタンス, receiveポートをportで変更可能
        vision = VisionReceiver(port=10020)

        # status = StatusReceiver()

        # RefereeReceiverのインスタンス
        # ref = RefereeReceiver()

        observer = Observer()

        role = Role()

        offense = Offense(observer, role)

        logger.info("Roop started")

        while True:
            # 送信用のコマンドリストを初期化
            sim_cmds = SimCommands(isteamyellow=False)

            vision.receive()

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
            sender.send(sim_cmds, online_id)

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received", exc_info=False)

    finally:
        logger.info("Cleaning up...")
        sender.stop_robots(online_id)
        del vision
        del sender
        shutdown()


if __name__ == "__main__":
    main()
