#!/usr/bin/env python3.10

"""geometry.py

    This module contains:
        - FieldShapeType
        - FieldLineSegment
        - FieldCirclerArc
        - GeometryFieldSize
        - GeometryCameraCalibration
        - BallModelStraightTwoPhase
        - BallModelChipFixedLoss

    See also:
        https://github.com/RoboCup-SSL/ssl-vision/blob/master/src/shared/proto/messages_robocup_ssl_geometry.proto
"""

from enum import Enum

from racoon_ai.models.vision.coordinate import Vector2f


class FieldShapeType(Enum):
    """FieldShapeType

    This enum represents the type of a field shape.
    """

    UNDEFINED = 0

    CENENTER_CIRCLE = 1

    TOP_TOUCHLINE = 2

    BOTTOM_TOUCHLINE = 3

    LEFT_GOALLINE = 4

    RIGHT_GOALLINE = 5

    HALFWAY_LINE = 6

    CENTER_LINE = 7

    LEFT_PENALTY_STRETCH = 8

    RIGHT_PENALTY_STRETCH = 9

    LEFT_FIELD_LEFT_PENALTY_STRETCH = 10

    LEFT_FIELD_RIGHT_PENALTY_STRETCH = 11

    RIGHT_FIELD_LEFT_PENALTY_STRETCH = 12

    RIGHT_FIELD_RIGHT_PENALTY_STRETCH = 13


class FieldLineSegment:
    """FieldLineSegment

    Attributes:
        name (str):
            Name of the line segment.
        p1 (Vector2f):
            Start point of the line segment.
        p2 (Vector2f):
            End point of the line segment.
        thickness (float):
            Thickness of the line segment.
        type (FieldShapeType, optional):
            Type of the line segment.
    """

    def __init__(
        self,
        name: str,
        p1: Vector2f,
        p2: Vector2f,
        thickness: float,
        field_shape_type: FieldShapeType = FieldShapeType.UNDEFINED,
    ):
        self.__name: str = name

        # Start point of the line segment.
        self.__p1: Vector2f = p1

        # End point of the line segment.
        self.__p2: Vector2f = p2

        # Thickness of the line segment.
        self.__thickness: float = thickness

        # Type of the line segment.
        self.__field_shape_type: FieldShapeType = field_shape_type

    def __str__(self) -> str:
        return "FieldLineSegment("

    def __repr__(self) -> str:
        return (
            "FieldLineSegment("
            f"name={self.name}, "
            f"p1={self.p1!s}, "
            f"p2={self.p2!s}, "
            f"thickness={self.thickness:.1f}, "
            f"type={self.field_shape_type}"
            ")"
        )

    @property
    def name(self) -> str:
        return self.__name

    @property
    def p1(self) -> Vector2f:
        return self.__p1

    @property
    def p2(self) -> Vector2f:
        return self.__p2

    @property
    def thickness(self) -> float:
        return self.__thickness

    @property
    def field_shape_type(self) -> FieldShapeType:
        return self.__field_shape_type


class FieldCircularArc:
    """FieldCircularArc

    Attributes:
        name (str):
            Name of this field marking.
        center (Vector2f):
            Center point of the circular arc.
        radius (float):
            Radius of the arc.
        a1 (float):
            Start angle in counter-clockwise order.
        a2 (float):
            End angle in counter-clockwise order.
        thickness (float):
            Thickness of the arc.
        type (FieldShapeType, optional):
            The type of this shape
    """

    def __init__(
        self,
        name: str,
        center: Vector2f,
        radius: float,
        a1: float,
        a2: float,
        thickness: float,
        field_shape_type: FieldShapeType = FieldShapeType.UNDEFINED,
    ):

        self.__name: str = name

        self.__center: Vector2f = center

        self.__radius: float = radius

        self.__a1: float = a1

        self.__a2: float = a2

        self.__thickness: float = thickness

        self.__field_shape_type: FieldShapeType = field_shape_type

    def __str__(self) -> str:
        return (
            "FieldCircularArc("
            f"name={self.name}, "
            f"center={self.center:.1f}, "
            f"radius={self.radius:.1f}, "
            f"a1={self.a1:.1f}, "
            f"a2={self.a2:.1f}, "
            f"thickness={self.thickness:.1f}, "
            f"type={self.field_shape_type}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "FieldCircularArc("
            f"{self.name}, "
            f"{self.center}, "
            f"{self.radius}, "
            f"{self.a1}, "
            f"{self.a2}, "
            f"{self.thickness}, "
            f"{self.field_shape_type}"
            ")"
        )

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
    def field_shape_type(self) -> FieldShapeType:
        """type

        Returns:
            FieldShapeType: The type of this shape
        """
        return self.__field_shape_type


class GeometryFieldSize:
    """GeometryFieldSize

    Attributes:
        field_length (int):
            The length of the field.
        field_width (int):
            The width of the field.
        goal_width (int):
            The width of the goal.
        goal_depth (int):
            The depth of the goal.
        boundary_width (int):
            The width of the boundary.
        field_lines (FieldLineSegment):
            The field lines.
        field_arcs (FieldCircularArc):
            The field arcs.
        penalty_area_depth (int, optional):
            The depth of the penalty area.
        penalty_area_width (int, optional):
            The width of the penalty area.
        center_circle_radius (int, optional):
            The radius of the center circle.
        line_thickness (int, optional):
            The width of the lines.
        goal_center_to_penalty_mark (int, optional):
            The distance between the goal center and the penalty mark.
        goal_height (int, optional):
            The height of the goal.
        ball_radius (int, optional):
            The radius of the ball.
        max_robot_radius (int, optional):
            The maximum radius of a robot.
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
        center_circle_radius: int = 0,
        line_thickness: int = 0,
        goal_center_to_penalty_mark: int = 0,
        goal_height: int = 0,
        goal_radius: float = 0,
        max_robot_radius: float = 0,
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

        self.__center_circle_radius: int = center_circle_radius

        self.__line_thickness: int = line_thickness

        self.__goal_center_to_penalty_mark: int = goal_center_to_penalty_mark

        self.__goal_height: int = goal_height

        self.__ball_radius: float = goal_radius

        self.__max_robot_radius: float = max_robot_radius

    def __str__(self) -> str:
        return (
            "GeometryFieldSize("
            f"field_length={self.field_length}, "
            f"field_width={self.field_width}, "
            f"goal_width={self.goal_width}, "
            f"goal_depth={self.goal_depth}, "
            f"boundary_width={self.boundary_width}, "
            f"field_lines={self.field_lines!s}, "
            f"field_arcs={self.field_arcs!s}, "
            f"penalty_area_depth={self.penalty_area_depth}, "
            f"penalty_area_width={self.penalty_area_width}, "
            f"center_circle_radius={self.center_circle_radius}, "
            f"line_thickness={self.line_thickness}, "
            f"goal_center_to_penalty_mark={self.goal_center_to_penalty_mark}, "
            f"goal_height={self.goal_height}, "
            f"ball_radius={self.ball_radius:.1f}, "
            f"max_robot_radius={self.max_robot_radius:.1f}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "GeometryFieldSize("
            f"{self.field_length}, "
            f"{self.field_width}, "
            f"{self.goal_width}, "
            f"{self.goal_depth}, "
            f"{self.boundary_width}, "
            f"{self.field_lines}, "
            f"{self.field_arcs}, "
            f"{self.penalty_area_depth}, "
            f"{self.penalty_area_width}, "
            f"{self.center_circle_radius}, "
            f"{self.line_thickness}, "
            f"{self.goal_center_to_penalty_mark}, "
            f"{self.goal_height}, "
            f"{self.ball_radius}, "
            f"{self.max_robot_radius}"
            ")"
        )

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

    @property
    def center_circle_radius(self) -> int:
        """center_circle_radius

        Returns:
            int: The radius of the center circle.
        """
        return self.__center_circle_radius

    @property
    def line_thickness(self) -> int:
        """line_thickness

        Returns:
            int: The width of the lines.
        """
        return self.__line_thickness

    @property
    def goal_center_to_penalty_mark(self) -> int:
        """goal_center_to_penalty_mark

        Returns:
            int: The distance between the goal center and the penalty mark.
        """
        return self.__goal_center_to_penalty_mark

    @property
    def goal_height(self) -> int:
        """goal_height

        Returns:
            int: The height of the goal.
        """
        return self.__goal_height

    @property
    def ball_radius(self) -> float:
        """ball_radius

        Returns:
            float: The radius of the ball.
        """
        return self.__ball_radius

    @property
    def max_robot_radius(self) -> float:
        """max_robot_radius

        Returns:
            float: The maximum radius of a robot.
        """
        return self.__max_robot_radius


class GeometryCameraCalibration:
    """GeometryCameraCalibration

    Attributes:
        camera_id (int):
            The camera id.
        focal_length (float):
            The focal length.
        principal_point_x (float):
            The x-coordinate of principal point.
        principal_point_y (float):
            The y-coordinate of principal point.
        distortion (float):
            The distortion coefficient.
        q0 (float):
            The q0 coefficient.
        q1 (float):
            The q1 coefficient.
        q2 (float):
            The q2 coefficient.
        q3 (float):
            The q3 coefficient.
        tx (float):
            The translation along x-axis.
        ty (float):
            The translation along y-axis.
        tz (float):
            The translation along z-axis.
        derived_camera_world_tx (float, optional):
            The derived camera world translation along x-axis.
        derived_camera_world_ty (float, optional):
            The derived camera world translation along y-axis.
        derived_camera_world_tz (float, optional):
            The derived camera world translation along z-axis.
        pixel_image_width (int, optional):
            The pixel image width.
        pixel_image_height (int, optional):
            The pixel image height.
    """

    def __init__(
        self,
        camera_id: int,
        focal_length: float,
        principal_point_x: float,
        principal_point_y: float,
        distortion: float,
        q0: float,
        q1: float,
        q2: float,
        q3: float,
        tx: float,
        ty: float,
        tz: float,
        derived_camera_world_tx: float = 0,
        derived_camera_world_ty: float = 0,
        derived_camera_world_tz: float = 0,
        pixel_image_width: int = 0,
        pixel_image_height: int = 0,
    ):

        self.__camera_id: int = camera_id

        self.__focal_length: float = focal_length

        self.__principal_point_x: float = principal_point_x

        self.__principal_point_y: float = principal_point_y

        self.__distortion: float = distortion

        self.__q0: float = q0

        self.__q1: float = q1

        self.__q2: float = q2

        self.__q3: float = q3

        self.__tx: float = tx

        self.__ty: float = ty

        self.__tz: float = tz

        self.__derived_camera_world_tx: float = derived_camera_world_tx

        self.__derived_camera_world_ty: float = derived_camera_world_ty

        self.__derived_camera_world_tz: float = derived_camera_world_tz

        self.__pixel_image_width: int = pixel_image_width

        self.__pixel_image_height: int = pixel_image_height

    def __str__(self) -> str:
        return (
            "GeometryCameraCalibration("
            f"camera_id={self.camera_id}, "
            f"focal_length={self.focal_length:.1f}, "
            f"principal_point_x={self.principal_point_x:.1f}, "
            f"principal_point_y={self.principal_point_y:.1f}, "
            f"distortion={self.distortion:.1f}, "
            f"q0={self.q0:.1f}, "
            f"q1={self.q1:.1f}, "
            f"q2={self.q2:.1f}, "
            f"q3={self.q3:.1f}, "
            f"tx={self.tx:.1f}, "
            f"ty={self.ty:.1f}, "
            f"tz={self.tz:.1f}, "
            f"derived_camera_world_tx={self.derived_camera_world_tx:.1f}, "
            f"derived_camera_world_ty={self.derived_camera_world_ty:.1f}, "
            f"derived_camera_world_tz={self.derived_camera_world_tz:.1f}, "
            f"pixel_image_width={self.pixel_image_width}, "
            f"pixel_image_height={self.pixel_image_height}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "GeometryCameraCalibration("
            f"{self.camera_id}, "
            f"{self.focal_length}, "
            f"{self.principal_point_x}, "
            f"{self.principal_point_y}, "
            f"{self.distortion}, "
            f"{self.q0}, "
            f"{self.q1}, "
            f"{self.q2}, "
            f"{self.q3}, "
            f"{self.tx}, "
            f"{self.ty}, "
            f"{self.tz}, "
            f"{self.derived_camera_world_tx}, "
            f"{self.derived_camera_world_ty}, "
            f"{self.derived_camera_world_tz}, "
            f"{self.pixel_image_width}, "
            f"{self.pixel_image_height}"
            ")"
        )

    @property
    def camera_id(self) -> int:
        """camera id

        Return:
            int: camera id
        """
        return self.__camera_id

    @property
    def focal_length(self) -> float:
        """focal length

        Return:
            float: focal length
        """
        return self.__focal_length

    @property
    def principal_point_x(self) -> float:
        """principal point x

        Return:
            float: principal point x
        """
        return self.__principal_point_x

    @property
    def principal_point_y(self) -> float:
        """principal point y

        Return:
            float: principal point y
        """
        return self.__principal_point_y

    @property
    def distortion(self) -> float:
        """distortion

        Return:
            float: distortion
        """
        return self.__distortion

    @property
    def q0(self) -> float:
        """q0

        Return:
            float: q0
        """
        return self.__q0

    @property
    def q1(self) -> float:
        """q1

        Return:
            float: q1
        """
        return self.__q1

    @property
    def q2(self) -> float:
        """q2

        Return:
            float: q2
        """
        return self.__q2

    @property
    def q3(self) -> float:
        """q3

        Return:
            float: q3
        """
        return self.__q3

    @property
    def tx(self) -> float:
        """tx

        Return:
            float: tx
        """
        return self.__tx

    @property
    def ty(self) -> float:
        """ty

        Return:
            float: ty
        """
        return self.__ty

    @property
    def tz(self) -> float:
        """tz

        Return:
            float: tz
        """
        return self.__tz

    @property
    def derived_camera_world_tx(self) -> float:
        """derived_camera_world_tx

        Return:
            float: derived_camera_world_tx
        """
        return self.__derived_camera_world_tx

    @property
    def derived_camera_world_ty(self) -> float:
        """derived_camera_world_ty

        Return:
            float: derived_camera_world_ty
        """
        return self.__derived_camera_world_ty

    @property
    def derived_camera_world_tz(self) -> float:
        """derived_camera_world_tz

        Return:
            float: derived_camera_world_tz
        """
        return self.__derived_camera_world_tz

    @property
    def pixel_image_width(self) -> int:
        """pixel_image_width

        Return:
            int: pixel_image_width
        """
        return self.__pixel_image_width

    @property
    def pixel_image_height(self) -> int:
        """pixel_image_height

        Return:
            int: pixel_image_height
        """
        return self.__pixel_image_height


class BallModelStraightTwoPhase:
    """BallModelStraightTwoPhase

    Attributes:
        acc_slide (float):
            Ball sliding acceleration [m/s^2] (should be negative)
        acc_role (float):
            Ball rolling acceleration [m/s^2] (should be negative)
        k_switch (float):
            Fraction of the initial velocity where the ball starts to roll
    """

    def __init__(self, acc_slide: float, acc_role: float, k_switch: float):

        self.__acc_slide: float = acc_slide

        self.__acc_role: float = acc_role

        self.__k_switch: float = k_switch

    def __str__(self) -> str:
        return (
            "BallModelStraightTwoPhase("
            f"acc_slide={self.acc_slide:.2f}, "
            f"acc_role={self.acc_role:.2f}, "
            f"k_switch={self.k_switch:.2f}"
            ")"
        )

    def __repr__(self) -> str:
        return "BallModelStraightTwoPhase(" f"{self.acc_slide}, " f"{self.acc_role}, " f"{self.k_switch}" ")"

    @property
    def acc_slide(self) -> float:
        """acc_slide

        Return:
            float: acc_slide
        """
        return self.__acc_slide

    @property
    def acc_role(self) -> float:
        """acc_role

        Return:
            float: acc_role
        """
        return self.__acc_role

    @property
    def k_switch(self) -> float:
        """k_switch

        Return:
            float: k_switch
        """
        return self.__k_switch


class BallModelChipFixedLoss:
    """BallModelChipFixedLoss

    Attributes:
        damping_xy_first_hop (float):
            Chip kick velocity damping factor in XY direction for the first hop
        damping_xy_other_hop (float):
            Chip kick velocity damping factor in XY direction for all following hops
        damping_z (float):
            Chip kick velocity damping factor in Z direction for all hops
    """

    def __init__(self, damping_xy_first_hop: float, damping_xy_other_hop: float, damping_z: float):

        self.__damping_xy_first_hop: float = damping_xy_first_hop

        self.__damping_xy_other_hop: float = damping_xy_other_hop

        self.__damping_z: float = damping_z

    def __str__(self) -> str:
        return (
            "BallModelChipFixedLoss("
            f"damping_xy_first_hop={self.damping_xy_first_hop:.2f}, "
            f"damping_xy_other_hop={self.damping_xy_other_hop:.2f}, "
            f"damping_z={self.damping_z:.2f}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "BallModelChipFixedLoss("
            f"{self.damping_xy_first_hop}, "
            f"{self.damping_xy_other_hop}, "
            f"{self.damping_z}"
            ")"
        )

    @property
    def damping_xy_first_hop(self) -> float:
        """damping_xy_first_hop

        Return:
            float: damping_xy_first_hop
        """
        return self.__damping_xy_first_hop

    @property
    def damping_xy_other_hop(self) -> float:
        """damping_xy_other_hop

        Return:
            float: damping_xy_other_hop
        """
        return self.__damping_xy_other_hop

    @property
    def damping_z(self) -> float:
        """damping_z

        Return:
            float: damping_z
        """
        return self.__damping_z


class GeometryModels:
    """GeometryModels

    Attributes:
        straight_two_phase (BallModelStraightTwoPhase):
            Ball model for straight two phase
        chip_fixed_loss (BallModelChipFixedLoss):
            Ball model for chip fixed loss
    """

    def __init__(
        self,
        straight_two_phase: BallModelStraightTwoPhase,
        chip_fixed_loss: BallModelChipFixedLoss,
    ):

        self.__straight_two_phase: BallModelStraightTwoPhase = straight_two_phase

        self.__chip_fixed_loss: BallModelChipFixedLoss = chip_fixed_loss

    def __str__(self) -> str:
        return (
            "GeometryModels("
            f"straight_two_phase={self.straight_two_phase!s}, "
            f"chip_fixed_loss={self.chip_fixed_loss!s}"
            ")"
        )

    def __repr__(self) -> str:
        return "GeometryModels(" f"{self.straight_two_phase}, " f"{self.chip_fixed_loss}" ")"

    @property
    def straight_two_phase(self) -> BallModelStraightTwoPhase:
        """ball_model_straight_two_phase

        Return:
            BallModelStraightTwoPhase: ball_model_straight_two_phase
        """
        return self.__straight_two_phase

    @property
    def chip_fixed_loss(self) -> BallModelChipFixedLoss:
        """ball_model_chip_fixed_loss

        Return:
            BallModelChipFixedLoss: ball_model_chip_fixed_loss
        """
        return self.__chip_fixed_loss


class GeometryData:
    """GeometryData

    Attributes:
        field (GeometryFieldSize):
            Field size
        calib (GeometryCameraCalibration):
            Camera calibration
        models (GeometryModels):
            Ball models
    """

    def __init__(
        self,
        field: GeometryFieldSize,
        calib: GeometryCameraCalibration,
        models: GeometryModels,
    ) -> None:

        self.__field: GeometryFieldSize = field

        self.__calib: GeometryCameraCalibration = calib

        self.__models: GeometryModels = models

    def __str__(self) -> str:
        return "GeometryData(" f"field={self.field!s}, " f"calib={self.calib!s}, " f"models={self.models!s}" ")"

    def __repr__(self) -> str:
        return "GeometryData(" f"{self.field!r}, " f"{self.calib!r}, " f"{self.models!r}" ")"

    @property
    def calib(self) -> GeometryCameraCalibration:
        """camera calibration

        Return:
            GeometryCameraCalibration: camera calibration
        """
        return self.__calib

    @property
    def field(self) -> GeometryFieldSize:
        """field

        Return:
            GeometryFieldSize: field
        """
        return self.__field

    @property
    def models(self) -> GeometryModels:
        """models

        Return:
            GeometryModels: models
        """
        return self.__models
