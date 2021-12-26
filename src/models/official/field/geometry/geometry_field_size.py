#!/usr/bin/env python3.10

"""geometry_field_size.py

    This module is for the GeometryFieldSize class.
"""


from models.official.field.geometry.field_circular_arc import FieldCircularArc
from models.official.field.geometry.field_line_segment import FieldLineSegment


class GeometryFieldSize:
    """GeometryFieldSize

    Args:
        field_length (int): The length of the field.
        field_width (int): The width of the field.
        goal_width (int): The width of the goal.
        goal_depth (int): The depth of the goal.
        boundary_width (int): The width of the boundary.
        field_lines (FieldLineSegment): The field lines.
        field_arcs (FieldCircularArc): The field arcs.
        penalty_area_depth (int, optional): The depth of the penalty area. Defaults to 0
        penalty_area_width (int, optional): The width of the penalty area. Defaults to 0
    """

    def __init__(
        self,
        field_length: int,
        field_width: int,
        goal_width: int,
        goal_depth: int,
        boundary_width: int,
        field_lines: FieldLineSegment,
        field_arcs: FieldCircularArc,
        penalty_area_depth: int = 0,
        penalty_area_width: int = 0,
    ) -> None:

        self.__field_length: int = field_length

        self.__field_width: int = field_width

        self.__goal_width: int = goal_width

        self.__goal_depth: int = goal_depth

        self.__boundary_width: int = boundary_width

        self.__field_lines: FieldLineSegment = field_lines

        self.__field_arcs: FieldCircularArc = field_arcs

        self.__penalty_area_depth: int = penalty_area_depth

        self.__penalty_area_width: int = penalty_area_width

    def __str__(self) -> str:
        pass

    @property
    def field_length(self) -> int:
        """field_length

        Returns:
            int: The length of the field.
        """
        return self.__field_length

    @property
    def field_width(self) -> int:
        """field_width

        Returns:
            int: The width of the field.
        """
        return self.__field_width

    @property
    def goal_width(self) -> int:
        """goal_width

        Returns:
            int: The width of the goal.
        """
        return self.__goal_width

    @property
    def goal_depth(self) -> int:
        """goal_depth

        Returns:
            int: The depth of the goal.
        """
        return self.__goal_depth

    @property
    def boundary_width(self) -> int:
        """boundary_width

        Returns:
            int: The width of the boundary.
        """
        return self.__boundary_width

    @property
    def field_lines(self) -> FieldLineSegment:
        """field_lines

        Returns:
            FieldLineSegment: The field lines.
        """
        return self.__field_lines

    @property
    def field_arcs(self) -> FieldCircularArc:
        """field_arcs

        Returns:
            FieldCircularArc: The field arcs.
        """
        return self.__field_arcs

    @property
    def penalty_area_depth(self) -> int:
        """penalty_area_depth

        Returns:
            int: The depth of the penalty area.
        """
        return self.__penalty_area_depth

    @property
    def penalty_area_width(self) -> int:
        """penalty_area_width

        Returns:
            int: The width of the penalty area.
        """
        return self.__penalty_area_width
