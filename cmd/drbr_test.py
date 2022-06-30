#!/usr/bin/env python3.10
# pylint: skip-file

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

    robot_id: str = input("テストするロボットIDを入力してください: ")
    sender = CommandSender(is_real=True, target_ids={int(robot_id)})
    drr_sec: str = input("ドリブラーに送信する秒数を入力してください: ")
    sim_cmds = SimCommands(isteamyellow=False)

    try:
        command = RobotCommand(int(robot_id))
        command.vel_fwd = 0
        command.vel_sway = 0
        command.vel_angular = -1.0
        command.dribble_pow = False
        command.kickpow = 0

        sim_cmds.robot_commands.append(command)

        while True:
            # Simulation又はRobotに送信
            
            sender.send(sim_cmds)

            print("ドリブラー信号を送信しています.")
            time.sleep(float(drr_sec))
    finally:
        print("終了します")
        del sender


if __name__ == "__main__":
    main()
