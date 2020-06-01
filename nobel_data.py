import pandas as pd
import numpy as np

nobel = pd.read_csv('datasets/nobel.csv')

nobel['birth_country'] = nobel['birth_country'].str.replace('United States of America', 'USA')
nobel['birth_country'] = nobel['birth_country'].str.replace('United Kingdom', 'U.K')
nobel['birth_country'] = nobel['birth_country'].str.replace(r'.*\((.*)\)', r'\1', regex=True)
nobel['birth_country'] = nobel['birth_country'].fillna('Unknown')

countries = ['USA', 'U.K', 'Germany', 'France', 'Sweden', 'Russia', 'Japan', 'Poland']

def others_countries(country):
    if country in countries:
        return country
    return 'Others'

nobel['Country'] = nobel['birth_country'].apply(others_countries)

nobel['Decade'] = (np.floor(nobel['year']/10) * 10).astype(int).astype('str')

nobel['death_date'] = nobel['death_date'].fillna('Alive')

nobel['motivation'] = nobel['motivation'].fillna('Unknown')

nobel['organization_name'] = nobel['organization_name'].str.replace(r'.*\((.*)\)', r'\1', regex=True)
nobel['organization_name'] = nobel['organization_name'].str.replace('MRC Laboratory of Molecular Biology', 'MRC')
nobel['organization_name'] = nobel['organization_name'].str.replace(r'University of (.*)', r'\1', regex=True)
nobel['organization_name'] = nobel['organization_name'].str.replace(r'(.*) University', r'\1', regex=True)
nobel['organization_name'] = nobel['organization_name'].str.replace('California', 'UC')
nobel['organization_name'] = nobel['organization_name'].str.replace('Chicago', 'UChicago')

organization_names = ['UC', 'Harvard', 'MIT', 'Stanford', 'UChicago', 'Cambridge', 'Caltech', 'Columbia', 
                      'Princeton', 'Rockefeller', 'MRC', 'Cornell', 'Washington', 'Oxford', 'Yale']

def others_organizations(organization):
    if organization in organization_names:
        return organization
    return 'others'

nobel['Affiliations'] = nobel['organization_name'].apply(others_organizations)

nobel['prize_share'] = nobel['prize_share'].str.replace(r'1/(.*)', r'\1', regex=True)


nobel['Category'] = nobel['category']
nobel['Year'] = nobel['year']
