#!/usr/bin/env python3.10

"""wrapper_tracked.py

    This module contains:
        - TrackerWrapperPacket

    See also:
        https://github.com/RoboCup-SSL/ssl-vision/blob/master/src/shared/proto/messages_robocup_ssl_wrapper_tracked.proto
"""


from models.official.vision.detection_tracked import TrackedFrame


class TrackerWrapperPacket:
    """TrackerWrapperPacket

    A wrapper packet containing meta data of the source
    Also serves for the possibility to extend the protocol later

    Attributes:
        uuid (str):
            A random UUID of the source that is kept constant while running.
            If multiple sources are broadcasting to the same network, this
            id can be used to identify individual sources
        source_name (str):
            The name of the source software that is producing this messages.
        tracked_frame (TrackedFrame):
            The tracked frame.
    """

    def __init__(
        self,
        uuid: str,
        source_name: str,
        tracked_frame: TrackedFrame,
    ) -> None:

        self.__uuid: str = uuid

        self.__source_name: str = source_name

        self.__tracked_frame: TrackedFrame = tracked_frame

    def __str__(self) -> str:
        return (
            "TrackerWrapperPacket("
            f"uuid={self.uuid}, "
            f"source_name={self.source_name}, "
            f"tracked_frame={self.tracked_frame}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "TrackerWrapperPacket("
            f"{self.uuid}, "
            f"{self.source_name}, "
            f"{self.tracked_frame}"
            ")"
        )

    @property
    def uuid(self) -> str:
        """uuid

        Returns:
            str:
        """
        return self.__uuid

    @property
    def source_name(self) -> str:
        """source_name

        Returns:
            str:
        """
        return self.__source_name

    @property
    def tracked_frame(self) -> TrackedFrame:
        """tracked_frame

        Returns:
            TrackedFrame:
        """
        return self.__tracked_frame
