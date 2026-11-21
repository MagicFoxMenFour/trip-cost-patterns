"""Кэширующий заместитель сервиса расчёта цены такси."""
from abc import ABC, abstractmethod
from argparse import ArgumentParser

from money import amount, money


class QuoteService(ABC):
    @abstractmethod
    def quote(self, km):
        pass


class TaxiService(QuoteService):
    def __init__(self):
        self.calls = 0

    def quote(self, km):
        self.calls += 1
        return 100 + km * 18


class CachedService(QuoteService):
    def __init__(self, service):
        self.service = service
        self.cache = {}

    def quote(self, km):
        if km not in self.cache:
            self.cache[km] = self.service.quote(km)
        return self.cache[km]


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("km", nargs="+", type=amount)
    args = parser.parse_args()
    taxi = TaxiService()
    service = CachedService(taxi)
    for distance in args.km:
        print(f"{distance} км:", money(service.quote(distance)))
    print("Запросов:", len(args.km), "| Вычислений:", taxi.calls)
