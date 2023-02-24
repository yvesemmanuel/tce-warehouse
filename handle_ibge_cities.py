import pandas as pd
from unidecode import unidecode
import re

def format_count(x):
    try:
        number = x.split()[0].replace('.', '')
        
        return int(number)
    except:
        return None


def format_percentage_value(value):
    try:
        value = value.strip().replace(',', '.').replace('%', '')

        value = float(value) / 100
    
        return value
    except:
        return None
    

def format_money(value):
    try:
        # remove any thousand separators (dots) and currency symbols
        value = value.replace('.', '').replace(',', '.').split(' ')[0]

        # check if the value has a scale factor (×1000)
        if '×' in value:
            value, scale = value.split('×')
            value = float(value) * float(scale)
        else:
            value = float(value)

        return value
    except:
        return None


def format_count_float(value):
    try:
        count_str = re.search(r'\d+([.,]\d+)?', value).group()
        count_float = float(count_str.replace(',', '.'))
        return count_float
    except:
        return None
    

def format_ibge_cities(df: pd.DataFrame) -> pd.DataFrame:
    df['População estimada [2021]'] = df['População estimada [2021]'].apply(format_count)
    df['População no último censo [2010]'] = df['População no último censo [2010]'].apply(format_count)
    df['Pessoal ocupado [2020]'] = df['Pessoal ocupado [2020]'].apply(format_count)
    df['Matrículas no ensino fundamental [2021]'] = df['Matrículas no ensino fundamental [2021]'].apply(format_count)
    df['Matrículas no ensino médio [2021]'] = df['Matrículas no ensino médio [2021]'].apply(format_count)
    df['Docentes no ensino fundamental [2021]'] = df['Docentes no ensino fundamental [2021]'].apply(format_count)
    df['Docentes no ensino médio [2021]'] = df['Docentes no ensino médio [2021]'].apply(format_count)
    df['Número de estabelecimentos de ensino fundamental [2021]'] = df['Número de estabelecimentos de ensino fundamental [2021]'].apply(format_count)
    df['Número de estabelecimentos de ensino médio [2021]'] = df['Número de estabelecimentos de ensino médio [2021]'].apply(format_count)    

    df['População ocupada [2020]'] = df['População ocupada [2020]'].apply(format_percentage_value)
    df['Percentual da população com rendimento nominal mensal per capita de até 1/2 salário mínimo [2010]'] = df['Percentual da população com rendimento nominal mensal per capita de até 1/2 salário mínimo [2010]'].apply(format_percentage_value)
    df['Taxa de escolarização de 6 a 14 anos de idade [2010]'] = df['Taxa de escolarização de 6 a 14 anos de idade [2010]'].apply(format_percentage_value)
    df['Percentual das receitas oriundas de fontes externas [2015]'] = df['Percentual das receitas oriundas de fontes externas [2015]'].apply(format_percentage_value)

    df['PIB per capita [2020]'] = df['PIB per capita [2020]'].apply(format_money)
    df['Total de receitas realizadas [2017]'] = df['Total de receitas realizadas [2017]'].apply(format_money)
    df['Total de despesas empenhadas [2017]'] = df['Total de despesas empenhadas [2017]'].apply(format_money)

    df['Mortalidade Infantil [2020]'] = df['Mortalidade Infantil [2020]'].apply(format_count_float)
    df['Internações por diarreia [2016]'] = df['Internações por diarreia [2016]'].apply(format_count_float)
    df['Estabelecimentos de Saúde SUS [2009]'] = df['Estabelecimentos de Saúde SUS [2009]'].apply(format_count)
    df['Área urbanizada [2019]'] = df['Área urbanizada [2019]'].apply(format_count_float)
    df['Índice de Desenvolvimento Humano Municipal (IDHM) [2010]'] = df['Índice de Desenvolvimento Humano Municipal (IDHM) [2010]'].apply(format_count_float)

    df['Esgotamento sanitário adequado [2010]'] = df['Esgotamento sanitário adequado [2010]'].apply(format_percentage_value)
    df['Arborização de vias públicas [2010]'] = df['Arborização de vias públicas [2010]'].apply(format_percentage_value)
    df['Urbanização de vias públicas [2010]'] = df['Urbanização de vias públicas [2010]'].apply(format_percentage_value)
    df['População exposta ao risco [2010]'] = df['População exposta ao risco [2010]'].apply(format_count)

    df['Área da unidade territorial [2021]'] = df['Área da unidade territorial [2021]'].apply(format_count_float)

    return df


def get_all_ibge_cities_concatenated() -> pd.DataFrame:
    df_cities = pd.read_csv('./data/cities_PE.csv')

    rows = []
    for city in df_cities.city:
        city_ascii = unidecode(city.lower())
        words = city_ascii.split()
        filename = '_'.join(words)

        df = pd.read_csv('./data/IBGE_cities/{}.csv'.format(filename))

        rows.append(df.value.tolist())

    columns = df.attribute.tolist()

    return pd.DataFrame(rows, columns=columns)


def build_formatted_ibge_cities():
    df = get_all_ibge_cities_concatenated()
    df = format_ibge_cities(df)

    df.to_csv('./data/cities_IBGE.csv')


if __name__ == '__main__':
    print('Handling...')
    build_formatted_ibge_cities()
    print('Done!')
