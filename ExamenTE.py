import pandas as pd
import requests
import hashlib
import time
import sqlite3
import json

# Obtener datos de la API
response = requests.get("https://restcountries.com/v3.1/all")
countries = response.json()

# Función para encriptar con SHA1
def sha1_encrypt(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

# Crear una lista para almacenar los datos
data = []

# Procesar los datos
for country in countries:
    region = country.get('region', '')
    city_name = country.get('name', {}).get('common', '')
    languages = country.get('languages', {}).values()
    
    for language in languages:
        start_time = time.time()
        encrypted_language = sha1_encrypt(language)
        end_time = time.time()
        processing_time = (end_time - start_time) * 1000  # Convertir a milisegundos
        
        data.append({
            "Region": region,
            "City Name": city_name,
            "Language": encrypted_language,
            "Time": processing_time
        })

# Crear el DataFrame
df = pd.DataFrame(data)

# Calcular métricas de tiempo
total_time = df['Time'].sum()
average_time = df['Time'].mean()
min_time = df['Time'].min()
max_time = df['Time'].max()

print(f"Total Time: {total_time:.2f} ms")
print(f"Average Time: {average_time:.2f} ms")
print(f"Min Time: {min_time:.2f} ms")
print(f"Max Time: {max_time:.2f} ms")

# Guardar en SQLite
conn = sqlite3.connect('data.db')
df.to_sql('countries', conn, if_exists='replace', index=False)
conn.close()

# Guardar en JSON
df.to_json('data.json', orient='records', lines=True)

# Pruebas unitarias
def test_sha1_encrypt():
    assert sha1_encrypt('English') == hashlib.sha1('English'.encode('utf-8')).hexdigest()

def test_processing_time():
    start_time = time.time()
    sha1_encrypt('English')
    end_time = time.time()
    assert (end_time - start_time) > 0

# Ejecutar pruebas
test_sha1_encrypt()
test_processing_time()