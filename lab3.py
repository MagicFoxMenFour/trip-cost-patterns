"""Сравнение расходов на весь маршрут и на одного пассажира."""
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from decimal import Decimal

from money import amount, money


class Tariff(ABC):
    @abstractmethod
    def price(self, km):
        pass


class LocalTariff(Tariff):
    def price(self, km):
        return km * 8


class MileMeter:
    def quote_miles(self, miles):
        return miles * 16


class MileAdapter(Tariff):
    def __init__(self, meter):
        self.meter = meter

    def price(self, km):
        return self.meter.quote_miles(km / Decimal("1.609344"))


class Estimate:
    def __init__(self, tariff):
        self.tariff = tariff

    def cost(self, km):
        return self.tariff.price(km)


class SharedEstimate(Estimate):
    def __init__(self, tariff, passengers):
        super().__init__(tariff)
        if passengers < 1:
            raise ValueError("Число пассажиров должно быть положительным")
        self.passengers = passengers

    def cost(self, km):
        return super().cost(km) / self.passengers


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("km", type=amount)
    parser.add_argument("--tariff", choices=["local", "mile"], default="local")
    parser.add_argument("--passengers", type=int, default=1)
    args = parser.parse_args()
    if args.passengers < 1:
        parser.error("Число пассажиров должно быть положительным")
    tariff = LocalTariff() if args.tariff == "local" else MileAdapter(MileMeter())
    print("За маршрут:", money(Estimate(tariff).cost(args.km)))
    print("На пассажира:", money(SharedEstimate(tariff, args.passengers).cost(args.km)))
