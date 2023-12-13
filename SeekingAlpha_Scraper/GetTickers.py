import csv
from Scraper import get_output

def get_tickers():
    with open("SeekingAlpha_Scraper/listing_status.csv") as file:
        reader = csv.reader(file, delimiter=",")
        symbols = []
        already_fetched = ['A']
        for row in reader:
            if row[0] not in already_fetched:
                symbols.append(row[0])

    return symbols


symbols = get_tickers()
for s in symbols:
    try:
        # webscrapes for the company with symbol s
        get_output(s)
    except Exception as e:
        continue