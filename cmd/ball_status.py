#!/usr/bin/env python3.10
# pylint: skip-file
# mypy: ignore-errors

"""kicker_test.py

    This is the kicker_test script.
"""

import pygame  # type: ignore

from racoon_ai.networks.command_sender import CommandSender
from racoon_ai.networks.status_reciever import StatusReceiver


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None`
    """

    status = StatusReceiver()

    robot_id: str = input("テストするロボットIDを入力してください: ")

    sender = CommandSender(is_real=True, online_ids=[int(robot_id)])

    pygame.mixer.init()
    count = 0
    pre_count = 0
    try:
        while True:
            status.receive()

            print(count, pre_count)
            if status.get_infrared(3):
                if count == 0:
                    crash_sound = pygame.mixer.Sound("./assets/metronome.mp3")
                    crash_sound.play()
                    count = count + 1
            else:
                count = 0

            # for i in range(20, 0, -1):
            #     # Simulation又はRobotに送信
            #     sim_cmds = SimCommands(isteamyellow=False)
            #     command = RobotCommand(int(robot_id))
            #     command.vel_fwd = i * 0.01
            #     command.vel_sway = 0
            #     command.vel_angular = 0
            #     command.dribble_pow = 0
            #     command.kickpow = 0

            #     sim_cmds.robot_commands.append(command)

            #     sender.send(sim_cmds)

            #     time.sleep(0.016)

    finally:
        print("終了します")
        del sender


if __name__ == "__main__":
    main()
