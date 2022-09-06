import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv

load_dotenv()

class Martingale(object):
  def __init__(self):
    self.key = os.getenv('API_KEY')
    self.secret = os.getenv('SECRET_KEY')
    self.alpaca_endpoint = os.getenv('APCA_API_BASE_URL')
    self.api = tradeapi.REST(self.api_key, self.secret_key, self.alpaca_endpoint)
    self.symbol = 'IVV'
    self.current_order = None
    self.last_price = 1
