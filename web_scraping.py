import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    #items = soup.find_all('div', class_='ui-search-result__content-wrapper')
    #items = soup.find_all('div', class_='ui-search-result__wrapper')
    items = soup.find_all('div', class_='poly-card poly-card--list')
    data = []
    for item in items:
        try:
            #name = item.find('h2', class_='ui-search-item__title').text.strip()
            name = item.find('h2', class_='poly-box').text.strip()
        except AttributeError:
            name = None

        try:
            currency = item.find('span', class_='andes-money-amount__currency-symbol').text.strip()
        except AttributeError:
            currency = None

        try:
            price = item.find('span', class_='andes-money-amount__fraction').text.strip()
        except AttributeError:
            price = None

        try:
          reviews = item.find('span', class_='andes-visually-hidden').text.strip()
        except AttributeError:
            reviews = None

        # Handle potential None result from .find()
        link_element = item.find('a', class_='poly-component__title')
        if link_element:  # Check if link_element is not None
            link = link_element['href']
        else:
            link = None

        # Handle potential None result from .find()
        #image_element = item.find('img', class_='ui-search-result-image__element')
        image_element = item.find('img', class_='poly-component__picture poly-component__picture--square')
        if image_element:  # Check if image_element is not None
            image_url = image_element['src']
        else:
            image_url = None


        data.append({
            'Name': name,
            'Currency': currency,
            'Price': price,
            'Reviews': reviews,
            'Product URL': link,
            'Image URL': image_url
        })

    return data

def main():
    base_url = 'https://listado.mercadolibre.com.hn/celulares-smartphones'
    data = []

    for page in range(1, 11):  # Scraping the first 10 pages
        url = f'{base_url}_Desde_{(page - 1) * 50 + 1}'
        page_data = get_data(url)
        if page_data:
            data.extend(page_data)

    df = pd.DataFrame(data)
    df.to_excel('data_scrap_celulares-smartphones.xlsx', index=False)
    print('Datos guardados en data_scrap_celulares-smartphones.xlsx')

if __name__ == '__main__':
    main()