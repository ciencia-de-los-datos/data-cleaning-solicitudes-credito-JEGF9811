"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""
import pandas as pd


def clean_data():
    import unicodedata
    df = pd.read_csv("solicitudes_credito.csv", sep=";")

   #poner todas las columna en minusculas
    df['sexo']=df['sexo'].str.lower()
    df['tipo_de_emprendimiento']=df['tipo_de_emprendimiento'].str.lower()
    df['idea_negocio']=df['idea_negocio'].str.lower()
    df['barrio']=df['barrio'].str.lower()
    df['línea_credito']=df['línea_credito'].str.lower()

    #eliminar las que tengan celdas vacias
    df = df.dropna(subset=['tipo_de_emprendimiento'], axis=0)
    df = df.dropna(subset=['comuna_ciudadano'], axis=0)
    df = df.dropna(subset=['barrio'], axis=0)

    #columna idea de negocio
    #cambiar - y _ por espacios y luego los espacios por _ para estandarizar y eliminar espacios al principio y al final
    df['idea_negocio'] = df['idea_negocio'].str.replace('_',' ').str.replace('-',' ').str.strip()
    df['idea_negocio'] = df['idea_negocio'].str.replace(' ','_')
    df['idea_negocio'] = df['idea_negocio'].apply(lambda x: unicodedata.normalize('NFKD',x).encode('ASCII','ignore').decode('utf-8'))


    #columna barrio
    #quitar espacios principio y final, cambiar estandarizar separacion con _ , cambiar ñ por n y quitar tildes
    df['barrio'] = df['barrio'].str.replace('_',' ').str.replace('-',' ').str.strip()
    df['barrio'] = df['barrio'].str.replace(' ','_')
    df['barrio'] = df['barrio'].apply(lambda x: unicodedata.normalize('NFKD',x).encode('ASCII','ignore').decode('utf-8'))

    #columna estrato
    #volver valores numericos y quitar los 0 que anteceden el numero
    df['estrato'] = pd.to_numeric(df['estrato'],errors='coerce',downcast='integer')

    #columna fecha de beneficio
    #Ajustar formatos de fecha a dd/mm/aaaa
    df['fecha_de_beneficio']=pd.to_datetime(df["fecha_de_beneficio"],format='mixed',dayfirst=True).dt.strftime('%d/%m/%Y')

    #columna monto_del_credito
    df['monto_del_credito'] = df['monto_del_credito'].str.replace('.00','').str.replace(',','').str.replace('$','').str.strip()

    #columna linea_credito
    df['línea_credito'] = df['línea_credito'].str.replace('_',' ').str.replace('-',' ').str.strip()
    df['línea_credito'] = df['línea_credito'].str.replace(' ','_').str.strip()

    #eliminar duplicados
    df.drop_duplicates(inplace=True)

    return df
