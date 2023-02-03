import datetime
import logging
import queue

from pizzaria.pizzaria.stations import DoughChef, OrderStart, OrderFinish, ToppingChef, Oven, Waiter


class ShiftManager:
    def __init__(self, dough_chef_number, topping_chef_number, oven_number, waiter_number):
        self.start_time = None
        self.end_time = None
        self.orders_report = {}
        self.queues = [queue.Queue() for _ in range(6)]
        new_orders, dough_queue, topping_queue, oven_queue, waiter_queue, finished_orders = self.queues

        start_station = OrderStart(0, new_orders, dough_queue, report=self.orders_report)
        dough_chefs = [DoughChef(i, dough_queue, topping_queue) for i in range(dough_chef_number)]
        topping_chefs = [ToppingChef(i, topping_queue, oven_queue) for i in range(topping_chef_number)]
        ovens = [Oven(i, oven_queue, waiter_queue) for i in range(oven_number)]
        waiters = [Waiter(i, waiter_queue, finished_orders) for i in range(waiter_number)]
        end_station = OrderFinish(0, finished_orders, report=self.orders_report)
        self.stations = dough_chefs + topping_chefs + ovens + waiters + [start_station, end_station]

    def start(self):
        self.start_time = datetime.datetime.now()
        for worker in self.stations:
            worker.start()

    def wait_on_stations(self):
        for i, station_queue in enumerate(self.queues):
            station_queue.join()
            logging.debug("joined q #%s", i)

    def get_end_of_shift_report(self):
        overall_duration = self.end_time - self.start_time
        return {
            "overall_duration_secs": overall_duration.total_seconds(),
            "duration_per_order_secs": self.orders_report
            }

    def end(self):
        for worker in self.stations:
            worker.stop()
            worker.join()
        self.end_time = datetime.datetime.now()
        return self.get_end_of_shift_report()

    def take_orders(self, orders):
        new_orders_queue = self.queues[0]
        for order in orders:
            new_orders_queue.put(order)
