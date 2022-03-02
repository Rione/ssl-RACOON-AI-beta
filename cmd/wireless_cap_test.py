#!/usr/bin/env python3.10
# pylint: skip-file
# mypy: ignore-errors

"""kicker_test.py

    This is the kicker_test script.
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

    sender = CommandSender(is_real=True, online_ids=[int(robot_id)])

    try:
        while True:
            for i in range(0, 20, 1):
                # Simulation又はRobotに送信
                sim_cmds = SimCommands(isteamyellow=False)
                command = RobotCommand(int(robot_id))
                command.vel_fwd = i * 0.01
                command.vel_sway = 0
                command.vel_angular = 0
                command.dribble_pow = 0
                command.kickpow = 0

                sim_cmds.robot_commands.append(command)

                sender.send(sim_cmds)

                time.sleep(0.016)

            for i in range(20, 0, -1):
                # Simulation又はRobotに送信
                sim_cmds = SimCommands(isteamyellow=False)
                command = RobotCommand(int(robot_id))
                command.vel_fwd = i * 0.01
                command.vel_sway = 0
                command.vel_angular = 0
                command.dribble_pow = 0
                command.kickpow = 0

                sim_cmds.robot_commands.append(command)

                sender.send(sim_cmds)

                time.sleep(0.016)

    finally:
        print("終了します")
        del sender


if __name__ == "__main__":
    main()
