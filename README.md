# Installation

To install the script, run install.bat

To uninstall the script, run uninstall.bat

# Configuration

In the Configs folder

## Full Scrapes

Place urls to a page you want to scrape multiple items from in full_urls.txt

The format should be NAME; URL

For example:
```
Google Example; https://www.google.com
```

## Individual Scrapes

Place urls to a page you want to scrape a single item from in individual_urls.txt

The format should be NAME; URL

For example:
```
Google Example; https://www.google.com
```

# Result overview

In the results folder

## Full Scrapes

Contains the scrapes from full_urls.txt

- Date/Time: When the scrape was performed
- Name: User defined name
- Product: Product name on the website
- Price: Price listed on the website, currency depends on the website but usually euros
- Unit: Unit for the price, e.g. 5 per square meter

## Individual Scrapes

Contains the scrapes from urls.txt

- Date/Time: When the scrape was performed
- Name: User defined name
- Price: Price listed on the website, currency depends on the website but usually euros
- Unit: Unit for the price, e.g. 5 per square meter