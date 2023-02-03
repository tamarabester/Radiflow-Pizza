import logging
from datetime import datetime
from queue import Empty
from time import sleep
from threading import Thread

logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
logging.getLogger().setLevel(logging.INFO)


class StationBase(Thread):
    station_name = ""
    prep_time_secs = 1

    def __init__(self, worker_id, source, target=None, source_timeout_secs=1, **kwargs):
        super().__init__(target=self.prepare, daemon=True)
        self.worker_id = worker_id
        self.source_queue = source
        self.target_queue = target
        self.source_timeout_secs = source_timeout_secs
        self.keep_serving = True
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_order(self):
        try:
            order = self.source_queue.get(timeout=self.source_timeout_secs)
            return order
        except Empty:
            return None

    def stop(self):
        logging.debug("worker id %s in stop", self.worker_id)
        self.keep_serving = False

    def pass_to_next_station(self, order):
        if self.target_queue:
            self.target_queue.put(order)
        self.source_queue.task_done()

    def log(self, order, station_worker_num, starting=True):
        op = 'entering' if starting else 'exiting'
        logging.info("Order %s %s station %s-%s", order.id, op, self.station_name, station_worker_num)

    def process_order(self, order, *args):
        self.log(order, self.worker_id, starting=True)
        self.work(order, *args)
        self.log(order, self.worker_id, starting=False)

    def work(self, *args, **kwargs):
        sleep(self.prep_time_secs)  # simulate the work

    def prepare(self):
        logging.debug("worker id %s in prepare - starting", self.worker_id)
        while self.keep_serving:
            order = self.get_order()
            if order:
                self.process_order(order)
                self.pass_to_next_station(order)
        logging.debug("worker id %s in prepare - exiting", self.worker_id)


class OrderStart(StationBase):
    report = None

    def process_order(self, order, *args):
        order.start_time = datetime.now()


class OrderFinish(StationBase):
    report = None

    def process_order(self, order, *args):
        order_prep_time = datetime.now() - order.start_time
        self.report[str(order.id)] = order_prep_time.total_seconds()


class DoughChef(StationBase):
    prep_time_secs = 7
    station_name = "Dough-Chef"


class ToppingChef(StationBase):
    prep_time_secs = 4
    station_name = "Topping-Chef"

    def work(self, order):
        # the topping chef can handle up to 2 toppings concurrently
        topping_session_num = len(order.toppings) // 2 + len(order.toppings) % 2
        sleep(topping_session_num * self.prep_time_secs)


class Oven(StationBase):
    prep_time_secs = 10
    station_name = "Oven"


class Waiter(StationBase):
    prep_time_secs = 5
    station_name = "Waiter"
