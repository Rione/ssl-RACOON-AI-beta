#!/usr/bin/env python3.10
# pylint: disable=R0801

"""kicker_test.py

    This is the kicker_test script.
"""

from time import sleep

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

    kick_pow: str = input("キッカーに送信する強度を入力してください(0.0-1.0) ")
    sim_cmds = SimCommands(isteamyellow=False)

    try:
        # Simulation又はRobotに送信
        command = RobotCommand(int(robot_id))
        command.vel_fwd = 0
        command.vel_sway = 0
        command.vel_angular = 0
        command.dribble_pow = 0
        command.kickpow = float(kick_pow)

        sim_cmds.robot_commands.append(command)
        input("Enter(Return)を押すと発射します.")

        sender.send(sim_cmds)

        print("キッカー信号を送信しました.")

        sleep(0.5)
    finally:
        print("終了します")
        del sender


if __name__ == "__main__":
    main()
