"""Genera el informe de consultoria en PDF a partir del inventario."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
from matplotlib.figure import Figure
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from datos import cargar_inventario
from graficos import GRAFICOS

# Completar con los datos del equipo antes de generar el informe.
INTEGRANTES = ["Nombre del integrante 1", "Nombre del integrante 2"]
INSTITUCION = "Nombre de la institucion"
CURSO = "Nombre del curso"
FECHA = "Octubre de 2026"

CARPETA = Path(__file__).parent
CARPETA_GRAFICOS = CARPETA / "graficos_informe"
SALIDA = CARPETA / "informe_consultoria.pdf"

estilos = getSampleStyleSheet()
TITULO = ParagraphStyle("Portada", parent=estilos["Title"], fontSize=24, leading=30)
SUBTITULO = ParagraphStyle("Sub", parent=estilos["Normal"], fontSize=14, alignment=1, leading=20)
CUERPO = ParagraphStyle("Cuerpo", parent=estilos["Normal"], fontSize=10.5, leading=15, spaceAfter=6)


def usd(valor):
    return f"${valor:,.2f}"


def guardar_graficos(df):
    CARPETA_GRAFICOS.mkdir(exist_ok=True)
    rutas = []
    for i, funcion in enumerate(GRAFICOS.values(), start=1):
        figura = Figure(figsize=(6.5, 3.4), tight_layout=True)
        funcion(figura.add_subplot(111), df)
        ruta = CARPETA_GRAFICOS / f"grafico_{i}.png"
        figura.savefig(ruta, dpi=150)
        rutas.append(ruta)
    return rutas


def tabla(datos, anchos=None):
    t = Table(datos, colWidths=anchos, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2a6f97")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef3f7")]),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ]
        )
    )
    return t


def calcular(df):
    """Calcula las cifras que usa el texto del informe."""
    por_sucursal = df.groupby("sucursal").agg(
        unidades=("cantidad", "sum"),
        valor=("valor_inventario", "sum"),
        bajo_minimo=("bajo_minimo", "sum"),
    )
    por_categoria = df.groupby("categoria").agg(
        unidades=("cantidad", "sum"),
        valor=("valor_inventario", "sum"),
        bajo_minimo=("bajo_minimo", "sum"),
    )
    margen = ((df["precio_unitario"] - df["costo_unitario"]) / df["precio_unitario"] * 100)
    return por_sucursal, por_categoria, margen


def portada():
    historia = [Spacer(1, 1.5 * inch)]
    historia.append(Paragraph(INSTITUCION, SUBTITULO))
    historia.append(Paragraph(CURSO, SUBTITULO))
    historia.append(Spacer(1, 1 * inch))
    historia.append(Paragraph("Informe de consultoria", TITULO))
    historia.append(Paragraph("Analisis del inventario por sucursal", SUBTITULO))
    historia.append(Spacer(1, 0.6 * inch))
    historia.append(Paragraph("Empresa: comercializadora salvadorena con cinco sucursales", SUBTITULO))
    historia.append(Spacer(1, 1 * inch))
    historia.append(Paragraph("<b>Integrantes</b>", SUBTITULO))
    for nombre in INTEGRANTES:
        historia.append(Paragraph(nombre, SUBTITULO))
    historia.append(Spacer(1, 0.6 * inch))
    historia.append(Paragraph(FECHA, SUBTITULO))
    historia.append(PageBreak())
    return historia


def analisis(df, por_sucursal, por_categoria, margen, graficos):
    total_valor = df["valor_inventario"].sum()
    total_unidades = df["cantidad"].sum()
    top_valor = por_sucursal["valor"].idxmax()
    low_valor = por_sucursal["valor"].idxmin()
    top_uni = por_sucursal["unidades"].idxmax()
    low_uni = por_sucursal["unidades"].idxmin()
    cat_valor = por_categoria["valor"].idxmax()
    pct_cat = por_categoria["valor"].max() / total_valor * 100
    bajo = int(df["bajo_minimo"].sum())

    h = [Paragraph("1. Analisis de hallazgos", estilos["Heading1"])]
    h.append(
        Paragraph(
            f"El inventario analizado contiene {len(df)} registros (20 productos en 5 sucursales), "
            f"con {total_unidades:,} unidades y un valor total a costo de {usd(total_valor)}. "
            "No se encontraron valores nulos en ninguna columna.",
            CUERPO,
        )
    )

    h.append(Paragraph("1.1 Resumen por sucursal", estilos["Heading2"]))
    filas = [["Sucursal", "Unidades", "Valor a costo", "Productos bajo minimo"]]
    for suc, r in por_sucursal.sort_values("valor", ascending=False).iterrows():
        filas.append([suc, f"{int(r.unidades):,}", usd(r.valor), int(r.bajo_minimo)])
    h.append(tabla(filas, [1.7 * inch, 1.2 * inch, 1.6 * inch, 1.8 * inch]))
    h.append(Spacer(1, 8))
    h.append(
        Paragraph(
            f"{top_uni} concentra la mayor cantidad de unidades y {low_uni} la menor. "
            f"En valor, la sucursal con mayor inventario es {top_valor} y la de menor es {low_valor}. "
            "La diferencia entre unidades y valor indica que el mix de productos pesa mas que el volumen.",
            CUERPO,
        )
    )
    h.append(Image(str(graficos[0]), width=6 * inch, height=3.1 * inch))
    h.append(Image(str(graficos[1]), width=6 * inch, height=3.1 * inch))

    h.append(Paragraph("1.2 Resumen por categoria", estilos["Heading2"]))
    filas = [["Categoria", "Unidades", "Valor a costo", "Productos bajo minimo"]]
    for cat, r in por_categoria.sort_values("valor", ascending=False).iterrows():
        filas.append([cat, f"{int(r.unidades):,}", usd(r.valor), int(r.bajo_minimo)])
    h.append(tabla(filas, [1.7 * inch, 1.2 * inch, 1.6 * inch, 1.8 * inch]))
    h.append(Spacer(1, 8))
    h.append(
        Paragraph(
            f"La categoria {cat_valor} representa el {pct_cat:.1f}% del valor del inventario. "
            "Las categorias de alto precio unitario concentran el capital aunque no tengan mas unidades.",
            CUERPO,
        )
    )
    h.append(Image(str(graficos[2]), width=6 * inch, height=3.1 * inch))

    h.append(Paragraph("1.3 Productos bajo el stock minimo", estilos["Heading2"]))
    h.append(
        Paragraph(
            f"Se detectaron {bajo} registros (producto por sucursal) con existencias por debajo del "
            "stock minimo definido, lo que equivale a "
            f"{bajo / len(df) * 100:.0f}% del inventario.",
            CUERPO,
        )
    )
    h.append(Image(str(graficos[3]), width=6 * inch, height=3.1 * inch))
    h.append(PageBreak())
    return h


def conclusiones(df, por_sucursal, por_categoria, margen):
    c = df["cantidad"]
    mas_caro = df.loc[df["precio_unitario"].idxmax(), "producto"]
    mas_barato = df.loc[df["precio_unitario"].idxmin(), "producto"]
    valor_prod = df.groupby("producto")["valor_inventario"].sum().sort_values(ascending=False)
    top3 = valor_prod.head(3)
    pct_top3 = top3.sum() / df["valor_inventario"].sum() * 100
    sin_cantidad = int((c == 0).sum())

    items = [
        (
            "id_producto y producto",
            f"Hay {df['producto'].nunique()} productos distintos, cada uno presente en las 5 sucursales. "
            f"Los tres con mayor valor inmovilizado ({', '.join(top3.index)}) suman {pct_top3:.1f}% "
            "del valor total, por lo que el control debe concentrarse en ellos.",
        ),
        (
            "categoria",
            f"Existen {df['categoria'].nunique()} categorias con 4 productos cada una. "
            f"{por_categoria['valor'].idxmax()} domina el valor y "
            f"{por_categoria['valor'].idxmin()} es la de menor valor, aunque mueve productos de consumo basico.",
        ),
        (
            "sucursal",
            f"{por_sucursal['unidades'].idxmax()} tiene {por_sucursal['unidades'].max():,} unidades y "
            f"{por_sucursal['unidades'].idxmin()} tiene {por_sucursal['unidades'].min():,}. "
            "La distribucion no es uniforme entre sucursales.",
        ),
        (
            "cantidad",
            f"El promedio es {c.mean():.1f} unidades por registro (mediana {c.median():.0f}), con minimo {c.min()} "
            f"y maximo {c.max()}. La desviacion estandar de {c.std():.1f} muestra alta variabilidad. "
            f"Registros sin existencias: {sin_cantidad}.",
        ),
        (
            "stock_minimo",
            f"Varia entre {df['stock_minimo'].min()} y {df['stock_minimo'].max()} unidades. "
            f"{int(df['bajo_minimo'].sum())} registros estan por debajo de este umbral, lo que senala riesgo de desabastecimiento.",
        ),
        (
            "precio_unitario",
            f"Va de {usd(df['precio_unitario'].min())} ({mas_barato}) a {usd(df['precio_unitario'].max())} ({mas_caro}). "
            f"La mediana es {usd(df['precio_unitario'].median())}, muy por debajo del promedio de "
            f"{usd(df['precio_unitario'].mean())}, lo que indica pocos productos de precio alto.",
        ),
        (
            "costo_unitario",
            f"El costo promedio es {usd(df['costo_unitario'].mean())}. El margen bruto promedio sobre el precio es "
            f"{margen.mean():.1f}%, con un rango de {margen.min():.1f}% a {margen.max():.1f}%.",
        ),
        (
            "valor_inventario (calculada)",
            f"Es el producto de cantidad por costo. El total es {usd(df['valor_inventario'].sum())} y el promedio por "
            f"registro {usd(df['valor_inventario'].mean())}, con gran dispersion ({usd(df['valor_inventario'].std())} de desviacion).",
        ),
    ]
    h = [Paragraph("2. Conclusiones por variable", estilos["Heading1"])]
    for nombre, texto in items:
        h.append(Paragraph(f"<b>{nombre}</b>", CUERPO))
        h.append(Paragraph(texto, CUERPO))
    h.append(PageBreak())
    return h


def recomendaciones(df, por_sucursal, por_categoria):
    alta = por_sucursal["bajo_minimo"].idxmax()
    cat_alta = por_categoria["bajo_minimo"].idxmax()
    cat_valor = por_categoria["valor"].idxmax()
    exceso = por_sucursal["valor"].idxmax()
    escasa = por_sucursal["unidades"].idxmin()
    textos = [
        f"Reabastecer de inmediato los productos bajo el stock minimo, priorizando {alta} (mayor numero de productos en alerta) "
        f"y la categoria {cat_alta}, que acumula mas casos.",
        f"Redistribuir inventario entre sucursales: transferir existencias desde {exceso} (mayor valor inmovilizado) "
        f"hacia {escasa} (menor numero de unidades) antes de comprar mas producto.",
        f"Reducir el capital inmovilizado en {cat_valor} con compras mas frecuentes y en menor volumen, ya que es la categoria de mayor valor.",
        "Definir el stock minimo segun la rotacion de cada producto y sucursal, en lugar de usar un rango general.",
        "Aplicar un sistema de clasificacion ABC y revisar con mayor frecuencia los pocos productos que concentran el valor.",
        "Registrar ventas por periodo para medir la rotacion real y calcular el punto de reorden de forma objetiva.",
        "Mantener este tablero de inventario como herramienta de control mensual y ampliarlo con fechas de ingreso y ventas.",
    ]
    h = [Paragraph("3. Recomendaciones estrategicas", estilos["Heading1"])]
    for i, t in enumerate(textos, start=1):
        h.append(Paragraph(f"{i}. {t}", CUERPO))
    return h


def main():
    df = cargar_inventario()
    por_sucursal, por_categoria, margen = calcular(df)
    graficos = guardar_graficos(df)

    historia = portada()
    historia += analisis(df, por_sucursal, por_categoria, margen, graficos)
    historia += conclusiones(df, por_sucursal, por_categoria, margen)
    historia += recomendaciones(df, por_sucursal, por_categoria)

    SimpleDocTemplate(str(SALIDA), pagesize=letter, title="Informe de consultoria").build(historia)
    print(f"Informe generado: {SALIDA}")


if __name__ == "__main__":
    main()
