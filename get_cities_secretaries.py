import pandas as pd

years = [2019, 2020]
df_cities = pd.read_csv('./data/cities_PE.csv')

for year in years:
    for city_id in df_cities.ID:

        try:
            filepath = './data/outputs{}/{}.csv'.format(year, city_id)
            df = pd.read_csv(filepath)

            df_health = df[df['NOME_UO'].str.contains('saude | saúde | médico | medico', case=False) == True]
            df_infrastructure = df[df['NOME_UO'].str.contains('infraestrutura | obras | secretaria construção', case=False) == True]
            df_education= df[df['NOME_UO'].str.contains('educa | educação | educacao | ensino | EDUCA', case=False) == True]

            df_health.to_csv('./data/secretaries/{}/health/{}.csv'.format(year, city_id), index=False)
            df_infrastructure.to_csv('./data/secretaries/{}/infrastructure/{}.csv'.format(year, city_id), index=False)
            df_education.to_csv('./data/secretaries/{}/education/{}.csv'.format(year, city_id), index=False)
        except:
            pass

print('Done!')