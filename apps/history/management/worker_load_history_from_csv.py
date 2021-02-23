import os
import csv
import datetime

from django.conf import settings

from apps.history.models import Currency, TimeMarker, Bar


def main():
    data_path = os.path.join(settings.BASE_DIR, "data", "currency")
    for csv_file in os.listdir(data_path):
        name = str(csv_file.split("_")[0]).lower()
        first = name[:3]
        second = name[3:]
        currency = Currency.objects.get(first=first, second=second)
        file = csv.DictReader(f=open(os.path.join(data_path, csv_file)), delimiter="\t")
        for line in file:
            close = float(line["<CLOSE>"])
            high = float(line["<HIGH>"])
            low = float(line["<LOW>"])
            t = datetime.datetime.strptime(line["<DATE>"], "%Y.%m.%d").date()
            if t.weekday() in {6, 5}:
                continue
            time_marker = TimeMarker.objects.get_or_create(time_marker=t)[0]
            print(currency, time_marker)
            Bar.objects.update_or_create(currency=currency, time_marker=time_marker, defaults={"close": close, "high": high, "low": low})
