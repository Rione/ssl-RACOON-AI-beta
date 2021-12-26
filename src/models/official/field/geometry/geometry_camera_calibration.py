#!/usr/bin/env python3.10


class GeometryCameraCalibration:
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

        # ˅
        pass
        # ˄

    def __str__(self) -> str:
        pass

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
    def camera_id(self) -> int:
        """camera id

        Return:
            int: camera id
        """
        return self.__camera_id

    @property
    def tz(self) -> float:
        """tz

        Return:
            float: tz
        """
        return self.__tz

    @property
    def q2(self) -> float:
        """q2

        Return:
            float: q2
        """
        return self.__q2

    @property
    def focal_length(self) -> float:
        """focal length

        Return:
            float: focal length
        """
        return self.__focal_length

    @property
    def q3(self) -> float:
        """q3

        Return:
            float: q3
        """
        return self.__q3

    @property
    def ty(self) -> float:
        """ty

        Return:
            float: ty
        """
        return self.__ty

    @property
    def tx(self) -> float:
        """tx

        Return:
            float: tx
        """
        return self.__tx

    @property
    def q1(self) -> float:
        """q1

        Return:
            float: q1
        """
        return self.__q1
