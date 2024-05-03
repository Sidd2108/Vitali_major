import requests
from bs4 import BeautifulSoup

def scrape_amzn_products(category):
    url = f"https://www.amazon.in/s?k=health+supplements&rh=n%3A1374492031%2Cn%{category}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products_prices = {}

    # Find the span containing the result count
    bs  = soup.find("span", class_ = "a-price-whole")
    if bs == None:
        result_span = soup.find('span', class_='a-size-medium-plus a-color-base a-text-bold', text=' results')
    if result_span:
        parent_div = result_span.find_parent('div', class_='a-section a-spacing-small')
        if parent_div:
            product_divs = parent_div.find_all('div', class_='sg-col-inner')
            for div in product_divs:
                data_asin = div.get('data-asin')
                if data_asin:
                    name_div = div.find('div', class_="s-widget-container s-spacing-small s-widget-container-height-small celwidget slot=MAIN template="
                                        "SEARCH_RESULTS widgetId=search-results_5")
                    product_name = None
                    if name_div : name_div = name_div.find(class_="a-declarative")
                    if name_div : name_div = name_div.find(class_="puis-card-container s-card-container s-overflow-hidden aok-relative puis-expand-height" 
                        "puis-include-content-margin puis puis-v3e4zzjeea908l2c0qtoqr7pr8a s-latency-cf-section puis-card-border")
                    if name_div : 
                        name_div = name_div.find(class_="a-section a-spacing-base",class_="a-section a-spacing-small puis-padding-left-small puis-padding-right-small")
                    if name_div : 
                        name_div = name_div.find( class_="a-section a-spacing-none ")
                        if name_div :
                            name_div = name_div.find(class_="a-size-base-plus ")  
                    if name_div : 
                        name_div = name_div.find( class_="a-section a-spacing-none a-spacing-top-small ")
                        if name_div :
                            name_div = name_div.find(class_="a-size-base-plus a-color-base a-text-normal")  
                    if name_div : 
                        name_div = name_div.find( class_="a-section a-spacing-none a-spacing-top-small s-title-instructions-style")
                        if name_div :
                            name_div = name_div.find(class_="a-size-base-plus a-color-base")  
                    
                    name_div = div.find('div', class_='a-section a-spacing-none a-spacing-top-small s-title-instructions-style')
                    if name_div:
                        product_name = name_div.find('span', class_='a-size-base-plus a-color-base a-text-normal').text.strip()
                    for div in product_divs:
                        data_asin = div.get('data-asin')
                        if data_asin:
                            name_div = div.find('div', class_="s-widget-container s-spacing-small s-widget-container-height-small celwidget slot=MAIN template="
                                        "SEARCH_RESULTS widgetId=search-results_5")
                    price = None
                    price_div = div.find('div', class_='a-row a-size-base a-color-base')
                    if price_div:
                        price_span = price_div.find('span', class_='a-price')
                        if price_div:
                            price_span = price_div.find('span', class_='a-price-offset')
                            if price_span:
                                price = price_span.find('span', class_='a-offscreen').text.strip()
                    if product_name:
                        products_prices[product_name] = price
                    if len(products_prices) == 10:
                        break
    return products_prices


