"""Консольный расчёт поездки и доли пассажира по архитектуре MVC."""
from argparse import ArgumentParser
from dataclasses import dataclass
from decimal import Decimal

from money import amount, money


@dataclass(frozen=True)
class TripModel:
    km: Decimal
    rate: Decimal
    parking: Decimal
    passengers: int

    def __post_init__(self):
        if self.passengers < 1:
            raise ValueError("Укажите хотя бы одного пассажира")

    def total(self):
        return self.km * self.rate + self.parking

    def share(self):
        return self.total() / self.passengers


class ConsoleView:
    def show(self, trip):
        print(f"Маршрут: {trip.km} км | Пассажиров: {trip.passengers}")
        print("За поездку:", money(trip.total()))
        print("На пассажира:", money(trip.share()))


class TripController:
    def __init__(self, view):
        self.view = view

    def calculate(self, km, rate, parking, passengers):
        model = TripModel(km, rate, parking, passengers)
        self.view.show(model)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("km", type=amount)
    parser.add_argument("--rate", type=amount, default=Decimal(8))
    parser.add_argument("--parking", type=amount, default=Decimal(0))
    parser.add_argument("--passengers", type=int, default=1)
    args = parser.parse_args()
    try:
        TripController(ConsoleView()).calculate(args.km, args.rate, args.parking, args.passengers)
    except ValueError as error:
        parser.error(str(error))
