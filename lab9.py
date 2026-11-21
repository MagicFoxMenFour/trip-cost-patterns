"""Пересчёт сметы при изменении маршрута и восстановление версии."""
from argparse import ArgumentParser, ArgumentTypeError
from dataclasses import dataclass
from decimal import Decimal

from money import amount, money


@dataclass(frozen=True)
class Snapshot:
    distance: Decimal


class Route:
    def __init__(self, changed):
        self.distance = Decimal(0)
        self.changed = changed

    def set_distance(self, km):
        self.distance = km
        self.changed()

    def save(self):
        return Snapshot(self.distance)

    def restore(self, snapshot):
        self.set_distance(snapshot.distance)


class Estimate:
    def update(self, km):
        self.cost = km * 8


class TripMediator:
    def __init__(self):
        self.estimate = Estimate()
        self.route = Route(self.route_changed)
        self.route_changed()

    def route_changed(self):
        self.estimate.update(self.route.distance)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("actions", nargs="+", help="расстояние в км, save или restore")
    trip = TripMediator()
    saved = None
    for action in parser.parse_args().actions:
        if action == "save":
            saved = trip.route.save()
            print("Сохранено:", saved.distance, "км")
        elif action == "restore":
            if saved is None:
                parser.error("Сначала сохраните маршрут командой save")
            trip.route.restore(saved)
        else:
            try:
                trip.route.set_distance(amount(action))
            except ArgumentTypeError as error:
                parser.error(str(error))
        print("Маршрут:", trip.route.distance, "км | Смета:", money(trip.estimate.cost))
