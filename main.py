from santiebeati import scrape_all_name_pages
import json

if __name__ == '__main__':
    results = scrape_all_name_pages(letter='A')

    print(json.dumps(results, indent=4))
