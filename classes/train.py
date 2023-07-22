from __future__ import annotations
from classes.station import Station
from classes.line import Line
import random


class Train:
    """
    A class to represent a Train.

    ...

    Attributes
    ----------
    _id (int): id of the train
    _line (Line): line of the train
    _station (Station): train's current station
    _direction (str): train's current direction
    _is_delayed (bool): train is delayed at current station

    Methods
    -------
    id():
        Returns train id
    line():
        Returns train line
    station_obj():
        Returns train's current station
    station():
        Returns train's current station name
    direction():
        Returns train's current direction
    is_delayed():
        Returns if train is delayed at current station
    set_delay():
        Sets is_delayed by random based on current station's delay probability
    change_direction():
        Changes train's direction from South (S) to North (N) and vice versa
    set_station():
        Changes train's current station
    move():
        Moves train to next/previous station based on direction
    """

    def __init__(self, _id: int, _line: Line, _station: Station, _direction: str):
        """
        Constructs all the necessary attributes for the train object.

        Parameters
        ----------
        _id (int): train id
        _line (Line): train line
        _station (Station): train current station
        _direction (str): train direction
        _is_delayed (bool): whether the train is delayed
        """
        self._id: int = _id
        self._line: Line = _line
        self._station: Station = _station
        self._direction: str = _direction
        self._is_delayed: bool = False

    def id(self) -> int:
        """
        Get train id

        Returns
        -------
        str : train id
        """
        return self._id

    def line(self) -> Line:
        """
        Get train line object

        Returns
        -------
        Line : train line
        """
        return self._line

    def station_obj(self) -> Station:
        """
        Get train staiton

        Returns
        -------
        Staiton : train station
        """
        return self._station

    def station(self) -> str:
        """
        Get train station name

        Returns
        -------
        str : train station name
        """
        return self._station.name()

    def direction(self) -> str:
        """
        Get train direction

        Returns
        -------
        str : train direction
        """
        return self._direction

    def is_delayed(self) -> bool:
        """
        Get whether the train is delayed

        Returns
        -------
        bool : train is delayed or not
        """
        return self._is_delayed

    def set_delay(self) -> None:
        """
        Set train delay by comparing random generated number between 0 and 1
        and the station's delay probability
        """
        self._is_delayed = random.random() < self._station.delay()

    def change_direction(self) -> None:
        """
        Changes the train direction from South (S) to North (N) and vice versa
        """
        self._direction = "N" if (self._direction == "S") else "S"

    def set_station(self) -> None:
        """
        Sets train current station to either next or previous station based on direction
        """
        if self._station.direction() == self.direction():
            if self._station.next_station():
                self._station = self._station.next_station()
            # after moving to next station
            # if the station is last station, change direction
            if not self._station.next_station():
                self.change_direction()
        else:
            if self._station.previous_station():
                self._station = self._station.previous_station()
            # after moving to previous station (next station but opposite direction)
            # if the station is last station, change direction
            if not self._station.previous_station():
                self.change_direction()

    def move(self) -> Train:
        """
        Sets new delay probability to the current station
        and moves train to its next station based on direction if there is no delay
        """
        self.set_delay()
        if not self.is_delayed():
            self.set_station()
            return self
        else:
            return self
