#!/usr/bin/env python3.10

"""communicate.py"""

from networks.vision_receiver import VisionReceiver
from networks.command_sender import CommandSender
from strategy.attacker import Attacker

# from src.observer.observer import Observer


def do_communicate():
    # VisionReceiverのインスタンス
    vision = VisionReceiver()

    # RefereeReceiverのインスタンス
    # ref = RefereeReceiver()

    # observer = Observer(vision, ref) 出力例: observer.ball.speedのように

    # TODO: 同期型処理。VisionのFPSに依存するから、VisionのFPS下がったら処理やばいかも？
    while True:
        # CommandSenderのインスタンス
        sender = CommandSender()

        vision.receive()

        attacker = Attacker(vision)
        # defence = Defence(vision) ...
        send_command = attacker.send_command()

        # send_commandの型はRobotCommand
        sender.set_robotcommand(send_command)

        sender.send()
