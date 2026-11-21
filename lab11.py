"""Расчёт стоимости по выбранному тарифу с общей последовательностью шагов."""
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from decimal import Decimal

from money import amount, money


class Fare(ABC):
    def total(self, km, parking):
        return self.boarding() + self.travel(km) + parking

    def boarding(self):
        return Decimal(0)

    @abstractmethod
    def travel(self, km):
        pass


class CarFare(Fare):
    def travel(self, km):
        return km * 8


class TaxiFare(Fare):
    def boarding(self):
        return Decimal(100)

    def travel(self, km):
        return km * 18


class Calculator:
    def __init__(self, fare):
        self.fare = fare

    def estimate(self, km, parking):
        return self.fare.total(km, parking)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("transport", choices=["car", "taxi"])
    parser.add_argument("km", type=amount)
    parser.add_argument("--parking", type=amount, default=Decimal(0))
    args = parser.parse_args()
    fare = {"car": CarFare, "taxi": TaxiFare}[args.transport]()
    calculator = Calculator(fare)
    print("Подача:", money(fare.boarding()))
    print("Проезд:", money(fare.travel(args.km)))
    print("Стоянка:", money(args.parking))
    print("Итого:", money(calculator.estimate(args.km, args.parking)))
