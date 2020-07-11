import pandas as pd
from bs4 import BeautifulSoup as Soup
import requests

if __name__ == '__main__':
    site_url = 'https://smokelab.me/%s'
    response = requests.get(site_url % 'catalog/tabak/')
    soup = Soup(response.content, 'html.parser')
    links = [site_url % a['href'] for a in soup.find('div', class_='catalog__sidebar').find_all('a')]

    constructor = {
        'Название': [],
        'Количество': []
    }

    for link in links:
        response = requests.get(link)
        soup = Soup(response.content, 'html.parser')
        items = soup.find_all('div', class_='products__list-item')
        for item in items:
            title = item.find('a', class_='products__list-item-name').text.strip()

            qty = item.find('div', class_='products__list-item-remains').strong.text.strip()
            constructor['Название'] += [title]
            constructor['Количество'] += [qty]

    df = pd.DataFrame(constructor)
    df = df.loc[df['Количество'] != '0 шт.']
    pd.DataFrame(df).to_excel('./result.xlsx', index=False)