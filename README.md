# Installation

To install the script, run install.bat

To uninstall the script, run uninstall.bat

Feel free to remove the 'placeholder' file in Results, this is just a placeholder for github purposes

# Configuration

In the Configs folder

## Full Scrapes

Place urls to a page you want to scrape multiple items from in full_urls.txt

The format should be NAME; URL

For example:
```
Google Example; https://www.google.com
```

Current supported sites:
- https://www.vc-wood.com

## Individual Scrapes

Place urls to a page you want to scrape a single item from in individual_urls.txt

The format should be NAME; URL

For example:
```
Google Example; https://www.google.com
```

Current supported sites:
- https://www.vc-wood.com
- https://www.baars-bloemhoff.nl

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