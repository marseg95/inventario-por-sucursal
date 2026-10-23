import pandas as pd

from datos import cargar_inventario

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


def main():
    df = cargar_inventario()

    print("Dimensiones (filas, columnas):", df.shape)
    print("\nPrimeras filas:")
    print(df.head())

    print("\nTipos de datos:")
    print(df.dtypes)

    print("\nInformacion general:")
    df.info()

    print("\nValores nulos por columna:")
    print(df.isnull().sum())

    print("\nEstadisticas de columnas numericas:")
    print(df.describe())

    print("\nEstadisticas de columnas de texto:")
    print(df.select_dtypes(exclude=["number", "bool"]).describe())

    print("\nUnidades y valor del inventario por sucursal:")
    print(df.groupby("sucursal")[["cantidad", "valor_inventario"]].sum())


if __name__ == "__main__":
    main()
