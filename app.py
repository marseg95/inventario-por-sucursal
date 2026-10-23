import sys
import os

os.environ.setdefault("QT_QPA_PLATFORM", "wayland")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
)

from datos import cargar_inventario
from graficos import GRAFICOS


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventario por sucursal")
        self.resize(900, 600)

        self.df = cargar_inventario()

        pestanas = QTabWidget()
        pestanas.addTab(self.crear_tabla(), "Inventario")
        for nombre, funcion in GRAFICOS.items():
            pestanas.addTab(self.crear_grafico(funcion), nombre)
        self.setCentralWidget(pestanas)

    def crear_tabla(self):
        tabla = QTableWidget(len(self.df), len(self.df.columns))
        tabla.setHorizontalHeaderLabels(self.df.columns)
        for fila, registro in enumerate(self.df.itertuples(index=False)):
            for columna, valor in enumerate(registro):
                tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))
        tabla.resizeColumnsToContents()
        return tabla

    def crear_grafico(self, funcion):
        figura = Figure(tight_layout=True)
        funcion(figura.add_subplot(111), self.df)
        return FigureCanvas(figura)


if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(aplicacion.exec_())
