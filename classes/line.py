from classes.station import Station


class Line:
    """
    A class to represent a Line.

    ...

    Attributes
    ----------
    _name (str) : name of the line
    _stations (int) : number of stations on line
    _stations_order (list[Station]) : list of stations objects on line

    Methods
    -------
    name():
        Returns the name of the line
    stations():
        Returns the number of stations on line
    stations_order():
        Returns a list of line's stations objects
    stations_list_string():
        Returns a list of line's stations names
    info():
        Returns dict of line's name and number of stations
    """
    _stations_objects: list[Station]

    def __init__(self, _name: str, _stations: int):
        """
        Constructs all the necessary attributes for the line object.

        Parameters
        ----------
        _name (str): name of the line
        _stations (int): number of stations on line
        """
        self._name: str = _name
        self._total_stations: int = _stations

    def name(self) -> str:
        """
        Get name of the line

        Returns
        -------
        str : name of the line
        """
        return self._name

    def total_stations(self) -> int:
        """
        Get number of stations on line

        Returns
        -------
        int : number of stations
        """
        return self._total_stations

    def stations(self) -> list[Station]:
        """
        Get list of line's stations objects 

        Returns
        -------
        list[Station] : line's stations objects 
        """
        return self._stations_objects

    def stations_list_string(self) -> list[str]:
        """
        Get list of line's stations names 

        Returns
        -------
        list[str] : line's stations names 
        """
        return [x.name() for x in self._stations_objects]
