import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd

mt5.initialize()
mt5.login(5364362, password="3hdSahJP", server="FxPro-MT5")
utc_from = datetime(2021, 3, 20)
utc_to = datetime(2021, 3, 21)
rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_D1, utc_from, utc_to)
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
2