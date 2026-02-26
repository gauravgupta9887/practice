import asyncio

from fastapi import FastAPI, File, UploadFile
from typing import List
import time
import ocr
import utils

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Visit the endpoint: /api/v1/extract_text to perform \
        ocr."}


@app.post("/api/v1/extract_text")
async def extract_text(images: List[UploadFile] = File(...,),):
    response = {}
    s = time.time()
    for img in images:
        print("Images Uploaded:", img.filename)
        temp_file = utils._save_file_to_server(img, path='/tmp/',
                                               save_as=img.filename)
        text = await ocr.read_image(temp_file)
        response[img.filename] = text
    response["Time Taken"] = round((time.time() - s), 2)

    return response


@app.post("/api/v1/extract_text_concurrent")
async def extract_text_concurrent(images: List[UploadFile] = File(...,),):
    response = {}
    s = time.time()
    tasks = []
    for img in images:
        print("Images Uploaded:", img.filename)
        temp_file = utils._save_file_to_server(img, path='/tmp/',
                                               save_as=img.filename)
        tasks.append(asyncio.create_task(ocr.read_image(temp_file)))
    text = await asyncio.gather(*tasks)
    for i in range(len(text)):
        response[images[i].filename] = text[i]
    response["Time Taken"] = round((time.time() - s), 2)

    return response
