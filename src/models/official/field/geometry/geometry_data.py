#!/usr/bin/env python3.10

"""geometry_data.py

    This module is for the GeometryData class.
"""


from models.official.field.geometry.geometry_camera_calibration import (
    GeometryCameraCalibration,
)
from models.official.field.geometry.geometry_field_size import GeometryFieldSize
from models.official.field.geometry.geometry_models import GeometryModels


class GeometryData:
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
        pass

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
