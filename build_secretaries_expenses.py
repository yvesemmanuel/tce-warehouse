import pandas as pd


def build_secretaries_expenses():
    filepath = './data/secretaries/{}/{}/{}.csv'.format(2019, 'health', 5296)
    df = pd.read_csv(filepath)


    years = [2019, 2020]
    secretaries = ['education', 'health', 'infrastructure']
    df_cities = pd.read_csv('./data/cities_PE.csv')

    for year in years:
        rows = []

        for _, row in df_cities.iterrows():
            city_id = row['ID']
            city_name = row['city']

            for secretary in secretaries:
                try:
                    filepath = './data/secretaries/{}/{}/{}.csv'.format(year, secretary, city_id)
                    df = pd.read_csv(filepath)
                    
                    new_row = [city_name, city_id, round(sum(df.VALOR), 2), secretary]
                    rows.append(new_row)
                except:
                    pass

        df = pd.DataFrame(rows, columns=['city', 'city id', 'loan expense', 'secretary'])

        df.to_csv('./data/secretaries/expenses{}/expenses.csv'.format(year), index=False)


if __name__ == '__main__':
    print('Building...')
    build_secretaries_expenses()
    print('Done!')