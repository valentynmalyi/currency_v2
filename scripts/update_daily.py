import os
import csv
import datetime

# noinspection PyUnresolvedReferences
import scripts.django_init

from apps.history.models import Currency, TimeMarker, Bar

HOME = os.path.join(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(HOME, "data", "currency")


def main():
    for csv_file in os.listdir(DATA_PATH):
        name = str(csv_file.split("_")[0]).lower()
        first = name[:3]
        second = name[3:]
        currency = Currency.objects.get(first=first, second=second)
        file = csv.DictReader(f=open(os.path.join(DATA_PATH, csv_file)), delimiter="\t")
        for line in file:
            close = float(line["<CLOSE>"])
            high = float(line["<HIGH>"])
            low = float(line["<LOW>"])
            t = datetime.datetime.strptime(line["<DATE>"], "%Y.%m.%d").date()
            time_marker = TimeMarker.objects.get_or_create(time_marker=t)[0]
            print(currency, time_marker)
            Bar.objects.update_or_create(currency=currency, time_marker=time_marker, defaults={"close": close, "high": high, "low": low})


if __name__ == '__main__':
    main()
