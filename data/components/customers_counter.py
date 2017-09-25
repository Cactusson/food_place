class CustomersCounter:
    def __init__(self, mode, game_events):
        self.game_events = game_events
        self.customers_served = 0
        self.customers_lost = 0
        if mode == 'INFINITE':
            self.customers_to_lose = 3
        else:
            self.customers_to_lose = None

    def customer_is_served(self):
        self.customers_served += 1

    def customer_is_lost(self):
        self.customers_lost += 1
        if self.customers_to_lose is not None:
            if self.customers_lost >= self.customers_to_lose:
                self.game_events.append(('LEVEL FINISHED',))
