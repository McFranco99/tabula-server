from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class FormulaRequest(BaseModel):
    colonna: str
    numeri: list[int]

@app.post("/somma-cumulata")
def somma_cumulata(req: FormulaRequest):
    cumulato = []
    somma = 0
    for n in req.numeri:
        somma += n
        cumulato.append(somma)
    return {"colonna": req.colonna, "risultato": cumulato}

@app.get("/")
def read_root():
    return {"message": "Benvenuto su Tabula!"}
