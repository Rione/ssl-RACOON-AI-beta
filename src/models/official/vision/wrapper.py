#!/usr/bin/env python3.10

"""wrapper.py

    This module contains:
        - WrapperPacket

    See also:
        https://github.com/RoboCup-SSL/ssl-vision/blob/master/src/shared/proto/messages_robocup_ssl_wrapper.proto
"""

from models.official.vision.detection import DetectionFrame
from models.official.vision.geometry import GeometryData


class WrapperPacket:
    """WrapperPacket

    Attributes:
        detection (DetectionFrame): The detection frame.
        geometry (GeometryData): The geometry data.
    """

    def __init__(self, detection: DetectionFrame, geomrtry: GeometryData) -> None:

        self.__detection: DetectionFrame = detection

        self.__geometry: GeometryData = geomrtry

    @property
    def detection(self) -> DetectionFrame:
        """detection

        Returns:
            DetectionFrame:
        """

        return self.__detection

    @property
    def geometry(self) -> GeometryData:
        """geometry

        Returns:
            GeometryData:
        """

        return self.__geometry