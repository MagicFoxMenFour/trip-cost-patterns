"""Дерево расходов на поездку со скидкой на проезд."""
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from dataclasses import dataclass
from decimal import Decimal

from money import amount, money


class Expense(ABC):
    @abstractmethod
    def total(self):
        pass


@dataclass
class Charge(Expense):
    value: Decimal

    def total(self):
        return self.value


@dataclass
class Group(Expense):
    items: tuple

    def total(self):
        return sum(item.total() for item in self.items)


@dataclass
class Discount(Expense):
    expense: Expense
    percent: Decimal

    def total(self):
        return self.expense.total() * (100 - self.percent) / 100


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("km", nargs="+", type=amount)
    parser.add_argument("--parking", type=amount, default=0)
    parser.add_argument("--discount", type=amount, default=0)
    args = parser.parse_args()
    if args.discount > 100:
        parser.error("Скидка должна быть от 0 до 100 процентов")
    travel = Group(tuple(Charge(km * 8) for km in args.km))
    reduced = Discount(travel, args.discount)
    trip = Group((reduced, Charge(args.parking)))
    print("Проезд без скидки:", money(travel.total()))
    print("Проезд со скидкой:", money(reduced.total()))
    print("Со стоянкой:", money(trip.total()))
