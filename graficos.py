"""Funciones de graficos compartidas por la aplicacion y el informe."""

COLOR = "#2a6f97"
COLOR_ALERTA = "#c0392b"


def unidades_por_sucursal(ax, df):
    datos = df.groupby("sucursal")["cantidad"].sum().sort_values(ascending=False)
    ax.bar(datos.index, datos.values, color=COLOR)
    ax.set_title("Unidades en inventario por sucursal")
    ax.set_ylabel("Unidades")


def valor_por_sucursal(ax, df):
    datos = df.groupby("sucursal")["valor_inventario"].sum().sort_values(ascending=False)
    ax.bar(datos.index, datos.values, color=COLOR)
    ax.set_title("Valor del inventario por sucursal (costo)")
    ax.set_ylabel("USD")


def valor_por_categoria(ax, df):
    datos = df.groupby("categoria")["valor_inventario"].sum().sort_values()
    ax.barh(datos.index, datos.values, color=COLOR)
    ax.set_title("Valor del inventario por categoria (costo)")
    ax.set_xlabel("USD")


def bajo_minimo_por_sucursal(ax, df):
    datos = df.groupby("sucursal")["bajo_minimo"].sum().sort_values(ascending=False)
    ax.bar(datos.index, datos.values, color=COLOR_ALERTA)
    ax.set_title("Productos bajo el stock minimo por sucursal")
    ax.set_ylabel("Cantidad de productos")


GRAFICOS = {
    "Unidades por sucursal": unidades_por_sucursal,
    "Valor por sucursal": valor_por_sucursal,
    "Valor por categoria": valor_por_categoria,
    "Bajo stock minimo": bajo_minimo_por_sucursal,
}
