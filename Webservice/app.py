from fastapi import FastAPI,HTTPException,Response
from api import Api

app = FastAPI()
connection = Api()

@app.get("/gol/")
def get_day():
    return connection.get_img()

@app.put("/gol/{Filename}")
def set_gol_file(Filename : str, response: Response):
    try:
        connection = Api("Saves/"+Filename)
        response.status_code = 200
    except:
        response.status_code = 404

@app.get("/gol/cycle")
def cycle():
    connection.api_cycle()