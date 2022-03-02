#!/usr/bin/env python3.10

"""drbr_test.py

    This is the dribbler test script.
"""

import time

from racoon_ai.models.robot import RobotCommand, SimCommands
from racoon_ai.networks.sender import CommandSender


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None`
    """

    sender = CommandSender()

    robot_id: str = input("テストするロボットIDを入力してください: ")
    drr_sec: str = input("ドリブラーに送信する秒数を入力してください: ")
    sim_cmds = SimCommands(isteamyellow=False)

    online_id: list[int] = [int(robot_id)]
    real_mode: bool = True

    try:
        # Simulation又はRobotに送信
        command = RobotCommand(int(robot_id))
        command.vel_fwd = 0
        command.vel_sway = 0
        command.vel_angular = 0
        command.dribble_pow = True
        command.kickpow = 0

        sim_cmds.robot_commands.append(command)

        sender.send(sim_cmds, online_id, real_mode)

        print("ドリブラー信号を送信しています.")
        time.sleep(float(drr_sec))
    finally:
        sender.stop_robots(online_id, real_mode)
        print("終了します")
        del sender


if __name__ == "__main__":
    main()
