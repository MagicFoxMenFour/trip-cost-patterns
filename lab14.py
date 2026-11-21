"""Запись поездки в SQLite и восстановление объекта через Data Mapper."""
from argparse import ArgumentParser
from contextlib import closing
from dataclasses import dataclass
from decimal import Decimal
import sqlite3

from money import amount, money


@dataclass(frozen=True)
class Trip:
    km: Decimal
    parking: Decimal

    def total(self):
        return self.km * 8 + self.parking


class TripMapper:
    def __init__(self, db):
        self.db = db
        db.execute("CREATE TABLE IF NOT EXISTS trips "
                   "(id INTEGER PRIMARY KEY, km TEXT NOT NULL, parking TEXT NOT NULL)")

    def insert(self, trip):
        with self.db:
            row = self.db.execute("INSERT INTO trips(km, parking) VALUES (?, ?)",
                                  (str(trip.km), str(trip.parking)))
        return row.lastrowid

    def load(self, trip_id):
        row = self.db.execute("SELECT km, parking FROM trips WHERE id = ?",
                              (trip_id,)).fetchone()
        if row is None:
            raise KeyError(trip_id)
        return Trip(Decimal(row[0]), Decimal(row[1]))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=":memory:", help="путь к базе SQLite")
    actions = parser.add_subparsers(dest="action", required=True)
    add = actions.add_parser("add")
    add.add_argument("km", type=amount)
    add.add_argument("--parking", type=amount, default=Decimal(0))
    actions.add_parser("show").add_argument("id", type=int)
    args = parser.parse_args()
    with closing(sqlite3.connect(args.db)) as db:
        mapper = TripMapper(db)
        if args.action == "add":
            trip_id = mapper.insert(Trip(args.km, args.parking))
            print("Сохранена запись", trip_id)
        else:
            trip_id = args.id
        try:
            trip = mapper.load(trip_id)
        except KeyError:
            parser.error("Запись с таким номером не найдена")
        print("Прочитано из SQLite:", trip.km, "км | Стоянка:", money(trip.parking))
        print("Стоимость:", money(trip.total()))
