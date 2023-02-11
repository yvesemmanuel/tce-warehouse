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

    delay_seconds = 10
    try:
        WebDriverWait(browser, delay_seconds).until(EC.presence_of_element_located((By.CLASS_NAME, 'painel__indicadores')))
        print('Found data from ' + city_name)
    except TimeoutException:
        print('Loading took too much time!')

    return browser.page_source


def get_city_attributes(city_name: str) -> pd.DataFrame:
    html = get_city_ibge_page(city_name)
    
    soup = BeautifulSoup(html, 'html.parser')

    attributes = []
    values = []

    for indicador in soup.find_all('div', {'class': 'indicador'}):

        try:
            attribute = indicador.find('div', {'class': 'indicador__nome'}).text
            value = indicador.find('div', {'class': 'indicador__valor'}).text
            attributes.append(attribute)
            values.append(value)
        except:
            pass

    return pd.DataFrame({'attributes': attributes, 'values': values})


def build_ibge_cities():
    df_cities = pd.read_csv('./data/cities_PE.csv')
    
    for city in df_cities.city:
        city_ascii = unidecode(city.lower())
        words = city_ascii.split()

        city_formatted = '-'.join(words)
        df_city = get_city_attributes(city_formatted)

        filename = '_'.join(words)
        df_city.to_csv('./data/IBGE_cities/{}.csv'.format(filename), index=False)


if __name__ == '__main__':
    print('Building...')
    build_ibge_cities()
    print('Done!')