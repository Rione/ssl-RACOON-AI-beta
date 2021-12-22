#!/usr/bin/env python3.10

"""
This is the main entry point for the program.
"""
from pathlib import Path
from sys import path

path.append(str(Path.joinpath(Path(__file__).parent.parent, "src")))

from networks.vision_receiver import VisionReceiver

if __name__ == "__main__":
    # 色チェンジならinvertをTrueに
    test = VisionReceiver(invert=False)
    print(test.get_fieldsize())
