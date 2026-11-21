"""Восстановление сметы по журналу событий поездки."""
from argparse import ArgumentParser
from dataclasses import dataclass
from decimal import Decimal

from money import amount, money


@dataclass(frozen=True)
class LegAdded:
    km: Decimal

    def apply(self, total):
        return total + self.km * 8


@dataclass(frozen=True)
class ParkingPaid:
    fee: Decimal

    def apply(self, total):
        return total + self.fee


class TripLog:
    def __init__(self):
        self._events = []

    def append(self, event):
        self._events.append(event)

    def balance(self, version):
        if not 0 <= version <= len(self._events):
            raise ValueError("Версия вне журнала")
        total = Decimal(0)
        for event in self._events[:version]:
            total = event.apply(total)
        return total


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("km", nargs="+", type=amount)
    parser.add_argument("--parking", type=amount)
    args = parser.parse_args()
    log = TripLog()
    for km in args.km:
        log.append(LegAdded(km))
    version = len(args.km)
    print(f"После {version} участков:", money(log.balance(version)))
    if args.parking is not None:
        log.append(ParkingPaid(args.parking))
        print("С учётом стоянки:", money(log.balance(version + 1)))
    print("До последнего участка:", money(log.balance(version - 1)))
