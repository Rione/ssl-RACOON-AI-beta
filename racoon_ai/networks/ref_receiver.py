#!/usr/bin/env python3.10

"""ref_receiver.py

    This module is for the RefReceiver class.
"""

from logging import getLogger

from racoon_ai.models.network import Network
from racoon_ai.proto.pb_gen.ssl_gc_referee_message_pb2 import Referee


class RefReceiver(Network):
    """RefReceiver

    Args:
        host (str, optional): IP address of game controller.
            Defaults to `224.5.23.1`.
        port (int, optional): Port number of game controller.
            Defaults to `10003`.
    """

    def __init__(self, *, host: str = "224.5.23.1", port: int = 10003) -> None:

        super().__init__(port, address=host)

        self.__logger = getLogger(__name__)

    def __del__(self) -> None:
        self.__logger.debug("Destructor called")

    def receive(self) -> None:
        """receive

        Recieve the refereee messages from the gc.

        Return:
            None
        """
        raise NotImplementedError

    def get_command(self) -> "Referee.Command":
        """get_command

        Return:
            Referee.Command: The command received from the referee.

        Note:
            0: HALT
                All robots should completely stop moving.

            1: STOP
                Robots must keep 50 cm from the ball.
            2: NORMAL_START
                A prepared kickoff or penalty may now be taken.

            3: FORCE_START
                A force start is taking place.
            4: PREPARE_KICKOFF_YELLOW
                The yellow team may move into kickoff position.

            5: PREPARE_KICKOFF_BLUE
                The blue team may move into kickoff position.

            6: PREPARE_PENALTY_YELLOW
                The yellow team may move into penalty position.

            7: PREPARE_PENALTY_BLUE
                The blue team may move into penalty position.

            8: DIRECT_FREE_YELLOW
                The yellow team may take a direct free kick.

            9: DIRECT_FREE_BLUE
                The blue team may take a direct free kick.

            10: INDIRECT_FREE_YELLOW
                The yellow team may take an indirect free kick.

            11: INDIRECT_FREE_BLUE
                The blue team may take an indirect free kick.

            12: TIMEOUT_YELLOW
                The yellow team is currently in a timeout.

            13: TIMEOUT_BLUE
                The blue team is currently in a timeout.

            14: GOAL_YELLOW
                The yellow team just scored a goal. Teams must treat as STOP.

            15: GOAL_BLUE
                The blue team just scored a goal. Teams must treat as STOP.

            16: BALL_PLACEMENT_YELLOW
                Equivalent to STOP, but the yellow team must pick up the ball and drop it in the Designated Position.

            17: BALL_PLACEMENT_BLUE
                Equivalent to STOP, but the blue team must pick up the ball and drop it in the Designated Position.
        """
        raise NotImplementedError
