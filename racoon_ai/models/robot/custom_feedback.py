#!/usr/bin/env python3.10

"""robot_custom_feedback.py

    This module contains:
        - RobotCustomFeedback
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RobotCustomFeedback:
    """RobotCustomFeedback

    A custom feedback for our robots.

    Attributes:
        battery_vol (float): The battery voltage.
        boosted_vol (float): The boosted voltage.
        encoder_vals (list[float]): The encoder values.
    """

    battery_vol: float = field(default=0)

    boosted_vol: float = field(default=0)

    encoder_vals: tuple[float, float, float, float] = field(default=(0, 0, 0, 0))


if __name__ == "__main__":
    from dataclasses import asdict, fields

    custom_feedback = RobotCustomFeedback(battery_vol=3, boosted_vol=4, encoder_vals=(1, 2, 3, 4))
    print(custom_feedback)
    print(fields(custom_feedback))
    print(asdict(custom_feedback))
