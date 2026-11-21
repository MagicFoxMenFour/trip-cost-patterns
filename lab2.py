"""Сравнение исходной поездки и копии с другой длиной маршрута."""
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from dataclasses import dataclass, replace
from decimal import Decimal

from money import amount, money


@dataclass(frozen=True)
class Ride(ABC):
    km: Decimal

    def clone(self, km):
        return replace(self, km=km)

    @abstractmethod
    def total(self):
        pass


class TaxiRide(Ride):
    def total(self):
        return 100 + self.km * 18


class CarRide(Ride):
    def total(self):
        return self.km * 8


class Planner(ABC):
    @abstractmethod
    def create_ride(self, km):
        pass

    def compare(self, km, alternative_km):
        original = self.create_ride(km)
        alternative = original.clone(alternative_km)
        return original.total(), alternative.total()


class TaxiPlanner(Planner):
    def create_ride(self, km):
        return TaxiRide(km)


class CarPlanner(Planner):
    def create_ride(self, km):
        return CarRide(km)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("transport", choices=["taxi", "car"])
    parser.add_argument("km", type=amount)
    parser.add_argument("alternative_km", type=amount)
    args = parser.parse_args()
    planners = {"taxi": TaxiPlanner, "car": CarPlanner}
    first, second = planners[args.transport]().compare(args.km, args.alternative_km)
    print("Исходный маршрут:", money(first))
    print("Альтернативный маршрут:", money(second))
