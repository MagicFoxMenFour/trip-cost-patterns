"""Согласование стоимости поездки по лимитам полномочий."""
from argparse import ArgumentParser
from money import amount, money


class ApprovalStep:
    def __init__(self, title, limit, successor=None):
        self.title = title
        self.limit = limit
        self.successor = successor

    def review(self, cost, trace):
        trace.append(self.title)
        if cost <= self.limit:
            return f"Согласовано: {self.title}"
        if self.successor is not None:
            return self.successor.review(cost, trace)
        return "Отклонено: превышен максимальный лимит"


def approval_chain():
    director = ApprovalStep("директор", 5000)
    manager = ApprovalStep("руководитель", 2000, director)
    return ApprovalStep("координатор", 500, manager)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("km", type=amount)
    parser.add_argument("--parking", type=amount, default=0)
    args = parser.parse_args()
    cost = args.km * 8 + args.parking
    trace = []
    decision = approval_chain().review(cost, trace)
    print("Стоимость:", money(cost))
    print("Порядок проверки:", " -> ".join(trace))
    print(decision)
