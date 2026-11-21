"""Смета маршрута с общими тарифами для повторяющихся зон."""
from argparse import ArgumentParser, ArgumentTypeError
from dataclasses import dataclass
from decimal import Decimal

from money import amount, money


@dataclass(frozen=True)
class ZoneTariff:
    zone: str
    rate: Decimal

    def cost(self, km):
        return self.rate * km


class TariffPool:
    rates = {"city": Decimal(10), "road": Decimal(8)}

    def __init__(self):
        self.tariffs = {}

    def get(self, zone):
        if zone not in self.tariffs:
            self.tariffs[zone] = ZoneTariff(zone, self.rates[zone])
        return self.tariffs[zone]


class RouteFacade:
    def __init__(self):
        self.pool = TariffPool()

    def estimate(self, legs):
        return sum(self.pool.get(zone).cost(km) for zone, km in legs)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("legs", nargs="+", metavar="ZONE:KM")
    legs = []
    for token in parser.parse_args().legs:
        zone, sep, distance = token.partition(":")
        if not sep or zone not in TariffPool.rates:
            parser.error("Укажите участок в формате city:10 или road:25")
        try:
            legs.append((zone, amount(distance)))
        except ArgumentTypeError as error:
            parser.error(str(error))
    facade = RouteFacade()
    print("Стоимость маршрута:", money(facade.estimate(legs)))
    print("Участков:", len(legs))
    print("Объектов тарифа:", len(facade.pool.tariffs))
