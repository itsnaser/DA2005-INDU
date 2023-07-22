import argparse
from classes.line import Line
from classes.station import Station
from classes.train import Train
from classes.logic import Logic as lgc

# declaring globals
DATA: list = []
UNIQUE_LINES: list[str] = []
LINES: list[Line] = []
STATIONS: list[Station] = []
TRAINS: list[Train] = []
TRAINS_INDX: str = ""


def main(trains):
    """ 
    Program main menu.
    Options to select from such as:
    1. Simulate the trains
    2. Get train's info by id
    3. Get all trains' info
    4. Route info between two stations
    q. Exit the program
    """
    running: bool = True
    while running:
        user_input = str(
            input("Continue simulation [1], Train info [2], All trains [3], Route info [4] Exit [q].\nSelect an option: "))

        match user_input:
            case "1":
                trains = Lgc.simulate(trains)
            case "2":
                train_id = int(input(f"Which train {TRAINS_INDX} : "))
                print(Lgc.get_train_info(trains, train_id))
            case "3":
                print(Lgc.get_train_info(trains, all=True))
            case "4":
                try:
                    station1 = str(input("Select a start station: "))
                    station2 = str(input("Select an end station: "))
                    timesteps = int(input("Select timesteps: "))
                except ValueError:
                    print("Invalid input!")
                else:
                    if Lgc.is_station(station1, STATIONS) and Lgc.is_station(station2, STATIONS):
                        is_reachable = "is reachable" if (Lgc.get_route_info(
                            STATIONS, station1, station2, timesteps)) else "is not reachable"
                        print(
                            f"Station {station2} {is_reachable} from station {station1} within {timesteps} timesteps.")
                    else:
                        print("Couldn't find one or more of the given stations!")

            case "q" | "Q":
                running = False
            case _:
                print("Invalid input!")

    return False


if __name__ == "__main__":
    # Enter True as debug parameter to run the program in debug mode
    # DEBUG: prints out the result of each function
    parser = argparse.ArgumentParser()
    parser.add_argument('-debug', action="store_true")
    args = parser.parse_args()
    parser.set_defaults(debug=False)

    Lgc = lgc(args.debug)

    validated: bool = True
    while validated:
        connections, stations, no_of_trains = Lgc.get_user_input()

        try:
            splitted_connections = Lgc.validate_connections(
                Lgc.split_data(connections, "connections"))

            splitted_stations = Lgc.validate_stations(
                Lgc.split_data(stations, "stations"))
        except ValueError:
            print("Invalid input!")

        else:
            UNIQUE_LINES = Lgc.get_unique_lines(splitted_connections)

            DATA = Lgc.group_stations(splitted_connections, UNIQUE_LINES)
            DATA = Lgc.create_last_stations(DATA)
            DATA = Lgc.populate_probabilities(DATA, splitted_stations)

            LINES = Lgc.create_lines(DATA, UNIQUE_LINES)

            STATIONS = Lgc.create_stations(DATA)
            STATIONS = Lgc.set_station_objects(STATIONS)

            LINES = Lgc.set_line_stations(LINES, STATIONS)
            STATIONS = Lgc.set_station_line(LINES, STATIONS)
            TRAINS = Lgc.generate_trains(no_of_trains, STATIONS)

            TRAINS_INDX = f"[1 - {len(TRAINS)}]"

            # Make sure that files were formatted correctly,
            # and lines, stations and trains are generated
            # Run the simulation
            if LINES and STATIONS and TRAINS:
                validated = main(TRAINS)
            else:
                validated = False
