from santiebeati import scrape_all_names, create_calendar
import json

if __name__ == '__main__':
    all = scrape_all_names()
    create_calendar(all)
