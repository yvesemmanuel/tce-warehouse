import pandas as pd


def build_query(words):
    return '|'.join(words)


def build_cities_secretaries():

    df_cities = pd.read_csv('./data/cities_PE.csv')

    years = [2019, 2020]
    health_terms = ['saude', 'saúde', 'médico', 'medico', 'sa?de', 'FUNDO MUNICIPAL DE SA', 'SAUDE', 'SA?DE', 'HOSPITALAR', 'MEDICA', 'MEDICAL', 'medica', 'Fundo Municipal de Saude', 'Fundo Municipal de Sa?']
    infrastructure_terms = ['infraestrutura', 'obras', 'secretaria construção']
    education_terms = ['educa', 'educação', 'educacao', 'ensino', 'EDUCA']

    query_health = build_query(health_terms)
    query_infrastructure = build_query(infrastructure_terms)
    query_education = build_query(education_terms)

    for year in years:
        for city_id in df_cities.ID:

            try:
                filepath = './data/outputs{}/{}.csv'.format(year, city_id)
                df = pd.read_csv(filepath)

                df_health = df[df['NOME_UO'].str.contains(query_health, case=False, na=False) == True]
                df_infrastructure = df[df['NOME_UO'].str.contains(query_infrastructure, case=False, na=False) == True]
                df_education= df[df['NOME_UO'].str.contains(query_education, case=False, na=False) == True]

                df_health.to_csv('./data/secretaries/{}/health/{}.csv'.format(year, city_id), index=False)
                df_infrastructure.to_csv('./data/secretaries/{}/infrastructure/{}.csv'.format(year, city_id), index=False)
                df_education.to_csv('./data/secretaries/{}/education/{}.csv'.format(year, city_id), index=False)
            except:
                pass



if __name__ == '__main__':
    print('Building...')
    build_cities_secretaries()
    print('Done!')