"""Добавление участков маршрута с возможностью отмены."""
from argparse import ArgumentParser, ArgumentTypeError
from decimal import Decimal

from money import amount, money


class Route:
    def __init__(self):
        self.legs = []

    def __iter__(self):
        return iter(self.legs)

    def total(self):
        return sum(self) * Decimal(8)


class AddLeg:
    def __init__(self, route, distance):
        self.route = route
        self.distance = distance

    def execute(self):
        self.route.legs.append(self.distance)

    def undo(self):
        self.route.legs.pop()


class Editor:
    def __init__(self):
        self.history = []

    def run(self, command):
        command.execute()
        self.history.append(command)

    def undo(self):
        if not self.history:
            raise ValueError("Нет команды для отмены")
        self.history.pop().undo()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("actions", nargs="+", help="длина участка в км или undo")
    route = Route()
    editor = Editor()
    for action in parser.parse_args().actions:
        try:
            if action == "undo":
                editor.undo()
            else:
                editor.run(AddLeg(route, amount(action)))
        except (ValueError, ArgumentTypeError) as error:
            parser.error(str(error))
    print("Участки, км:", ", ".join(map(str, route)) or "маршрут пуст")
    print("Стоимость:", money(route.total()))
