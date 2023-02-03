import logging
import os
from csv import reader

from pizzaria.pizzaria.dal import DB
from pizzaria.pizzaria.order import Order
from pizzaria.pizzaria.shift import ShiftManager


def parse_input():
    try:
        with open("orders.csv", "r") as f:
            orders = [Order(toppings=row) for row in reader(f)]
        return orders
    except FileNotFoundError:
        raise Exception("Expects input file 'orders.csv' in current dir")


def main(orders):
    shift = ShiftManager(dough_chef_number=2, topping_chef_number=3, oven_number=1, waiter_number=2)
    shift.take_orders(orders)
    shift.start()
    shift.wait_on_stations()
    report = shift.end()
    print("Shift Report: ", report)
    DB().save_report(report)


if __name__ == '__main__':
    if os.getenv("RETRIEVAL_MODE"):
        logging.debug("In  RETRIEVAL_MODE: printing all past reports")
        DB().get_report(os.getenv("RETRIEVAL_MODE"))
    else:
        orders = parse_input()
        main(orders)

