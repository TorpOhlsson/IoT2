import os
import zipfile
from azure.storage.blob import BlobServiceClient
from datetime import datetime

d_time = datetime.now()
time = d_time.strftime("%d-%m-%Y_%H-%M-%S")

zipFile = "backup.zip" + str(time)

with zipfile.ZipFile(zipFile, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write("database.db", "database.db")
print("Zipfil oprettet med SQLite-databasefil:", zipFile)

azureStorage = "DefaultEndpointsProtocol=https;AccountName=XXXX;AccountKey=XXXXXXXXX;EndpointSuffix=core.windows.net"
blobName = "default"
blobService = BlobServiceClient.from_connection_string(azureStorage)
blobClient = blobService.get_container_client(blobName)

with open(zipFile, "rb") as data:
	blobClient.upload_blob(name=os.path.basename(zipFile), data=data)
print("Zipfil uploadet til Azure Blob Storage.")

try:
	os.remove(zipFile)
except:
	print("!!")
