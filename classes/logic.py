import os
from typing import Union
import random
from classes.line import Line
from classes.station import Station
from classes.train import Train


class Logic:
    """
    Logic class used to read, manipulate and update
    objects from Line, Station and Train classes.

    ...

    Methods
    ----------
    get_user_input():
        Get connections, station and number of simulated trains
        input from the user
    """

    def __init__(self, debug: bool = False):
        self.debug: bool = debug

    def get_user_input(self):
        """
        Get user input for connections, stations files, and number of trains to simulate.

        Returns
        -------
        list[str]: list of stations' connections 
        list[str]: list of stations' delay probabilities
        int: number of trains to simulate
        """
        not_valid_input: bool = True
        connections, stations, trains = "", "", 0
        while not_valid_input:
            try:
                stations_input = str(
                    input("Enter name of stations file: "))
                connections_input = str(
                    input("Enter name of connections file: "))
                trains = int(
                    input("Enter how many trains to simulate: "))

                # read data
                connections = self.read_data(connections_input)
                stations = self.read_data(stations_input)

                if trains < 1:
                    raise ValueError

            except FileNotFoundError:
                print("File not found!")
            except ValueError:
                print("Invalid input!")
            else:
                not_valid_input = False
        
        return connections, stations, trains

    def read_data(self, filename: str) -> list[str]:
        """
        Read a text file and returns its lines 

        Parameters
        ----------
        filename (str): text file name

        Raises
        ------
        FileNotFoundError: if file does not exist

        Returns
        -------
        list[str]: file data lines
        """
        filename = filename if filename.endswith('.txt') else filename+".txt"
        if not os.path.isfile(filename):
            raise FileNotFoundError
        with open(filename, 'r', encoding="utf-8") as f:
            data: list[str] = f.readlines()
        return data

    def split_data(self, data, split_type: str):
        """
        Splits connections and stations list into sublists 

        Parameters
        ----------
        data (list): list of stations/connections
        split_type (str): type of list

        Raises
        ------
        ValueError: if split_type is invalid

        Returns
        -------
        list[str]: the splitted list
        """
        if split_type.lower() == "connections":
            result = [x.strip().split(",")
                      for x in data if not x.startswith("#")]
        elif split_type.lower() == "stations":
            result = [x.strip().split(",") for x in data]
        else:
            raise ValueError
        return result

    def is_station(self, station: str, staitons: list[Station]) -> bool:
        """
        Checks if input string exists in a stations list

        Parameters
        ----------
        station (str): name of station
        staitons (list[Station]): list of all stations

        Returns
        -------
        bool: whether input string exist in stations
        """
        result: bool = any(x.name() == station for x in staitons)
        return result

    def is_valid(self, list_to_validate: list, type_of_validation: str) -> bool:
        """
        Check if a list format is valid, based on defined format type (connection, station)
        More formats can be defined 

        Parameters
        ----------
        list_to_validate (list): list to validate
        type_of_validation (str): what type of validation

        Returns
        -------
        bool: whether the list is valid or not
        """
        match type_of_validation:
            # connection list format: ["station_name","staiton_name","line_name","direction (N or S)"]
            # length of 4
            # 3rd index must be either "N" or "S"
            case "connection":
                if len(list_to_validate) != 4:
                    return False
                if any(item == "" for item in list_to_validate):
                    return False
                if list_to_validate[3].lower() not in ["s", "n"]:
                    return False
                return True

            # station list format: ["station_name","delay probability"]
            # length of 2
            # delay probability must be able to be converted to float
            case "station":
                if len(list_to_validate) != 2:
                    return False
                if not list_to_validate[0]:
                    return False
                try:
                    list_to_validate[1] = float(list_to_validate[1])
                except:
                    return False
                return True

            case _:
                return False

    def validate_connections(self, connections: list[list[str]]) -> list[list[str]]:
        """
        Validate the connections list by a defined format, and returns list of valid lines

        Parameters
        ----------
        connections (list): list of connections to validate

        Returns
        -------
        list[list[str]]: validated connections (dropping all invalid lines)
        """
        result: list[list[str]] = []
        for connection in connections:
            connection: list[str]
            if self.is_valid(connection, "connection"):
                result.append(connection)

        if self.debug:
            print("\n\n[validate_connections]\n")
            for _station in result:
                print(_station)
        return result

    def validate_stations(self, stations: list[list]) -> list[list[Union[str, float]]]:
        """
        Validate the stations list by a defined format, and returns list of valid lines

        Parameters
        ----------
        stations (list): list of stations to validate

        Returns
        -------
        list[list[Union[str, float]]]: validated stations (dropping all invalid lines)
        """
        result: list[list[Union[str, float]]] = []
        for station in stations:
            station: list
            if self.is_valid(station, "station"):
                result.append(station)

        if self.debug:
            print("\n\n[validate_stations]\n")
            for _station in result:
                print(_station)

        return result

    def get_unique_lines(self, data: list[list[str]]) -> list[str]:
        """
        Get unique lines from stations list

        Parameters
        ----------
        data (list[list[str]]): list of all stations 

        Returns
        -------
        list[str]: list of unique lines
        """
        result = list(set([i[2] for i in data]))
        return result

    def group_stations(self, data: list[list[str]], unique_lines: list[str]) -> list[list[list[str]]]:
        """
        Group stations by line name

        Parameters
        ----------
        data (list[list[str]]): list of all stations
        unique_lines (list[str]): list of unique lines

        Returns
        -------
        list[list[list[str]]]: list of grouped stations 
        example:
        [   # all lines 
            [   # blue line stations
                ["station1","station2","blue","S"],
                ["station2","station3","blue","S"]
            ],
            [   # green line stations
                ["station1","station2","green","N"],
                ["station2","station3","green","N"]
            ]
        ]
        """
        result: list[list[list[str]]] = []
        for line in unique_lines:
            line: str
            # for each line, find all stations that belong to it
            # add it to result as list
            temp = [station for station in data if station[2] == line]
            result.append(temp)

        if self.debug:
            print("\n\n[group_stations]\n")
            for _line in result:
                print(f"\n[LINE - {_line[0][2]}]\n")
                for _station in _line:
                    print(_station)

        return result

    def create_last_stations(self, data: list[list[list[str]]]) -> list[list[list[str]]]:
        """
        Add last stations as individuals since they are not defined in the text files

        Parameters
        ----------
        data (list[list[list[str]]]): list of grouped stations by line

        Returns
        -------
        list[list[list[str]]]: list of grouped stations by line, including last stations 
        """
        result = data.copy()
        for line in result:
            line: list[list[str]]
            from_stations: list[str] = []
            to_stations: list[str] = []
            line_name: str = line[0][2]
            line_direction: str = line[0][3]

            for station in line:
                station: list[str]
                from_stations.append(station[0])
                to_stations.append(station[1])

            for to_station in to_stations:
                if to_station not in from_stations:
                    temp = [to_station, "", line_name, line_direction]
                    line.append(temp)

        if self.debug:
            print("\n\n[validate_last_stations]\n")
            for _line in result:
                print(f"\n[LINE - {_line[0][2]}]\n")
                for _station in _line:
                    print(_station)
        return result

    def populate_probabilities(self, data: list[list[list]], stations_probabilities: list[list]) -> list[list[list]]:
        """
        Set delay probability to each station

        Parameters
        ----------
        connections (list[list[list]]): list of grouped stations by line
        stations (list[list]): list of stations' delay probability

        Returns
        -------
        list[list[list]]: list of grouped stations by line, including delay probability
        """
        length_of_full_station_list = 5
        for line in data:
            line: list[list]
            for index, station in enumerate(line):

                delay_index = next(
                    (stations_probabilities.index(x) for x in stations_probabilities if x[0] == station[0]), None)

                station_dont_have_delay_probability: bool = len(
                    line[index]) != length_of_full_station_list

                if station_dont_have_delay_probability and delay_index is not None:
                    line[index].append(stations_probabilities[delay_index][1])
                else:
                    # for a station, if no delay probability or wrong station name
                    # was provided in the text file, then assign delay to 0
                    station.append(0.0)

        if self.debug:
            print("\n\n[populate_probabilities]\n")
            for _line in data:
                print(f"\n[LINE - {_line[0][2]}]\n")
                for _station in _line:
                    print(_station)
        return data

    def create_lines(self, data: list[list[list]], unique_lines: list) -> list[Line]:
        """
        Create a list of all unique lines as objects

        Parameters
        ----------
        data (list[list[list]]): list of grouped stations by line
        unique_lines (list): list of unique lines

        Returns
        -------
        list[Line]: list of line objects
        """
        result: list[Line] = []
        for line in unique_lines:
            line: str
            total_stations: int = len(
                [_station for _line in data for _station in _line if _station[2] == line])
            result.append(Line(line, total_stations))

        if self.debug:
            print("\n\n[create_lines]\n")
            for _line in result:
                print(
                    f"Line: {_line.name()} - Number of Stations: {_line.total_stations()}")

        return result

    def create_stations(self, data: list[list[list]]) -> list[Station]:
        """
        Create a list of all stations as objects

        Parameters
        ----------
        data (list[list[list]]): list of grouped stations by line

        Returns
        -------
        list[Station]: list of Station objects
        """
        result: list[Station] = []
        for line in data:
            line: list[list]
            for i in range(len(line)):
                previous_station = self.get_previous(line, i)
                try:
                    station: Station = Station(
                        # name
                        line[i][0],
                        # line
                        line[i][2],
                        # delay
                        float(line[i][4]),
                        # next station
                        line[i][1],
                        # previous station
                        previous_station,
                        # direction
                        line[i][3])
                except IndexError:
                    raise IndexError
                result.append(station)
        return result

    def get_previous(self, line: list[list[Union[str, float]]], index: int) -> Union[str, float]:
        """
        Get station's previous station 

        Parameters
        ----------
        line (list[list[Union[str, float]]]): list of line's stations 
        index (int): index of the station to get its previous station

        Returns
        -------
        Union[str, float]: previous station
        """
        result: Union[str, float] = ""
        station_name = line[index]
        for station in line:
            station: list
            if station[1] == station_name[0]:
                result = station[0]
                break

        if self.debug:
            print("\n[get_previous]")
            print(f"Station: {station_name} - Previous Station: {result}")
        return result

    def set_station_objects(self, stations: list[Station]) -> list[Station]:
        """
        Set next and previous stations for each station to a Station object

        Parameters
        ----------
        stations (list[Station]): list of Station objects

        Returns
        -------
        list[Station]: list of Station objects (changed next and previous stations to Station objects)
        """
        result: list[Station] = stations.copy()
        for station in result:
            station: Station
            for second_station in result:
                second_station: Station
                # station1NextStat: str = station.next_station()
                # station1PrevStat: str = station.previous_station()
                # station1Line: str = station.line()
                # station2Line: str = second_station.line()
                # station2: str = second_station.name()
                # same_nxt_station: bool = station1NextStat == station2
                # same_prv_station: bool = station1PrevStat == station2
                # same_lines: bool = station1Line == station2Line
                same_nxt_station: bool = station.next_station() == second_station.name()
                same_prv_station: bool = station.previous_station() == second_station.name()
                same_lines: bool = station.line() == second_station.line()
                if (same_nxt_station and same_lines):
                    station._next_station = second_station
                elif (same_prv_station and same_lines):
                    station._previous_station = second_station
        return result

    def set_line_stations(self, lines: list[Line], stations: list[Station]) -> list[Line]:
        """
        Set line's stations as Station objects

        Parameters
        ----------
        lines (list[Line]): list of Line objects
        stations (list[Station]): list of Station objects

        Returns
        -------
        list[Line]: list of Line objects
        """
        result: list = lines.copy()
        for line in result:
            line._stations_objects = [
                x for x in stations if x.line() == line.name()]
        return result

    def set_station_line(self, lines: list[Line], stations: list[Station]) -> list[Station]:
        """
        Set station's line as Line object

        Parameters
        ----------
        lines (list[Line]): list of Line objects
        stations (list[Station]): list of Station objects

        Returns
        -------
        list[Station]: list of Station objects
        """
        result: list[Station] = stations.copy()
        for station in result:
            for line in lines:
                if station.line() == line.name():
                    station._line = line
        return result

    def generate_trains(self, number_of_trains: int, stations: list[Station]) -> list[Train]:
        """
        Generate trains and set them at random line, station and driection

        Parameters
        ----------
        number_of_trains (int): number of trains to generate
        stations (list[Station]): list of Station objects

        Returns
        -------
        list[Train]: list of Train objects
        """
        if not stations:
            return []
        result: list[Train] = []

        for number in range(1, number_of_trains+1):
            station = random.choice(stations)
            result.append(
                Train(
                    number,
                    station.line(),
                    station,
                    random.choice(["N", "S"])
                )
            )
        return result

    def simulate(self, trains: list[Train]) -> list[Train]:
        """
        Simulate all trains one turn

        Parameters
        ----------
        trains list[Train]: list of Train objects to simulate

        Returns
        -------
        list[Train]: list of Train objects after the simulation
        """
        result: list[Train] = trains.copy()
        for train in result:
            train: Train
            train = train.move()
        return result

    # TODO: create type hints, and refactor

    def get_train_info(self, trains: list[Train], train_id: int = 0, all: bool = False) -> str:
        """
        Get information about a train by id, or all trains by giving True value to "all" parameter

        Parameters
        ----------
        trains (list[Train]): list of Train objects to get information from
        train_id (int) default 0: train id to get its information
        all (bool) default False: gets all trains information

        Returns
        -------
        str: printed string of train information
        """
        if all:
            result: str = ""
            for train in trains:
                train: Train
                # check if train is delayed, and add (DELAY) to the result if it is True.
                # and build the result string
                delayed: str = "(DELAY)" if (train.is_delayed()) else ""
                result += f'\nTrain {train.id()} on {train.line().name().upper()} line is at station {train.station()} heading in {train.direction()} direction {delayed}\n'
            return result
        else:
            for train in trains:
                train: Train
                # find the Train object
                if train.id() == int(train_id):
                    # build the result string
                    delayed = "(DELAY)" if (train.is_delayed()) else ""
                    return f'\nTrain {train.id()} on {train.line().name().upper()} line is at station {train.station()} heading in {train.direction()} direction {delayed}\n'
        return ""

    def get_station_obj(self, stations: list[Station], station: str) -> Union[Station, None]:
        """
        Get Station object from stations list by station name string

        Parameters
        ----------
        stations (list[Station]): stations list to get the Station object from
        station (str): station name to get its Station object

        Returns
        -------
        Union[Station, None]: whether the Station object or None if not found
        """
        for _station in stations:
            if _station.name().lower() == station.lower():
                return _station

    def get_common_stations(self, station1: Station, station2: Station) -> list[Station]:
        """
        Get if two stations have a common station

        Parameters
        ----------
        station1 (Station): first station 
        station2 (Station): second station

        Returns
        -------
        list[Station]: list of all common stations
        """
        # store all stations on the same line of stations one and two (parameters)
        station1_line_stations = station1.line().stations()
        station2_line_stations = [x.name() for x in station2.line().stations()]
        common_stations = [station for station in station1_line_stations
                           if station.name() in station2_line_stations]
        return common_stations

    def get_shortest_common_steps(self, station1: Station, station2: Station, common_stations: list[Station]) -> int:
        """
        Get the shortest path from station 1 to station 2 by going through a common station 

        Parameters
        ----------
        station1 (Station): first station
        station2 (Station): second station
        common_stations list[Station]: list of all common stations

        Returns
        -------
        int: number of steps of the shortest path
        """
        steps: int = 9999
        for common_station in common_stations:
            station1_steps: int = self.get_timesteps(station1, common_station)
            station2_steps: int = self.get_timesteps(station2, common_station)
            total_steps: int = station1_steps + station2_steps
            # if steps is greater than total_steps then update its value to total_steps,
            # otherwise keep steps value unchanged.
            steps = total_steps if total_steps < steps else steps
        return steps

    def get_timesteps(self, station1: Station, station2: Station) -> int:
        """
        Get number of steps between two stations on the same line

        Parameters
        ----------
        station1 (Station): first station
        station2 (Station): second station

        Returns
        -------
        int: absoulte value of steps between two stations
        """
        # get line's stations "in order", then find each station's index,
        # then subtract the indexes from each other and return the absoulte value
        stations_order: list[str] = station1.line().stations_list_string()
        station1_indx: int = stations_order.index(station1.name())
        station2_indx: int = stations_order.index(station2.name())
        return abs(station2_indx - station1_indx)

    def get_route_info(self, stations: list[Station], station1: str, station2: str, timesteps: int) -> bool:
        """
        Check if it is possible to get from station 1 to station 2 by "t" timesteps

        Parameters
        ----------
        stations (list[Station]): list of Station objects
        station1 (str): first station
        station2 (str): second station
        timesteps (int): amount timesteps 

        Returns
        -------
        bool: whether station 2 is reachable from station 1 by "t" timesteps
        """
        st1_obj: Union[Station, None] = self.get_station_obj(
            stations, station1)
        st2_obj: Union[Station, None] = self.get_station_obj(
            stations, station2)

        if not st1_obj or not st2_obj:
            print("Invalid station names")
            return False

        on_same_line: bool = st1_obj.line() == st2_obj.line()

        if on_same_line:
            station1_to_station2: int = self.get_timesteps(st1_obj, st2_obj)
            is_reachable: bool = timesteps >= station1_to_station2

        else:  # different lines
            # get all common stations between station1 and station2
            # find out which common station has the shortest path
            # check if total timesteps is in range of the wished timesteps
            common_stations: list[Station] = self.get_common_stations(
                st1_obj, st2_obj)
            if not common_stations:
                return False
            shortest_common_station: int = self.get_shortest_common_steps(
                st1_obj, st2_obj, common_stations)
            is_reachable: bool = timesteps >= shortest_common_station

        return is_reachable
