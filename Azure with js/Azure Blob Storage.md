### what we need to setup on Azure
1. create a storage account
	1. in networking enable public access from all networks
	2. defaults for everything else
2. create a container in the storage account
	1. in the LHS find Shared Access Signature allow resource type of object
	2. we need the SAS token

### what we need in the node.js app
> npm install -- save @azure/storage-blob mongodb dotenv

in the .env file
```env
SASTOKEN=""
ACCOUNTNAME="yapperstorage"
CONTAINERNAME="yapperstorage"
```


AzureBlobService.js
```jsx
const { BlobServiceClient } = require('@azure/storage-blob');  
const dotenv = require('dotenv');  
dotenv.config();  
const accountName = process.env.ACCOUNTNAME;  
const containerName = process.env.CONTAINERNAME;  
const sasToken = process.env.SASTOKEN;  
  
const blobServiceClient = new BlobServiceClient(  
  `https://${accountName}.blob.core.windows.net/?${sasToken}`  
);  
const container = blobServiceClient.getContainerClient(containerName);  
  
async function uploadImageStream(filename, file) {  
  const blob = container.getBlockBlobClient(filename);  
  await blob.uploadData(file);  
  return blob.url;  
}  
  
async function saveToBlob(filename, ext, file) {  
  try {  
    const imageUrl = await uploadImageStream(filename, file);  
    return { imageUrl };  
  } catch (e) {  
    console.log('error uploading: ' + e);  
  }  
}  
module.exports = saveToBlob;
```

