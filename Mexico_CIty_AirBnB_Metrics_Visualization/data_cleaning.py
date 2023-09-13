# -*- coding: utf-8 -*-
import pandas as pd

zipcodes = ['05000', '06000', '01000', '11000', '04000', '15241',
            '03000', '10000', '14739', '08000', '09870', '07000',
            '16000', '02000', '13000', '12000']

def ZipCode(neighborhood):
    if neighborhood == 'Cuajimalpa de Morelos':
        return zipcodes[0];
    elif neighborhood == 'Cuauhtemoc':
        return zipcodes[1];
    elif neighborhood == 'Alvaro Obregon' :
        return zipcodes[2];
    elif neighborhood == 'Miguel Hidalgo':
        return zipcodes[3];
    elif neighborhood == 'Coyoacan' :
        return zipcodes[4];
    elif neighborhood == 'Venustiano Carranza' :
        return zipcodes[5];
    elif neighborhood == 'Benito Juarez' :
        return zipcodes[6];
    elif neighborhood == 'La Magdalena Contreras' :
        return zipcodes[7];
    elif neighborhood == 'Tlalpan':
        return zipcodes[8];
    elif neighborhood == 'Iztacalco' :
        return zipcodes[9];
    elif neighborhood == 'Iztapalapa' :
        return zipcodes[10];
    elif neighborhood == 'Gustavo A. Madero' :
        return zipcodes[11];
    elif neighborhood == 'Xochimilco':
        return zipcodes[12];
    elif neighborhood == 'Azcapotzalco' :
        return zipcodes[13];
    elif neighborhood == 'Tlahuac':
        return zipcodes[14];
    elif neighborhood == 'Milpa Alta' :
        return zipcodes[15];
    else:
        return 0;
    
df = pd.read_csv('listings.csv') #Reading the 

# print(df.columns)

#print(df['neighbourhood_cleansed'])

df.drop(['description','neighborhood_overview','name','listing_url','host_about', 'picture_url', 'host_url', 'host_thumbnail_url',
         'host_picture_url', 'host_neighbourhood'], inplace=True, axis=1)

#print(df['neighbourhood_cleansed'].unique())

# df['neighbourhood_cleansed'] = df['neighbourhood_cleansed'].replace('Cuauhtémoc', 'Cuauhtemoc')

# df['neighbourhood_cleansed'] = df['neighbourhood_cleansed'].replace('Álvaro Obregón', 'Alvaro Obregon')

# df['neighbourhood_cleansed'] = df['neighbourhood_cleansed'].replace('Coyoacán', 'Coyoacan')

# df['neighbourhood_cleansed'] = df['neighbourhood_cleansed'].replace('Benito Juárez', 'Benito Juarez')

# df['neighbourhood_cleansed'] = df['neighbourhood_cleansed'].replace('Tláhuac', 'Tlahuac')

# print(df['neighbourhood_cleansed'].unique())

df['ZipCode'] = df['neighbourhood_cleansed'].apply(ZipCode)

df.to_excel('data_cleaned_2.xlsx', index = False)