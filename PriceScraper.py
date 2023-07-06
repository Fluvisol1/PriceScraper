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
full_url_path = os.path.join(base_path, 'full_urls.txt')
output_path = os.path.join(base_path, 'individual_scrapes.csv')
full_output_path = os.path.join(base_path, 'full_scrapes.csv')

# Define variables

names = []
full_names = []
urls = []
full_urls = []
prices = []
full_prices = []
units = []
full_units = []
result_names = []
products = []

# Read the urls from the file and store them in a list

with open(url_path, 'r') as f:
    for line in f:
        data = line.strip()
        names.append(data.split(';')[0])
        urls.append(data.split(';')[1])

# Read the full urls from the file and store them in a list

with open(full_url_path, 'r') as f:
    for line in f:
        data = line.strip()
        full_names.append(data.split(';')[0])
        full_urls.append(data.split(';')[1])

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

for url in full_urls:
    driver.get(url) 
    time.sleep(2)
    # Click on the "Accept" button which has the following html: 
    try:
        driver.find_element(By.CSS_SELECTOR, "#CybotCookiebotDialogBodyButtonAccept").click()
        time.sleep(2)
    except:
        pass

    try:
        # On the page, there is a dropdown menu with class "sort-number". This needs to be clicked and the option where the value contains the string "PageSize_96" needs to be clicked. This will show 96 products per page instead of 24 products per page.
        driver.find_element(By.CSS_SELECTOR, ".sort-number").click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "[value*='PageSize_96']").click()
        time.sleep(10)
    except:
        pass
    
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    # Find all the divs with class "product-item" and store them in a list
    product_divs = soup.find_all('div', {'class': 'product-item'})

    # Get the name corresponding to the url
    name = full_names[full_urls.index(url)]

    for product_div in product_divs:
        # find the label with class product-description-label
        product_description_label = product_div.find('label', {'class': 'product-description-label'})

        # find the div with class actual-price-price
        actual_price_price = product_div.find('div', {'class': 'actual-price-price'})

        # find the label with class current-price
        current_price = actual_price_price.find('label', {'class': 'current-price'})

        # find the label with class unit-current
        unit_current = actual_price_price.find('label', {'class': 'unit-current'})

        # Extract the text inside the product_description_label, current_price and unit_current, and remove the whitespace
        product = product_description_label.text.strip()
        price = current_price.text.strip()
        unit = unit_current.text.strip()
        price = ''.join([i for i in price if i.isdigit() or i == ','])

        result_names.append(name)
        products.append(product)
        full_prices.append(price)
        full_units.append(unit)

# Convert names, prices, units to a csv file, also add the current date and hour in 2 columns
# Set the date and hour as the first 2 columns

date = time.strftime('%d-%m-%Y')
hour = time.strftime('%H:%M:%S')

# Create a dataframe with the data

df = pd.DataFrame({'Date': date, 'Hour': hour, 'Name': names, 'Price': prices, 'Unit': units})
df_full = pd.DataFrame({'Date': date, 'Hour': hour, 'Name': result_names, 'Product': products, 'Price': full_prices, 'Unit': full_units})

# Save the dataframe to a csv file

if os.path.exists(output_path):
    df.to_csv(output_path, mode='a', header=False, index=False, sep=';')
else:
    df.to_csv(output_path, index=False, sep=';')

if os.path.exists(full_output_path):
    df_full.to_csv(full_output_path, mode='a', header=False, index=False, sep=';')
else:
    df_full.to_csv(full_output_path, index=False, sep=';')

driver.quit()
