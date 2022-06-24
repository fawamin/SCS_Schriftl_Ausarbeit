import os
from fastapi import FastAPI,HTTPException,Response
from fastapi.middleware.cors import CORSMiddleware
from api import Api
from pydantic import BaseModel

class File(BaseModel):
    Filename: str

app = FastAPI()
connection = Api()

# @TODO Properly configure CORS 
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/gol/")
def get_day():
    return connection.get_array()

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