#!/usr/bin/env python3.10
# mypy: ignore-errors
# pylint: skip-file

"""joystick_mode.py

    This is the joystick script.
"""

import time

import pygame  # type: ignore
from pygame.locals import JOYAXISMOTION, JOYBUTTONDOWN  # pylint: disable=no-name-in-module

from racoon_ai.models.robot.commands import RobotCommand, SimCommands
from racoon_ai.networks.command_sender import CommandSender


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None`
    """
    pygame.joystick.init()
    try:
        # ジョイスティックインスタンスの生成
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print("ジョイスティックの名前:", joystick.get_name())
        print("ボタン数 :", joystick.get_numbuttons())
    except pygame.error:
        print("ジョイスティックが接続されていません")
        exit()

    # pygameの初期化
    pygame.init()

    robot_id: str = input("テストするロボットIDを入力してください: ")

    # センダーの設定
    sender = CommandSender(is_real=True, online_ids=[int(robot_id)])

    # ループ
    active = True
    try:
        while active:
            # イベントの取得
            for e in pygame.event.get():
                sim_cmds = SimCommands(isteamyellow=False)
                command = RobotCommand(int(robot_id))
                command.vel_fwd = 0
                command.vel_sway = 0
                command.vel_angular = 0
                command.dribble_pow = 0
                command.kickpow = 0

                # Button 9 (R1)
                if joystick.get_button(9) == 1:
                    command.dribble_pow = 1

                if joystick.get_button(5) == 1:
                    command.vel_angular = 0.05

                if joystick.get_button(7) == 1:
                    command.vel_angular = -0.05

                # ジョイスティックのボタンの入力
                if e.type == JOYAXISMOTION:

                    # PS3 DUALSHOCK: MARU
                    if joystick.get_button(13):
                        command.use_wheels_speed = True
                        command.wheels = int(joystick.get_axis(1) * 10) * 0.1 * 100, 0.0, 0.0, 0.0

                    # PS3 DUALSHOCK: BATSU
                    if joystick.get_button(14):
                        command.use_wheels_speed = True
                        command.wheels = 0.0, int(joystick.get_axis(1) * 10) * 0.1 * 100, 0.0, 0.0

                    # PS3 DUALSHOCK: SANKAKU
                    if joystick.get_button(15):
                        command.use_wheels_speed = True
                        command.wheels = 0.0, 0.0, int(joystick.get_axis(1) * 10) * 0.1 * 100, 0.0

                    # PS3 DUALSHOCK: SHIKAKU
                    if joystick.get_button(12):
                        command.use_wheels_speed = True
                        command.wheels = 0.0, 0.0, 0.0, int(joystick.get_axis(1) * 10) * 0.1 * 100

                    command.vel_fwd = int(joystick.get_axis(1) * 10) * 0.1 * -1
                    command.vel_sway = int(joystick.get_axis(0) * 10) * 0.1 * -1
                    command.vel_angular = int(joystick.get_axis(2) * 10) * 0.1 * 0.3 * -1
                    print("十時キー:", command.vel_fwd, command.vel_sway)

                    sim_cmds.robot_commands.append(command)

                    sender.send(sim_cmds)

                    time.sleep(0.016)

                elif e.type == JOYBUTTONDOWN:
                    if int(e.button) == 11:
                        command.kickpow = 1
                        sim_cmds.robot_commands.append(command)
                        sender.send(sim_cmds)
                        time.sleep(0.016)

    finally:
        print("終了します")
        del sender


if __name__ == "__main__":
    main()
