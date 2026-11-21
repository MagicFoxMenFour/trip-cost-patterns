"""Публикация изменений сметы при согласовании поездки."""
from argparse import ArgumentParser, ArgumentTypeError

from money import amount, money


class Draft:
    name = "Черновик"

    def change(self, trip, distance):
        trip.distance = distance

    def confirm(self, trip):
        trip.state = Confirmed()


class Confirmed:
    name = "Подтверждена"

    def change(self, trip, distance):
        raise ValueError("Изменить подтверждённую поездку нельзя")

    def confirm(self, trip):
        raise ValueError("Поездка уже подтверждена")


class Trip:
    def __init__(self):
        self.distance = 0
        self.state = Draft()
        self.listeners = []

    def subscribe(self, listener):
        self.listeners.append(listener)

    def notify(self):
        for listener in self.listeners:
            listener(self)

    def change(self, distance):
        self.state.change(self, distance)
        self.notify()

    def confirm(self):
        self.state.confirm(self)
        self.notify()


def show_quote(trip):
    print(f"{trip.state.name} | {trip.distance} км | {money(trip.distance * 8)}")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("actions", nargs="+", help="расстояние в км или confirm")
    trip = Trip()
    trip.subscribe(show_quote)
    for action in parser.parse_args().actions:
        try:
            if action == "confirm":
                trip.confirm()
            else:
                trip.change(amount(action))
        except (ValueError, ArgumentTypeError) as error:
            parser.error(str(error))
