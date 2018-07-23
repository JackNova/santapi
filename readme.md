# SANTAPI

This is just a scraper for the website <http://www.santiebeati.it/>.

In the db/ directory there is a json dump of the scraped results (Alphabetical)

In the calendar/ directory there is a json dump of the scraped results (Calendar)

If you want to run the scraper by yourself

edit the main.py file to run the command you want then

```bash
rm -rf db/*.json
pip install -r requirements.txt
python main.py
```

or

```bash
rm -rf calendar/
pip install -r requirements.txt
python main.py
```



## TODO

- [] calendar in sorted order
- [] create rest api
