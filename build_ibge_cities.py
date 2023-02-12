from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode


def get_city_ibge_page(city_name: str) -> str:
    url_ibge = 'https://cidades.ibge.gov.br/brasil/pe/{}/panorama'.format(city_name)
    
    browser = webdriver.Chrome()
    browser.get(url_ibge)

    delay_seconds = 30
    try:
        WebDriverWait(browser, delay_seconds).until(EC.presence_of_element_located((By.CLASS_NAME, 'lista__nome')))
        print('Found data from ' + city_name)
    except TimeoutException:
        print('Loading took too much time!')

    return browser.page_source


def get_city_attributes(city_name: str) -> pd.DataFrame:
    html = get_city_ibge_page(city_name)    
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', {'class': 'lista'})
    rows = table.find_all('tr', {'class': 'lista__indicador'})

    data = []
    for row in rows:
        nome = row.find('td', {'class': 'lista__nome'}).text.strip()
        valor = row.find('td', {'class': 'lista__valor'}).text.strip()

        data.append([nome, valor])

    return pd.DataFrame(data, columns=['attribute', 'value'])


def format_data(df: pd.DataFrame) -> pd.DataFrame:
    df['attribute'] = df['attribute'].apply(lambda x: ' '.join(x.split()))
    df['value'] = df['value'].apply(lambda x: ' '.join(x.split()))

    return df


def build_ibge_cities():
    df_cities = pd.read_csv('./data/cities_PE.csv')
    
    for city in df_cities.city:
        city_ascii = unidecode(city.lower())
        words = city_ascii.split()

        city_formatted = '-'.join(words)
        df_city = get_city_attributes(city_formatted)
        df_formatted = format_data(df_city)

        filename = '_'.join(words)
        df_formatted.to_csv('./data/IBGE_cities/{}.csv'.format(filename), index=False)


if __name__ == '__main__':
    print('Building...')
    build_ibge_cities()
    print('Done!')