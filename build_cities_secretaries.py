import pandas as pd


def build_query(words):
    return '|'.join(words)


def build_cities_secretaries():

    df_cities = pd.read_csv('./data/cities_PE.csv')

    years = [2019, 2020]
    health_terms = ['saude', 'saúde', 'médico', 'medico', 'sa?de', 'FUNDO MUNICIPAL DE SA', 'SAUDE', 'SA?DE', 'HOSPITALAR', 'MEDICA', 'MEDICAL', 'medica', 'Fundo Municipal de Saude', 'Fundo Municipal de Sa?', 'SUS', 'sus']
    infrastructure_terms = ['infraestrutura', 'obras', 'construção', 'constru', 'obra', 'infraes']
    education_terms = ['educa', 'educação', 'educacao', 'ensino', 'EDUCA', 'EDUCACAO', 'EDUC']

    query_health = build_query(health_terms)
    query_infrastructure = build_query(infrastructure_terms)
    query_education = build_query(education_terms)

    for year in years:
        for city_id in df_cities.ID:

            try:
                filepath = './data/outputs{}/{}.csv'.format(year, city_id)
                df = pd.read_csv(filepath)

                # HEALTH
                is_health_term_in_NOME_UO= df['NOME_UO'].str.contains(query_health, case=False, na=False) == True
                is_health_term_in_NOME_FONTE_REC = df['NOME_FONTE_REC'].str.contains(query_health, case=False, na=False) == True
                is_health_term_in_FORNEC = df['FORNEC'].str.contains(query_health, case=False, na=False) == True

                contains_health_terms = is_health_term_in_NOME_UO | is_health_term_in_NOME_FONTE_REC | is_health_term_in_FORNEC

                df_health = df[contains_health_terms]
                ########
                
                # infrastructure
                is_infrastructure_term_in_NOME_UO = df['NOME_UO'].str.contains(query_infrastructure, case=False, na=False) == True
                is_infrastructure_term_in_NOME_FONTE_REC = df['NOME_FONTE_REC'].str.contains(query_infrastructure, case=False, na=False) == True
                is_infrastructure_term_in_FORNEC = df['FORNEC'].str.contains(query_infrastructure, case=False, na=False) == True

                contains_infrastructure_terms = is_infrastructure_term_in_NOME_UO | is_infrastructure_term_in_NOME_FONTE_REC | is_infrastructure_term_in_FORNEC

                df_infrastructure = df[contains_infrastructure_terms]
                ################

                # education
                is_education_term_in_NOME_UO = df['NOME_UO'].str.contains(query_education, case=False, na=False) == True
                is_education_term_in_NOME_FONTE_REC = df['NOME_FONTE_REC'].str.contains(query_education, case=False, na=False) == True
                is_education_term_in_NOME_FORNEC = df['FORNEC'].str.contains(query_education, case=False, na=False) == True

                contains_education_terms = is_education_term_in_NOME_UO | is_education_term_in_NOME_FONTE_REC | is_education_term_in_NOME_FORNEC
                df_education = df[contains_education_terms]
                ###########

                df_health.to_csv('./data/secretaries/{}/health/{}.csv'.format(year, city_id), index=False)
                df_infrastructure.to_csv('./data/secretaries/{}/infrastructure/{}.csv'.format(year, city_id), index=False)
                df_education.to_csv('./data/secretaries/{}/education/{}.csv'.format(year, city_id), index=False)
            except:
                pass



if __name__ == '__main__':
    print('Building...')
    build_cities_secretaries()
    print('Done!')