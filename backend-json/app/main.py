from typing import Optional, Union

from fastapi import FastAPI 
from fastapi import File, UploadFile

import json
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def diz_ola():
    return {"Olá" : "Mundo"}



