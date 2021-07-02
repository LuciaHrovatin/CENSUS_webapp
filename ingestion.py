from zipfile import ZipFile

# Create a ZipFile Object and load sample.zip in it
with ZipFile('response.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall(path='./dataset')