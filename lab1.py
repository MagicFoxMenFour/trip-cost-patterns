"""Сборка сметы из участков маршрута и дополнительных расходов."""
from argparse import ArgumentParser
from dataclasses import dataclass
from decimal import Decimal

from money import amount, money


@dataclass(frozen=True)
class Trip:
    legs: tuple
    rate: Decimal
    parking: Decimal

    def total(self):
        return sum(self.legs) * self.rate + self.parking


class TripBuilder:
    def __init__(self, rate):
        self.rate = rate
        self.legs = []
        self.parking = Decimal(0)

    def add_leg(self, km):
        self.legs.append(km)
        return self

    def add_parking(self, fee):
        self.parking += fee
        return self

    def build(self):
        if not self.legs:
            raise ValueError("Добавьте участок маршрута")
        return Trip(tuple(self.legs), self.rate, self.parking)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("km", nargs="+", type=amount, help="длины участков в км")
    parser.add_argument("--rate", type=amount, default=Decimal(8), help="руб./км")
    parser.add_argument("--parking", type=amount, default=Decimal(0), help="стоянка, руб.")
    args = parser.parse_args()
    builder = TripBuilder(args.rate)
    for km in args.km:
        builder.add_leg(km)
    trip = builder.add_parking(args.parking).build()
    print("Стоимость поездки:", money(trip.total()))
