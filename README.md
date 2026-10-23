# Inventario por sucursal

Proyecto de consultoria de datos para una empresa salvadorena con sucursales en
San Salvador, Santa Ana, San Miguel, La Libertad y Sonsonate.

## Integrantes

Marlon Moises Segovia Henriquez

## Archivos

| Archivo | Descripcion |
|---|---|
| `generar_datos.py` | Genera el inventario y lo guarda en `inventario.csv` |
| `datos.py` | Carga el CSV y agrega columnas calculadas |
| `inspeccion.py` | Inspeccion con Pandas (estructura, tipos y estadisticas) |
| `graficos.py` | Graficos de Matplotlib |
| `app.py` | Interfaz grafica en PyQt5 |
| `informe.py` | Genera `informe_consultoria.pdf` |
| `inventario.csv` | Datos del inventario |

## Uso

```bash
pip install -r requirements.txt
python generar_datos.py   # opcional, el CSV ya esta incluido
python inspeccion.py
python app.py
python informe.py
```
