import requests
from zipfile import ZipFile

# Automated download zip file from Banca d'Italia
url = "https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/documenti/storico/storico_ascii.zip?language_id=1"
target_path = "bancaditalia_dataset.zip"
response = requests.get(url, stream=True)
handle = open(target_path, "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:  # filter out keep-alive new chunks
        handle.write(chunk)
handle.close()

# Create a ZipFile Object and load sample.zip in it
with ZipFile('bancaditalia_dataset.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall(path='./dataset')