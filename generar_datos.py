import numpy as np
import pandas as pd

from datos import RUTA_CSV

SUCURSALES = {
    "San Salvador": 1.6,
    "Santa Ana": 1.1,
    "San Miguel": 1.0,
    "La Libertad": 0.8,
    "Sonsonate": 0.6,
}

# (producto, categoria, precio de venta, costo)
PRODUCTOS = [
    ("Refrigeradora 10 pies", "Electrodomesticos", 420.00, 310.00),
    ("Cocina a gas 4 hornillas", "Electrodomesticos", 260.00, 190.00),
    ("Licuadora 600W", "Electrodomesticos", 45.00, 31.00),
    ("Plancha de vapor", "Electrodomesticos", 28.00, 19.00),
    ("Laptop 15 pulgadas", "Tecnologia", 550.00, 430.00),
    ("Telefono celular", "Tecnologia", 220.00, 165.00),
    ("Television 43 pulgadas", "Tecnologia", 340.00, 260.00),
    ("Audifonos inalambricos", "Tecnologia", 35.00, 22.00),
    ("Juego de sabanas", "Hogar", 32.00, 20.00),
    ("Juego de ollas", "Hogar", 58.00, 38.00),
    ("Silla plastica", "Hogar", 12.00, 7.50),
    ("Mesa de comedor", "Hogar", 190.00, 130.00),
    ("Taladro electrico", "Ferreteria", 75.00, 52.00),
    ("Juego de destornilladores", "Ferreteria", 18.00, 11.00),
    ("Pintura galon", "Ferreteria", 24.00, 16.00),
    ("Cemento bolsa", "Ferreteria", 9.50, 7.20),
    ("Aceite 1 litro", "Alimentos", 2.80, 2.10),
    ("Arroz 5 libras", "Alimentos", 4.20, 3.30),
    ("Frijol 5 libras", "Alimentos", 5.50, 4.40),
    ("Azucar 5 libras", "Alimentos", 3.60, 2.90),
]


def generar_inventario():
    rng = np.random.default_rng(42)
    filas = []
    for sucursal, factor in SUCURSALES.items():
        for i, (producto, categoria, precio, costo) in enumerate(PRODUCTOS, start=1):
            filas.append(
                {
                    "id_producto": f"P{i:03d}",
                    "producto": producto,
                    "categoria": categoria,
                    "sucursal": sucursal,
                    "cantidad": int(rng.integers(0, 120) * factor),
                    "stock_minimo": int(rng.integers(10, 30)),
                    "precio_unitario": precio,
                    "costo_unitario": costo,
                }
            )
    return pd.DataFrame(filas)


if __name__ == "__main__":
    df = generar_inventario()
    df.to_csv(RUTA_CSV, index=False)
    print(f"Archivo generado: {RUTA_CSV} ({len(df)} filas)")
