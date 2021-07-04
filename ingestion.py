import requests
from zipfile import ZipFile
import os
import shutil


# Automated download zip file from Banca d'Italia
url14 = "https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/documenti/ind14_ascii.zip"
target_path = "bancaditalia_dataset_14.zip"
response = requests.get(url14, stream=True)
handle = open(target_path, "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:  # filter out keep-alive new chunks
        handle.write(chunk)
handle.close()

# Create a ZipFile Object and load sample.zip in it
file_to_keep14 = ["carcom14.csv", "rfam14.csv", "rper14.csv"]
with ZipFile('bancaditalia_dataset_14.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall(path='./dataset')

for i in file_to_keep14:
    shutil.move("dataset/CSV/"+i, "dataset")

if os.path.exists('dataset/CSV'):
    shutil.rmtree('dataset/CSV')

# Automated download zip file from Banca d'Italia
url16 = "https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/documenti/ind16_ascii.zip"
target_path = "bancaditalia_dataset_16.zip"
response = requests.get(url16, stream=True)
handle = open(target_path, "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:  # filter out keep-alive new chunks
        handle.write(chunk)
handle.close()

# Create a ZipFile Object and load sample.zip in it
file_to_keep16 = ["carcom16.csv", "rfam16.csv", "rper16.csv"]
with ZipFile('bancaditalia_dataset_16.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   # zipObj.extractall(path='./dataset')
   for i in file_to_keep16:
       zipObj.extract(i, path='./dataset')

