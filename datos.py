from pathlib import Path

import pandas as pd

RUTA_CSV = Path(__file__).parent / "inventario.csv"


def cargar_inventario(ruta=RUTA_CSV):
    """Carga el inventario y agrega dos columnas calculadas."""
    df = pd.read_csv(ruta)
    df["valor_inventario"] = df["cantidad"] * df["costo_unitario"]
    df["bajo_minimo"] = df["cantidad"] < df["stock_minimo"]
    return df
