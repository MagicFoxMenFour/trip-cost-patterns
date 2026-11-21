"""Очередь заявок на расчёт поездки с отдельным потоком-потребителем."""
from argparse import ArgumentParser
from queue import Queue
from threading import Thread

from money import amount, money


class QuoteConsumer(Thread):
    def __init__(self, requests):
        super().__init__()
        self.requests = requests
        self.results = []

    def run(self):
        while True:
            job = self.requests.get()
            if job is None:
                return
            number, km = job
            self.results.append((number, km, km * 8))


class QuoteProducer:
    def __init__(self, requests):
        self.requests = requests

    def submit_all(self, distances):
        for number, km in enumerate(distances, 1):
            self.requests.put((number, km))
        self.requests.put(None)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("km", nargs="+", type=amount)
    args = parser.parse_args()
    requests = Queue(maxsize=2)
    consumer = QuoteConsumer(requests)
    consumer.start()
    QuoteProducer(requests).submit_all(args.km)
    consumer.join()
    for number, km, total in consumer.results:
        print(f"Заявка {number}: {km} км | {money(total)}")
    print("Обработано заявок:", len(consumer.results))
