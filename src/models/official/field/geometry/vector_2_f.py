#!/usr/bin/env python3.10

"""vector_2_f.py

    This module contains the Vector2F class.
"""


class Vector2f:
    """Vector2f

    Args:
        x (float): The x value.
        y (float): The y value.
    """

    def __init__(self, x: float, y: float):

        self.__x: float = x

        self.__y: float = y

    def __str__(self) -> str:
        pass

    @property
    def x(self) -> float:
        """x

        Returns:
            float: The x value.
        """
        return self.__x

    @x.setter
    def x(self, value: float) -> None:
        """x

        Args:
            value (float): The new x value.

        Returns:
            None
        """
        self.__x = value

    @property
    def y(self) -> float:
        """y

        Returns:
            float: The y value.
        """
        return self.__y

    @y.setter
    def y(self, value: float) -> None:
        """y

        Args:
            value (float): The new y value.

        Returns:
            None
        """
        self.__y = value
