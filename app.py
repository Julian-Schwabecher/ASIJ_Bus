import math
from dataclasses import dataclass

import pandas as pd


@dataclass(order=True)
class Coordinate:
    lat: float
    lon: float

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def __post_init__(self):
        if (not ((self.lat > 35.5) and (self.lat < 35.85))) or (
            not ((self.lon > 139.4) and (self.lon < 139.9))
        ):
            raise ValueError

    def distance_to(self, other):
        lat_1 = (self.lat * math.pi) / 180
        lon_1 = (self.lon * math.pi) / 180
        lat_2 = (other.lat * math.pi) / 180
        lon_2 = (other.lon * math.pi) / 180
        a = math.sin((lat_2 - lat_1) / 2) ** 2 + math.cos(lat_1) * math.cos(lat_2) * (
            math.sin((lon_2 - lon_1) / 2) ** 2
        )
        b = 2 * 6371 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return b

    def __str__(self):
        return f"Lat: {self.lat}\nLon: {self.lon}\n"


class BusStop:
    stop_id: str
    location: Coordinate
    name: str

    def __init__(self, location):
        self.location = location

    def __hash__(self):
        return hash(self.stop_id)

    def __eq__(self, other):
        return self.stop_id == other.stop_id

    def __str__(self):
        return str(self.location)


class BusRoute:
    route_id: str
    time: str
    stops: list[BusStop]

    def __init__(self, time):
        self.time = time
        self.stops = []

    def __len__(self):
        len(self.stops)

    def __getitem__(self, index):
        return self.stops[index]

    def add_stops(self, stop: BusStop):
        self.stops.append(stop)

    def __str__(self):
        string = self.time + "\n"
        for index, stop in enumerate(self.stops):
            string += f"Stop Number: {index}\n"
            string += str(stop) + "\n"
        return string


class Bus:
    bus_number: int
    routes: list[BusRoute]
    capacity: int = 50
    monitors: list[str]

    def __init__(self, bus_number, routes) -> None:
        self.bus_number = bus_number
        self.routes = routes

    def getRoutes(self):
        return self.routes

    def __str__(self):
        string = f"Bus Number: {self.bus_number}\n\n"
        for route in self.routes:
            string += str(route) + "\n"
        return string


buses = []

df = pd.read_csv("/Users/julian/Code/Bus/Bus_Stops_2526_clean.csv")
current = 0
next = 0
for index, row in df.iterrows():
    next = row["Bus"]
    if not (next == current):
        buses.append(
            Bus(
                bus_number=row["Bus"], routes=[BusRoute(time="AM"), BusRoute(time="PM")]
            )
        )
        current_routes = buses[-1].getRoutes()
        current = next
        current_routes[0].add_stops(
            BusStop(location=Coordinate(lat=row["AM_lat"], lon=row["AM_long"]))
        )
        current_routes[1].add_stops(
            BusStop(location=Coordinate(lat=row["PM_lat"], lon=row["PM_long"]))
        )
    else:
        current = next
        current_routes[0].add_stops(
            BusStop(location=Coordinate(lat=row["AM_lat"], lon=row["AM_long"]))
        )
        current_routes[1].add_stops(
            BusStop(location=Coordinate(lat=row["PM_lat"], lon=row["PM_long"]))
        )


for bus in buses:
    print(bus)
