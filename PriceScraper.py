import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import bs4
import pandas as pd
import os
import io
import sys

# Set up a fake io stream to capture the output of the script
# If this is not done, the script will crash when run as a .exe

buffer = io.StringIO()
sys.stdout = buffer
sys.stderr = buffer


if len(sys.argv) > 1:
    base_path = sys.argv[1]
else:
    # Get the current working directory
    base_path = os.getcwd()
url_path = os.path.join(base_path, 'urls.txt')
output_path = os.path.join(base_path, 'output.csv')

# Define variables

names = []
urls = []
prices = []
units = []

# Read the urls from the file and store them in a list

with open(url_path, 'r') as f:
    for line in f:
        data = line.strip()
        names.append(data.split(';')[0])
        urls.append(data.split(';')[1])
   

# start by defining the options 
options = webdriver.ChromeOptions() 
options.add_argument('headless=new') # it's more scalable to work in headless mode 
# normally, selenium waits for all resources to download 
# we don't need it as the page also populated with the running javascript code. 
options.page_load_strategy = 'none' 
# this returns the path web driver downloaded 
chrome_path = ChromeDriverManager().install() 
chrome_service = Service(chrome_path) 
# pass the defined options and service objects to initialize the web driver 
driver = uc.Chrome(options=options, service=chrome_service) 
driver.implicitly_wait(2)

for url in urls:
    driver.get(url)
    time.sleep(2)
    # Click on the "Accept" button which has the following html: 
    try:
        driver.find_element(By.CSS_SELECTOR, "#CybotCookiebotDialogBodyButtonAccept").click()
        time.sleep(2)
    except:
        pass
    
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    if url.find("baars-bloemhoff.nl") != -1: 
        # Find the div with the class "scale-prices prices" and the itemprop "offers"
        price_div = soup.find('div', {'class': 'scale-prices prices', 'itemprop': 'offers'})

        # Find the span with the class "price" inside the price_div and the span with the class "unit"
        price_span = price_div.find('span', {'class': 'price'})
        unit_span = price_div.find('span', {'class': 'unit'})

        # Extract the text inside the price_span and unit_span, and remove the whitespace
        price = price_span.text.strip()
        unit = unit_span.text.strip()

        # Make sure only numbers and letters are left in price and unit
        price = ''.join([i for i in price if i.isdigit() or i == ','])
        unit = ''.join([i for i in unit if i.isdigit() or i.isalpha()])
    
    elif url.find("vc-wood.com"):
        # Find the div with class actual-price-price
        price_div = soup.find('div', {'class': 'actual-price-price'})

        # Find the span with the class "price" inside the price_div and the span with the class "unit"
        price_span = price_div.find('label', {'class': 'current-price'})
        unit_span = price_div.find('label', {'class': 'unit-current'})

        # Extract the text inside the price_span and unit_span, and remove the whitespace
        price = price_span.text.strip()
        unit = unit_span.text.strip()

        # Make sure only numbers and letters are left in price and unit
        price = ''.join([i for i in price if i.isdigit() or i == ','])

    prices.append(price)
    units.append(unit)


# Convert names, prices, units to a csv file, also add the current date and hour in 2 columns
# Set the date and hour as the first 2 columns

date = time.strftime('%d-%m-%Y')
hour = time.strftime('%H:%M:%S')

# Create a dataframe with the data

df = pd.DataFrame({'Date': date, 'Hour': hour, 'Name': names, 'Price': prices, 'Unit': units})

# Save the dataframe to a csv file

if os.path.exists(output_path):
    df.to_csv(output_path, mode='a', header=False, index=False, sep=';')
else:
    df.to_csv(output_path, index=False, sep=';')

driver.quit()
