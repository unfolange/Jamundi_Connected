from dotenv import load_dotenv
load_dotenv()

import requests
from pathlib import Path
import pandas as pd
import numpy as np
import os
import re

def download_conectividad_data():
    """Download connectivity data from datos.gov.co API"""
    print("Downloading connectivity data...")
    url = f"https://www.datos.gov.co/api/v3/views/n48w-gutb/query.json?query=SELECT%20anno%2C%20trimestre%2C%20proveedor%2C%20cod_departamento%2C%20departamento%2C%20cod_municipio%2C%20municipio%2C%20segmento%2C%20tecnologia%2C%20velocidad_bajada%2C%20velocidad_subida%2C%20no_de_accesos%20WHERE%20(upper(%60municipio%60)%20LIKE%20'%25JAMUND%25')&app_token={os.getenv('APP_TOKEN')}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv('datos/conectividad_pais_raw.csv', index=False)
    print(f"Connectivity data saved: {len(df)} rows")
    return df

def load_conectividad_data():
    """Load connectivity data from CSV"""
    print("Loading connectivity data...")
    df = pd.read_csv('datos/conectividad_pais_raw.csv')
    print(f"Loaded: {len(df)} rows")
    return df

def clean_conectividad_data(df):
    """Clean connectivity data: convert types, normalize units, handle outliers"""
    print("Cleaning connectivity data...")
    
    # Convert string to numeric (replace comma with dot for decimals)
    df['velocidad_bajada'] = pd.to_numeric(df['velocidad_bajada'].str.replace(',', '.'))
    df['velocidad_subida'] = pd.to_numeric(df['velocidad_subida'].str.replace(',', '.'))
    df['no_de_accesos'] = pd.to_numeric(df['no_de_accesos'])
    
    # Normalize XDSL data (convert from Kbps to Mbps)
    def normalize_data_before_2020(x, col):
        if x['tecnologia'] == 'XDSL':
            return x[col] / 1000
        else:
            return x[col]
    
    df['velocidad_bajada'] = df.apply(normalize_data_before_2020, axis=1, args=['velocidad_bajada'])
    df['velocidad_subida'] = df.apply(normalize_data_before_2020, axis=1, args=['velocidad_subida'])
    
    # Create anno_trimestre column
    df['anno_trimestre'] = df['anno'].apply(str) + '-' + df['trimestre'].apply(str)
    
    print("Data cleaning complete")
    return df

def replace_outliers_iqr_efficient(df, column):
    """Replace outliers using IQR method by technology and segment groups"""
    print(f"Replacing outliers for {column} using IQR method...")
    
    # Calculate IQR by group
    grouped = df.groupby(['tecnologia', 'segmento'])[column]
    Q1 = grouped.transform('quantile', 0.25)
    Q3 = grouped.transform('quantile', 0.75)
    IQR = Q3 - Q1
    
    # Calculate limits
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    
    # Detect outliers
    outliers = (df[column] < lower) | (df[column] > upper)
    
    # Replace with median of the group
    median = grouped.transform('median')
    df.loc[outliers, column] = median[outliers]
    
    outliers_count = outliers.sum()
    print(f"Replaced {outliers_count} outliers in {column}")
    
    return df

def load_wifi_zones():
    """Load WiFi zones data"""
    print("Loading WiFi zones data...")
    url = f"https://www.datos.gov.co/api/v3/views/8zhi-vkbj/query.json?query=SELECT%20id_municipio%2C%20municipio%2C%20subregion%2C%20zonas_wifi%2C%20ubicacion%2C%20direccion%2C%20longitud%2C%20latitud%20WHERE%20(upper(%60municipio%60)%20LIKE%20'%25JAMUN%25')&app_token={os.getenv('APP_TOKEN')}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv('datos/Zonas_WiFi_en_el_Departamento_del_Valle_del_Cauca.csv', index=False)
    print(f"Jamundí WiFi zones data saved: {len(df)} rows")
    return df

def load_education_data():
    """Load education statistics"""
    print("Loading education data...")
    url = f"https://www.datos.gov.co/api/v3/views/nudc-7mev/query.json?query=SELECT%20a_o%2C%20c_digo_municipio%2C%20municipio%2C%20c_digo_departamento%2C%20departamento%2C%20c_digo_etc%2C%20etc%2C%20poblaci_n_5_16%2C%20tasa_matriculaci_n_5_16%2C%20cobertura_neta%2C%20cobertura_neta_transici_n%2C%20cobertura_neta_primaria%2C%20cobertura_neta_secundaria%2C%20cobertura_neta_media%2C%20cobertura_bruta%2C%20cobertura_bruta_transici_n%2C%20cobertura_bruta_primaria%2C%20cobertura_bruta_secundaria%2C%20cobertura_bruta_media%2C%20tama_o_promedio_de_grupo%2C%20sedes_conectadas_a_internet%2C%20deserci_n%2C%20deserci_n_transici_n%2C%20deserci_n_primaria%2C%20deserci_n_secundaria%2C%20deserci_n_media%2C%20aprobaci_n%2C%20aprobaci_n_transici_n%2C%20aprobaci_n_primaria%2C%20aprobaci_n_secundaria%2C%20aprobaci_n_media%2C%20reprobaci_n%2C%20reprobaci_n_transici_n%2C%20reprobaci_n_primaria%2C%20reprobaci_n_secundaria%2C%20reprobaci_n_media%2C%20repitencia%2C%20repitencia_transici_n%2C%20repitencia_primaria%2C%20repitencia_secundaria%2C%20repitencia_media%20WHERE%20(upper(%60municipio%60)%20LIKE%20'%25JAMUND%25')%20ORDER%20BY%20a_o%20DESC&app_token={os.getenv('APP_TOKEN')}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv('datos/MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR_BÁSICA_Y_MEDIA_POR_MUNICIPIO.csv', index=False)
    print(f"Loaded: {len(df)} rows")
    return df

def download_file(url, destination):
    """Download a file from URL if it doesn't exist"""
    destination_path = Path(destination)
    
    # Create directory if it doesn't exist
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Download only if file doesn't exist
    if not destination_path.exists():
        print(f"Downloading {destination_path.name}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(destination_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ Downloaded: {destination_path.name}")
        except Exception as e:
            print(f"✗ Error downloading {destination_path.name}: {e}")
            raise
    else:
        print(f"✓ File already exists: {destination_path.name}")

def load_censo_social():
    """Load 2018 census data for Jamundí"""
    print("Loading 2018 census data...")
    
    # Download file if needed
    url = 'https://www.dane.gov.co/files/censo2018/informacion-tecnica/PERSONAS_SOCIAL_Cuadros_CNPV_2018.XLSX'
    file_path = 'datos/PERSONAS_SOCIAL_Cuadros_CNPV_2018.XLSX'
    download_file(url, file_path)
    
    df = pd.read_excel(file_path, sheet_name='1PM', skiprows=9, header=0)

    new_col_names = {k: re.sub(r' .[0-9]+', '', k) + ' - ' + i + ': ' + j if i and j else k for i, j, k in zip(df.iloc[0].ffill(axis='index').fillna('').values,df.iloc[1].fillna('').values,df.columns.values)}

    new_names = [
        'Departamento',
        'Municipio',
        'área (Total, Cabecra, Resto)',
        'sexo',
        'edad',
        'Total personas',
        'Total personas: Si tiene alguna dificultad',
        'Total personas:No tiene dificultades',
    ]

    i = 0
    for k, v in new_col_names.items():
        if i < len(new_names):
            new_col_names[k] = new_names[i]
            i += 1
        else:
            break

    print(new_col_names)
    df.dropna(axis=1, how='all', inplace=True)
    df.rename(columns=new_col_names,inplace=True)
    df.drop(index=[0,1],inplace=True)
    df = df[df['Municipio'].fillna('').str.contains('Jamund')]

    df.to_csv('datos/censo_social_2018_jamundi.csv')
    print(f"Loaded: {len(df)} rows")
    return df

def load_censo_proyecciones():
    """Load and filter population projections for Jamundí"""
    print("Loading population projections...")
    
    # Download file if needed
    url = 'https://www.dane.gov.co/files/censo2018/proyecciones-de-poblacion/Municipal/DCD-area-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx'
    file_path = 'datos/DCD-area-proypoblacion-Mun-2020-2035-ActPostCOVID-19.xlsx'
    download_file(url, file_path)
    
    df = pd.read_excel(file_path, sheet_name='Hoja1', skiprows=8, header=0)
    
    df = df[df['DPMP'].str.contains('Jamund', na=False)]
    df = df.iloc[:-3]

    df.to_csv('datos/censo_proyecciones_jamundi_2020-2035.csv')
    print(f"Filtered Jamundí projections: {len(df)} rows")
    return df

if __name__ == "__main__":
    print("=" * 60)
    print("Data Preparation for Digital Inclusion Analysis")
    print("Valle del Cauca & Jamundí, Colombia")
    print("=" * 60)
    print()

    output_path = 'datos'
    os.makedirs(output_path, exist_ok=True)
    
    # Download connectivity data from API
    conectividad_df = download_conectividad_data()
    print()
    
    # Load connectivity data
    conectividad_df = load_conectividad_data()
    
    # Clean connectivity data
    conectividad_df = clean_conectividad_data(conectividad_df)
    
    # Apply IQR outlier filtering for velocidad_bajada and velocidad_subida
    conectividad_df = replace_outliers_iqr_efficient(conectividad_df, 'velocidad_bajada')
    conectividad_df = replace_outliers_iqr_efficient(conectividad_df, 'velocidad_subida')
    
    # Save cleaned data
    print("\nSaving cleaned connectivity data...")
    conectividad_df.to_csv('datos/conectividad_pais.csv', index=False)
    print(f"Cleaned data saved to: conectividad_pais.csv")
    print()
    
    # Load other datasets
    wifi_df = load_wifi_zones()
    education_df = load_education_data()
    censo_df = load_censo_social()
    proyecciones_df = load_censo_proyecciones()
    
    print()
    print("=" * 60)
    print("All datasets loaded and cleaned successfully!")
    print("=" * 60)
    print(f"\nCleaned connectivity file: conectividad_pais.csv ({len(conectividad_df)} rows)")
    print(f"WiFi zones: {len(wifi_df)} rows")
    print(f"Education data: {len(education_df)} rows")
    print(f"Census 2018: {len(censo_df)} rows")
    print(f"Population projections: {len(proyecciones_df)} rows")