from fastapi import FastAPI,HTTPException
from datetime import datetime
from pydantic import BaseModel,ValidationError
from pydantic.datetime_parse import parse_datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient,BlobType,BlobBlock
from database import SessionLocal, engine,Base
from models import Blob
from dotenv import load_dotenv

import os, uuid
import base64

# creating tables, api instance and db session
Base.metadata.create_all(engine)
app = FastAPI()
db = SessionLocal()

# loading env variables and grabbing them
load_dotenv()
ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
KEY = os.getenv("KEY")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")

# auth credentials for azure cloud storage
connection_string = connection_string = f"DefaultEndpointsProtocol=https;AccountName={ACCOUNT_NAME};AccountKey={KEY};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)


# custom class for utc as naivedatetime 
class NaiveDatetime(datetime):

    @classmethod
    def __get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls,v):
        v = parse_datetime(v)
        v = v.replace(tzinfo=None)
        return v

# serializing our model
class Image(BaseModel):
    date: datetime
    utc: NaiveDatetime
    base64_str: str
    id: str





@app.post("/images")
async def root(item: Image) -> Image:
    try:
        # decoding image from base64 to bytes and creating the corresponding and then uploading it
        image_content = base64.b64decode((item.base64_str))
        source_blob_client = container_client.get_blob_client(f"{item.date.strftime('%m-%d-%Y-%H-%M-%S')}")
        source_blob_client.upload_blob(image_content,overwrite = True)
    
        # adding record to the db
        db_blob = Blob(blob_url = source_blob_client.url,camera_id = item.id,date = item.date)
        db.add(db_blob)
        db.commit()

        return item
      
    except Exception as e:
        raise HTTPException(status_code=404,detail = str(e))

