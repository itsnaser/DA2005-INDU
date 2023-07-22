class Station:
    """
    A class to represent a Station.

    ...

    Attributes
    ----------
    _name (str) : name of the station
    _line (Line) : line object of the station
    _delay_probability (float) : station's delay probability
    _next_station (Station) : next station as object
    _previous_station (Station) : previous station as object
    _direction (str) : direction to next station

    Methods
    -------
    name():
        Returns the name of the station
    line():
        Returns the line of the station object
    delay():
        Returns station's delay probability
    next_station():
        Returns station's next station object
    previous_station():
        Returns station's previous station object
    direction():
        Returns direction to next station
        Returns dict of station's all info
    """

    def __init__(self, _name: str, _line, _delay_probability: float, _next_station, _previous_station, _direction: str):
        """
        Constructs all the necessary attributes for the station object.

        Parameters
        ----------
        _name (str): name of the station
        _line (int): line of the station
        _delay_probability (float): station's delay probability
        _next_station (Station): next station object
        _previous_station (Station): previous station object
        _direction (str): direction to next station
        """
        self._name: str = _name
        self._line = _line
        self._delay_probability: float = _delay_probability
        self._next_station = _next_station
        self._previous_station = _previous_station
        self._direction: str = _direction

    def name(self) -> str:
        """
        Get name of the station

        Returns
        -------
        str : name of the station
        """
        return self._name

    def line(self):
        """
        Get line object of the station

        Returns
        -------
        Line : line object
        """
        return self._line

    def delay(self) -> float:
        """
        Get station delay probability

        Returns
        -------
        float : delay probability
        """
        return self._delay_probability

    def next_station(self):
        """
        Get next station object

        Returns
        -------
        Station : next station object
        """
        return self._next_station

    def previous_station(self):
        """
        Get previous station object

        Returns
        -------
        Station : previous station object
        """
        return self._previous_station

    def direction(self) -> str:
        """
        Get direction to next station

        Returns
        -------
        str : direction to next station
        """
        return self._direction
