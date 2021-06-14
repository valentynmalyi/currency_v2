from datetime import date

from environ import Env

env = Env()

start_date_year = env.int("START_DATE_YEAR")
start_date_month = env.int("START_DATE_MONTH")
start_date_day = env.int("START_DATE_DAY")

START_DATE = date(year=start_date_year, month=start_date_month, day=start_date_day)
