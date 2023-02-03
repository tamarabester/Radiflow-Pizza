import uuid

class Order:
    def __init__(self, toppings):
        self.toppings = toppings
        self.id = uuid.uuid4()
        self.start_time = None
