import queue
import threading
import time

from order import Order
from pizzaria.pizzaria.stations import StationBase
from unittest import TestCase


class TestingStation(StationBase):
    station_name = "testing"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed_items = []

    def work(self, order):
        self.processed_items.append(order)


def init_q(items):
    q = queue.Queue()
    for item in items:
        q.put(item)
    return q


class TestPrepare(TestCase):
    orders = [Order(["a"]) for _ in range(5)]

    def get_testing_station(self, source_items=None, with_target=False, **kwargs):
        items = source_items if source_items is not None else self.orders
        s_q = init_q(items)
        t_q = init_q([]) if with_target else None
        return TestingStation(1, s_q, target=t_q, **kwargs)

    def test_get_order_q_full(self):
        station = self.get_testing_station()
        order = station.get_order()
        assert order == self.orders[0]

    def test_get_order_q_empty(self):
        station = self.get_testing_station(source_items=[])
        order = station.get_order()
        assert order is None

    def test_pass_to_next_station_exists(self):
        station = self.get_testing_station(source_items=self.orders[:1], with_target=True)
        assert station.source_queue.unfinished_tasks == 1
        assert station.target_queue.unfinished_tasks == 0
        station.pass_to_next_station(self.orders[:1])
        assert station.source_queue.unfinished_tasks == 0
        assert station.target_queue.unfinished_tasks == 1
        assert station.target_queue.queue[0] == self.orders[:1]

    def test_pass_to_next_station_no_target(self):
        station = self.get_testing_station(source_items=self.orders[:1])
        assert station.source_queue.unfinished_tasks == 1
        station.pass_to_next_station(self.orders[0])
        assert station.source_queue.unfinished_tasks == 0

    def test_prepare(self):
        station = self.get_testing_station(source_timeout_secs=0)
        t = threading.Thread(target=station.prepare)
        t.start()
        time.sleep(1)
        station.stop()
        t.join()
        assert station.processed_items == self.orders
