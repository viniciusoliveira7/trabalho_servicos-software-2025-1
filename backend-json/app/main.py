from typing import Optional, Union

from fastapi import FastAPI 
from fastapi import File, UploadFile

import json
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def diz_ola():
    return {"Olá" : "Mundo"}

class Item(BaseModel):
    name: str
    valor: float
    descricao: Optional[str] =None

@app.post("/json/")
async def upload_json(item: Item):
    return "Recebido objeto com nome: " + item.name

