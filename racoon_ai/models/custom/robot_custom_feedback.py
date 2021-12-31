#!/usr/bin/env python3.10

"""robot_custom_feedback.py

    This module contains:
        - RobotCustomFeedback
"""


class RobotCustomFeedback:
    """RobotCustomFeedback

    A custom feedback for our robots.

    Args:
        battery_vol (float): The battery voltage.
        boosted_vol (float): The boosted voltage.
        encoder_vals (list[float]): The encoder values.
    """

    def __init__(self, battery_vol: float, boosted_vol: float, encoder_vals: list[float]) -> None:

        self.__battery_vol: float = battery_vol

        self.__boosted_vol: float = boosted_vol

        self.__encoder_vals: list[float] = encoder_vals

    def __str__(self) -> str:
        return (
            "RobotCustomFeedback("
            f"battery_vol={self.battery_vol:.2f}, "
            f"boosted_vol={self.boosted_vol:.2f}, "
            f"encoder_vals={self.__encoder_vals_to_str()}"
            ")"
        )

    @property
    def battery_vol(self) -> float:
        """battery_vol

        Returns:
            float: The battery voltage
        """
        return self.__battery_vol

    @property
    def boosted_vol(self) -> float:
        """boosted_vol

        Returns:
            float: The boosted voltage of the kicker.
        """
        return self.__boosted_vol

    @property
    def encoder_vals(self) -> list[float]:
        """encoder_vals

        Returns:
            float: The encoder values of the wheels.
        """
        return self.__encoder_vals

    def __encoder_vals_to_str(self) -> str:
        """_encoder_vals_to_str

        Returns:
            str: The rounded encoder values of the wheels as a string.
        """
        return "[" + ", ".join(f"{x:.2f}" for x in self.encoder_vals) + "]"


if __name__ == "__main__":
    custom_feedback = RobotCustomFeedback(battery_vol=3, boosted_vol=4, encoder_vals=[1, 2, 3, 4])
    print(custom_feedback)
