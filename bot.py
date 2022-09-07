import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv

load_dotenv()

# Set up class
class Martingale(object):
    def __init__(self):
        self.key = os.getenv('API_KEY')
        self.secret = os.getenv('SECRET_KEY')
        self.alpaca_endpoint = os.getenv('APCA_API_BASE_URL')
        self.api = tradeapi.REST(self.key, self.secret, self.alpaca_endpoint)
        self.symbol = 'IVV'
        self.current_order = None
        self.last_price = 1

        # Get start position - we dont have more than one position at once
        try:
            self.position = int(self.api.get_position(self.symbol.qty))
        except:
            self.position = 0

        print(self.position)

    # Submit an order - Cancel current order if one exists
    def submit_order(self, target):
        if self.current_order is not None:
            self.api.cancel_order(self.current_order.id)

        delta = target - self.position
        if delta == 0:
            return
        print(f'Processing the order for {target} shares')
        # Is the delta is greater than 0 and we dont have a position, Buy
        if delta > 0:
            buy_quantity = delta
        if self.position < 0:
            buy_quantity = min(abs(self.position), buy_quantity)
            print(f'Buying {buy_quantity} shares')
            self.current_order = self.api.submit_order(self.symbol, buy_quantity, 'buy', 'limit', 'day', self.last_price)
        # If the delta is lower than 0, Sell the quantity of absolute delta
        elif delta < 0:
            sell_quantity = abs(delta)
        if self.position > 0:
            sell_quantity = min(abs(self.position), sell_quantity)
            print(f'Selling {sell_quantity} shares')
            self.current_order = self.api.submit_order(self.symbol, sell_quantity, 'sell', 'limit', 'day', self.last_price)

# Run app
if __name__ == '__main__':
    trade = Martingale()
    trade.submit_order(3)
