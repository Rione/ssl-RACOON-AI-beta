#!/usr/bin/env python3.10

"""field_circular_arc.py

    This module contains the FieldCircularArc class.
"""

from models.official.field.geometry.field_shape_type import FieldShapeType
from models.official.field.geometry.vector_2_f import Vector2f


class FieldCircularArc:
    """FieldCircularArc

    Args:
        name (str): Name of this field marking.
        center (Vector2f): Center point of the circular arc.
        radius (float): Radius of the arc.
        a1 (float): Start angle in counter-clockwise order.
        a2 (float): End angle in counter-clockwise order.
        thickness (float): Thickness of the arc.
        type (FieldShapeType, optional): The type of this shape
    """

    def __init__(
        self,
        name: str,
        center: Vector2f,
        radius: float,
        a1: float,
        a2: float,
        thickness: float,
        type: FieldShapeType = FieldShapeType.UNDEFINED,
    ):

        self.__name: str = name

        self.__center: Vector2f = center

        self.__radius: float = radius

        self.__a1: float = a1

        self.__a2: float = a2

        self.__thickness: float = thickness

        self.__type: FieldShapeType = type

    def __str__(self) -> str:
        pass

    @property
    def name(self) -> str:
        """name

        Returns:
            str: Name of this field marking.
        """
        return self.__name

    @property
    def center(self) -> Vector2f:
        """center

        Returns:
            Vector2f: Center point of the circular arc.
        """
        return self.__center

    @property
    def radius(self) -> float:
        """radius

        Returns:
            float: Radius of the arc.
        """
        return self.__radius

    @property
    def a1(self) -> float:
        """a1

        Returns:
            float: Start angle in counter-clockwise order.
        """
        return self.__a1

    @property
    def a2(self) -> float:
        """a2

        Returns:
            float: End angle in counter-clockwise order.
        """
        return self.__a2

    @property
    def thickness(self) -> float:
        """thickness

        Returns:
            float: Thickness of the arc.
        """
        return self.__thickness

    @property
    def type(self) -> FieldShapeType:
        """type

        Returns:
            FieldShapeType: The type of this shape
        """
        return self.__type
