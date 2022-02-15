#!/usr/bin/env python3.10

"""kicker_test.py

    This is the kicker_test script.
"""
import os
import time

from racoon_ai.models.robot.commands import RobotCommand, SimCommands
from racoon_ai.networks.command_sender import CommandSender


def beep(freq: int, dur: int = 100) -> None:
    """
    ビープ音を鳴らす.
    @param freq 周波数
    @param dur  継続時間（ms）
    """
    os.system("play -n synth %s sin %s" % (dur / 1000, freq))


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None`
    """

    sender = CommandSender()

    robot_id: str = input("テストするロボットIDを入力してください: ")

    online_id: list[int] = [int(robot_id)]
    real_mode: bool = True

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

                sender.send(sim_cmds, online_id, real_mode)

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

                sender.send(sim_cmds, online_id, real_mode)

                time.sleep(0.016)

            beep(440, 100)
    finally:
        sender.stop_robots(online_id, real_mode)
        print("終了します")
        del sender


if __name__ == "__main__":
    main()
