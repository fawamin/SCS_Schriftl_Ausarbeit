import os
from fastapi import FastAPI,HTTPException,Response
from api import Api
from pydantic import BaseModel

class File(BaseModel):
    Filename: str

app = FastAPI()
connection = Api()

@app.get("/gol/", responses = {200:{"content":{"image/png":{}}}})
def get_day():
    return connection.get_img()

@app.post("/gol/")
def set_gol_file(file: File,response: Response):   
    name = file.Filename
    filePath = "Saves/"+name+".npy"
    try:
        connection.init_file(filePath)
        response.status_code = 200
    except:
        response.status_code = 404

@app.get("/gol/cycle")
def cycle():
    connection.api_cycle()