from datetime import datetime
import json
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import sys
from dotenv import load_dotenv 

load_dotenv()

from_currency = "GBP"
to_currency = "USD"

def build_api_url(from_currency):
    """ The aim of this function is to build the api url
        The function uses the os module to read the api key from the .env file
        If there is no api key it uses the open, no key end point from ExchangeRate-API's free tier
        The function returns the complete url
    """
    api_key = os.getenv('EXCHANGE_API_KEY')  # Direct call
    # Ensure base URL is correct for keyed vs. open endpoint
    base_api_url = "https://open.er-api.com/v6/latest/" if not api_key else "https://api.exchangerate-api.com/v4/latest/"
    print(f"Building API URL with base: {base_api_url}, currency: {from_currency}, key: {'Yes' if api_key else 'No'}")  # Debug
    url = f"{base_api_url}{from_currency}"
    if api_key:
        url += f"?access_key={api_key}"
    print(f"Final API URL: {url}")  
    return url

API_URL = build_api_url(from_currency)

def fetch_exchange_rate():
    """This function fetches the exchange rate from the API
       The function uses the requests library to make a GET request to the API URL"""
 
#The getenv garbs the key from the .env file

    api_key = os.getenv('EXCHANGE_API_KEY')
    #Prints the message using an f-string prinfing the message if the key is found
    #The try block is used to catch any errors that may occur during the request
    #The requests fetches the data from the api url with a timeout of 10 seconds
    #The data is converted from json format to a python dictionary with the .json() method
 
    try:
        print(f"Fetching rate from API(key used: {'Yes ' if api_key else 'No'})...")
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()


    #Uses an if statement to check if the rates key is in the data and if yes, pulls the rate
    #If it fails, it raises a value error at the end of the function.
        if "rates" in data and to_currency in data["rates"]:
            rate = data["rates"][to_currency]
            timestamp_str =  data.get("data", data.get("timestamp, datetime.now().isoformat()))"))

            #The datetime is a built in method  but we convert the timestamp string to a datetime object that can be read in python
            #We try this and if it fails we use the current time which is the time now
            #The f string prints the current currency the rate and the to currency with the date
            try: 
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            except:
                timestamp = datetime.now()
                print(f"Exchange rate fetched: 1 {from_currency} = {rate} {to_currency} (as of {timestamp})")
                return rate, timestamp.isoformat()
        else:
            raise ValueError("Target currency not supported ")
        
    except requests.exceptions.RequestException as e:
            print(f"Connection error fetching exchange rate: {e}")
            print("Using mock rate: 1GBP = 1.29 USD")
            return 1.29, datetime.now().isoformat()

    except (KeyError, ValueError) as e:
                print(f"API error: {e}")
                return 1.29, datetime.now().isoformat()
         

def scrape_products():
    """Scrape at least 10 products with error handling."""
    products = []
    url = "https://books.toscrape.com/"
    page = 1
    max_pages = 5
    
    while len(products) < 10 and page <= max_pages:
        try:
            print(f"Scraping page {page} at {url}...")
            response = requests.get(url, timeout=10)
            print(f"Status code: {response.status_code}")
            response.raise_for_status()
            with open(f"page_{page}_debug.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"Saved HTML to page_{page}_debug.html")
        except requests.exceptions.RequestException as e:
            print(f"Connection error scraping page {page}: {e}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        product_items = soup.find_all('article', class_='product_pod')[:20]
        if not product_items:
            print("Primary selector 'article.product_pod' found 0 items. Trying fallback...")
            product_items = soup.find_all('div', class_='product_pod')[:20]
        if not product_items:
            print("Fallback selector 'div.product_pod' found 0 items. Dumping first 500 chars of HTML...")
            print(soup.prettify()[:500])
            print("No products found on this page.")
            break
        
        print(f"Found {len(product_items)} product items")
        
        for item in product_items:
            if len(products) >= 10:
                break
            # Title extraction
            title_tag = item.find('h3')
            if not title_tag:
                print("Skipping item: No <h3> tag found")
                continue
            a_tag = title_tag.find('a')
            if not a_tag:
                print("Skipping item: No <a> tag in <h3>")
                continue
            title = a_tag.get('title', '').strip() or a_tag.text.strip()  # Fallback to text if no title attr
            if not title:
                print("Skipping item: No title found")
                continue
            
            # Price extraction
            price_tag = item.find('p', class_='price_color')
            if not price_tag:
                print("Skipping item: No <p class='price_color'> found")
                continue
            price_str = price_tag.text.strip()
            import re
            match = re.search(r'£(\d+\.\d{2})', price_str)
            if match:
                price = float(match.group(1))
            else:
                print(f"Skipping item: Invalid price format ({price_str})")
                continue
            
            products.append({
                'name': title,  # Consistent with display_table
                'original_price': price,
                'original_currency': from_currency
            })
            print(f"Added product: {title}")
        
        next_button = soup.find('li', class_='next')
        if not next_button or not next_button.find('a'):
            print("No more pages to scrape.")
            break
        next_url = next_button.find('a')['href']
        url = "https://books.toscrape.com/" + next_url.replace('../', '')
        page += 1
    
    if len(products) < 10:
        print(f"Warning: Only scraped {len(products)} products.")
    
    return products
def convert_prices(products, rate, timestamp):
    """Convert prices and add timestamp."""
    for prod in products:
        prod['converted_price'] = round(prod['original_price'] * rate, 2)
        prod['conversion_rate'] = rate
        prod['timestamp'] = timestamp
        prod['target_currency'] = to_currency
    return products



def save_to_csv(products, filename='products_prices.csv'):
     """ This function saves the product details to a CSV file
         The function takes in two parameters: products and filename
         The products is a list of dictionaries containing product details with the title, original price, original currency, converted price, conversion rate, timestamp and target currency
         The filename is the name of the CSV file to save the data to, defaulting to 'products_prices.csv'
         The function uses the pandas library to create a DataFrame from the products list and saves it to a CSV file using the to_csv method
         The index parameter is set to False to avoid writing row numbers to the file
         A message is printed indicating where the data has been saved
     """
     df  = pd.DataFrame(products)
     df.to_csv('products.csv', index=False)
     print(f"Data saved to: {filename}")



def save_to_json(products, filename='products_prices.json'):
     """ This function svaes the data to json file
         The open function is used to open the file in write mode
         The json.dump function is used to write the data to the file
         The indent parameter is used to format the json file with an indentation of 4 spaces otherwise the json would be messy
         The f  is the file handle to write to.
         The default parameter is used to convert any non-serializable objects to strings i.e timestamps to avoid any errors.
         The data is saved in json and a message is printed indicating where the data has been saved to
       """
     with open('products.json', 'w') as f:
          json.dump(products, f, indent=4, default= str)
     print(f"Data saved to : {filename}")
          
                 
def display_table(products):
    """ This function displays the product details in a tabular format
            The function takes in one parameter: products
            The products is a list of dictionaries containing product details with the title, original price, original currency, converted price, conversion rate, timestamp and target currency
            The function uses the pandas library to create a DataFrame from the products list
            The display_df variable is used to select specific columns to display in the table for better visualization
            The to_string method is used to convert the DataFrame to a string format for printing, with the index parameter set to False to avoid displaying row numbers
            A message is printed indicating that the products with converted prices are being displayed"""     
        
    df = pd.DataFrame(products)
    display_df = df[['name', 'original_price', 'converted_price', 'original_currency', 'conversion_rate', 'timestamp']]
    print("  Products with Converted Prices: " )
    print(display_df.to_string(index=False))

def plot_prices(original_prices, converted_prices, names):
     """ This function plots the chart 
         It takes in the original price, converted prices and name as the parameter
         The range function creates a sequence of intergers for 10 books
         The fig and ax intializes a matplotlib figure with a size 10inches wide and 6 inches tall
         The first ax.bar plots bars from original prices at positions shifted by width/2 each bars width=0.35 and color blue
         Like wise for second ax.bar but for converted prices but with orange color
         The ax.xlabel, ax.ylabel and ax.set_title are fro setting the names on the axis
         The ax.set.xtick(x places ticks at interger positions)
         The ax.set.xticklabels(names, rotation=45, ha='right') maps book titles to ticks, rotates labels 45degrees for readability and aligns right
         The ax.legend shows the "GBP Price"blue and "USD Price"orange" 
         The ax.tight_layout ensures a clean plot 
         The plot is saved and shown"""
     x = range(len(names))
     width = 0.35 
     fig, ax = plt.subplots(figsize=(10,6))  
     ax.bar([i - width/2 for i in x], original_prices, width, label=f'{from_currency} Price', color='blue')
     ax.bar([i + width/2 for i in x], converted_prices, width, label=f'{to_currency} Price', color='orange')
     ax.set_xlabel('Products')
     ax.set_ylabel('Price')
     ax.set_title('Original vs Converted Prices')
     ax.set_xticks(x)
     ax.set_xticklabels(names, rotation=45, ha='right')
     ax.legend()
     ax.tight_layout()
     plt.savefig('price_comparison.png')
     plt.show()
     print("Price comparison chart saved as 'price_comparison.png'")

if __name__ == "__main__":
     """ This is the main function and starts off with a print message
       And then calls the fetch_exchange_rate to use the website 
        The scrape_product_price is called to scrape the website and there is a condition if it fails
        The convert_price() is called which transforms the GBP PRICES to target currency
        If they are found the save_to_csv function is called and the save_to_json function
        The next step uses list comprehension to extract up to 10 books names and prices
        The plot_price fnction is called which prints the plot with original prices, converted prices and names
           and then DONE!!!!   """
     

     print("Starting Price Scraper and Currency Converter...")

     rate, timestamp = fetch_exchange_rate()
     products = scrape_products()

     if not products:
          print("No products to scrap. Exiting.")
          sys.exit(1)

     products = convert_prices(products, rate, timestamp)
     display_table(products)

     save_to_csv(products)
     save_to_json(products)

     names = [p['name'] for p in products[:10]] 
     orig_prices = [p['original_price'] for p in products[:10]] 
     conv_prices = [p['converted_price'] for p in products[:10]]   

     plot_prices(orig_prices, conv_prices, names)


     print(" Done! Check the files and plot. (Rates by exchangerate_api.com)")

