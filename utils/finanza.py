# utils/finanza.py

def calcola_piano_ammortamento(
    importo: float,
    tasso_annuo_pct: float,
    durata_anni: int,
    rate_per_anno: int = 12
) -> list[dict]:
    """
    Restituisce la lista delle rate con:
    mese, rata, interessi, capitale, debito_residuo.
    """
    tot_rate = durata_anni * rate_per_anno
    tasso_mensile = tasso_annuo_pct / 100 / rate_per_anno
    rata = importo * tasso_mensile / (1 - (1 + tasso_mensile) ** -tot_rate)
    saldo = importo
    piano = []

    for mese in range(1, tot_rate + 1):
        interessi = saldo * tasso_mensile
        capitale = rata - interessi
        saldo -= capitale
        piano.append({
            "mese": mese,
            "rata": round(rata, 2),
            "interessi": round(interessi, 2),
            "capitale": round(capitale, 2),
            "debito_residuo": round(max(saldo, 0), 2)
        })

    return piano
