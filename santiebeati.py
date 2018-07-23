"""
    Client that can parse results from the website
    santiebeati.it
"""
import os
import os.path
import re
from collections import defaultdict, namedtuple
from string import ascii_uppercase
import json

from helpers import cached_in_db
from helpers import cache_in_calendar
from requests_html import HTMLSession

SaintDay = namedtuple('SaintDay', ['month', 'day'])
SaintResult = namedtuple('SaintResult',
                         ['full_name', 'first_name', 'role', 'dates'])

SPLIT_SAINTS_REGEX = re.compile(r"\d+ >")
SPLIT_LINES_REGEX = re.compile(r"\n+ ")
ITALIAN_MONTHS = [
    "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
    "agosto", "settembre", "ottobre", "novembre", "dicembre"
]
DATE_REGEX = re.compile(r"\d{1,2} (?:" + "|".join(ITALIAN_MONTHS) + ")")
SESSION = HTMLSession()


def create_url(letter, page):
    page_label = f'more{page}.html' if page > 1 else ''
    return f"http://www.santiebeati.it/{letter}/{page_label}"


def create_calendar_url(month, day):
    return "http://www.santiebeati.it/{:02d}/{:02d}".format(month, day)


def parse_saint_days(days):
    results = []
    for day in days:
        d, m = day.split()
        results.append(SaintDay(1 + ITALIAN_MONTHS.index(m), int(d))._asdict())
    return results


def parse_saint(txt):
    # days are the last elements I care about
    days = []
    # remove empty lines
    rows = [s for s in txt.splitlines() if s]
    non_day_rows = []
    for x in rows:
        xs = DATE_REGEX.findall(x)
        if xs:
            days += xs
        else:
            # what follows days does not matter
            if not days:
                non_day_rows.append(x)

    try:
        return SaintResult(" ".join(non_day_rows), non_day_rows[1],
                           non_day_rows[2] if len(non_day_rows) > 2 else None,
                           parse_saint_days(days))
    except IndexError as error:
        print(error)
        print(non_day_rows)
        return None


def scrape_page(url):
    response = SESSION.get(url)
    if response.status_code != 200:
        return None
    saints_table = response.html.find('table', first=True).text
    xs = SPLIT_SAINTS_REGEX.split(saints_table)
    return [parse_saint(x)._asdict() for x in xs[1:] if parse_saint(x)]


@cached_in_db
def scrape_all_name_pages(letter):
    results = []
    page = 1

    while True:
        url = create_url(letter, page)
        saints = scrape_page(url)
        if not saints:
            break
        page += 1
        results += saints
        print(f"page {page} done")

    return results


@cache_in_calendar
def scrape_calendar_page(month, day):
    url = create_calendar_url(month, day)
    return scrape_page(url)


def scrape_all_names():
    results = []
    for letter in ascii_uppercase:
        xs = scrape_all_name_pages(letter=letter)
        results += xs
        print(f"letter {letter} DONE")
    return results


def scrape_all_calendar():
    for month, day in [(month, day) for month in range(1, 13)
                       for day in range(1, 32)]:
        scrape_calendar_page(month=month, day=day)
        print(f"{month}/{day} DONE")


def create_calendar(saint_results_dicts):
    """
    takes a list of SaintResult dictionaries and
    organizes them as a dictionary where the root
    key is mont-day
    """
    saints_calendar = defaultdict(list)
    for saint in saint_results_dicts:
        for saint_date in saint.get('dates', []):
            xs = [str(saint_date.get('month')), str(saint_date.get('day'))]
            key = '-'.join(xs)
            saints_calendar[key].append(saint)

    with open('db/calendar.json', 'w') as calendar_file:
        calendar_file.write(json.dumps(saints_calendar, indent=4))
