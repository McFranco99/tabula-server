from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


# ✅ SOMMA CUMULATA ORIGINALE
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
def home():
    return {"message": "Benvenuto su Tabula Server!"}


# ✅ NUOVO: ENDPOINT PIANO AMMORTAMENTO
class AmmortamentoRequest(BaseModel):
    importo: float
    tasso_annuo: float
    durata_anni: int

@app.post("/piano-ammortamento")
def piano_ammortamento(req: AmmortamentoRequest):
    import math
    rate_annue = req.durata_anni
    rate_totali = rate_annue * 12
    tasso_mensile = req.tasso_annuo / 12 / 100
    importo = req.importo

    rata = importo * tasso_mensile / (1 - (1 + tasso_mensile)**-rate_totali)
    saldo = importo
    output = []

    for mese in range(1, rate_totali + 1):
        quota_interessi = saldo * tasso_mensile
        quota_capitale = rata - quota_interessi
        saldo -= quota_capitale

        output.append({
            "mese": mese,
            "rata": round(rata, 2),
            "interessi": round(quota_interessi, 2),
            "capitale": round(quota_capitale, 2),
            "debito_residuo": round(max(saldo, 0), 2)
        })

    return output
