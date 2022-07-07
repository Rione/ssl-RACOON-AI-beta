#!/usr/bin/env python3.10
# pylint: disable=R0801

"""joystick_mode.py

    This is the joystick script.
"""

from math import radians
from sys import exit as sys_exit
from time import sleep

import pygame
from pygame import JOYAXISMOTION, JOYBUTTONDOWN  # pylint: disable=E0611

from racoon_ai.models.robot import RobotCommand, SimCommands
from racoon_ai.networks.sender import CommandSender


def main() -> None:  # pylint: disable=R0912,R0915
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
        sys_exit()

    # pygameの初期化
    pygame.init()

    robot_id: str = input("テストするロボットIDを入力してください: ")

    # センダーの設定
    sender = CommandSender(is_real=True, target_ids={int(robot_id)})

    # ループ
    active = True
    try:
        while active:
            # イベントの取得
            for event in pygame.event.get():
                sim_cmds = SimCommands(isteamyellow=False)
                command = RobotCommand(int(robot_id), chip_enabled=False, use_imu=False)

                # Button 9 (R1)
                if joystick.get_button(9):
                    command.dribble_pow = 1

                if joystick.get_button(5):
                    command.vel_angular = radians(30)

                if joystick.get_button(7):
                    command.vel_angular = radians(-30)

                # ジョイスティックのボタンの入力
                if event.type == JOYAXISMOTION:

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
                    command.vel_angular = radians(int(joystick.get_axis(2) * 10) * 18) * -1
                    print("十時キー:", command.vel_fwd, command.vel_sway, command.vel_angular)

                    sim_cmds.robot_commands.append(command)

                    sender.send(sim_cmds)

                    sleep(0.016)

                elif event.type == JOYBUTTONDOWN:
                    if int(event.button) == 11:
                        command.kickpow = 80
                        sim_cmds.robot_commands.append(command)
                        sender.send(sim_cmds)
                        sleep(0.016)

    finally:
        print("終了します")
        del sender


if __name__ == "__main__":
    main()
