#!/usr/bin/env python3.10

"""
This is the main entry point for the program.
"""
from pathlib import Path
from sys import path

path.append(str(Path.joinpath(Path(__file__).parent.parent, "src")))

import comms.communicate

if __name__ == "__main__":
    # comms/communicate内を実行
    comms.communicate.do_communicate()
