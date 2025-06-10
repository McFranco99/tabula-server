from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from utils.finanza import calcola_piano_ammortamento

app = FastAPI()

# --- Somma cumulata (esistente) ---
class FormulaRequest(BaseModel):
    colonna: str
    numeri: List[int]

@app.post("/somma-cumulata", response_model=dict)
def somma_cumulata(req: FormulaRequest):
    cumulato, s = [], 0
    for n in req.numeri:
        s += n
        cumulato.append(s)
    return {"success": True, "colonna": req.colonna, "data": cumulato}

# --- Nuovo: Piano ammortamento estratto in utils/finanza.py ---
class AmmortamentoRequest(BaseModel):
    importo: float = Field(..., gt=0, description="Capitale > 0")
    tasso_annuo: float = Field(..., ge=0, description="Tasso annuo % ≥ 0")
    durata_anni: int = Field(..., gt=0, description="Durata anni > 0")

@app.post("/piano-ammortamento", response_model=dict)
def piano_ammortamento(req: AmmortamentoRequest):
    try:
        piano = calcola_piano_ammortamento(
            importo=req.importo,
            tasso_annuo_pct=req.tasso_annuo,
            durata_anni=req.durata_anni
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "success": True,
        "meta": {"n_rate": len(piano)},
        "data": piano
    }

@app.get("/")
def home():
    return {"message": "Benvenuto su Tabula Server!"}
