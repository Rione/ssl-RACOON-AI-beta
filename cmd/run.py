#!/usr/bin/env python3.10

"""run.py

    This is the main script.
"""

import sys

if __name__ == "__main__":
    from racoon_ai.comms import communicate

    sys.exit(communicate.do_communicate())
