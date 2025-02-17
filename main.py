import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtWidgets
from frontend import Ui_MainWindow  
import pandas as pd

MAX = 1
MIN = 0
MAX_REGISTERS = (60*60*24)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect buttons or elements
        self.pushButtonLoadArchive.clicked.connect(self.on_pushButtonLoadArchive_click)

        self.pushButtonGridFreq.clicked.connect(self.on_pushButtonGridFreq_click)
        self.pushButtonGridVoltage.clicked.connect(self.on_pushButtonGridVoltage_click)
        self.pushButtonGridMaxVoltage.clicked.connect(self.on_pushButtonGridMaxVoltage_click)
        self.pushButtonGridMinVoltage.clicked.connect(self.on_pushButtonGridMinVoltage_click)
        self.pushButtonGridActivePower.clicked.connect(self.on_pushButtonGridActivePower_click)
        self.pushButtonGridReactivePower.clicked.connect(self.on_pushButtonGridReactivePower_click)

        self.pushButtonOtherTemp.clicked.connect(self.on_pushButtonOtherTemp_click)
        self.pushButtonOtherHumidity.clicked.connect(self.on_pushButtonOtherHumidity_click)

        self.plot_graph = pg.PlotWidget() 
        self.plot_graph.addLegend()

        self.setWindowTitle('Logs Reader')


    def on_pushButtonLoadArchive_click(self):

        # Load CSV Data
        if not self.load_data():
            return

        # Add graphs to QGraphicsView
        self.graphWidget.setLayout(QtWidgets.QVBoxLayout()) 
        self.graphWidget.layout().addWidget(self.plot_graph)

        self.plot_graph.getViewBox().setLimits(xMin=0, xMax=MAX_REGISTERS)

        plot_item = self.plot_graph.getPlotItem()

        # Signar of zoom change
        self.plot_graph.sigRangeChanged.connect(self.update_graph)

    def on_pushButtonGridFreq_click(self):
        self.fill_graph('Frequency')
        self.plot_graph.getPlotItem().setLabel('left', 'Frequency (Hz)')

    def on_pushButtonGridVoltage_click(self):
        self.fill_graph('Voltage')

    def on_pushButtonGridMaxVoltage_click(self):
        self.fill_graph('Maximum Voltage')

    def on_pushButtonGridMinVoltage_click(self):
        self.fill_graph('Minimum Voltage')

    def on_pushButtonGridActivePower_click(self):
        self.fill_graph('Active Power')

    def on_pushButtonGridReactivePower_click(self):
        self.fill_graph('Reactive Power')

    def on_pushButtonOtherTemp_click(self):
        self.fill_graph('Temperature')

    def on_pushButtonOtherHumidity_click(self):
        self.fill_graph('Voltage Humidity ')


    def fill_graph(self, type_column):
        test = 0

    def load_data(self):

        options = QFileDialog.Options()

        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Todos os Arquivos (*)", options=options)
        
        if not file_path:
            return False

        try:
            # Using pandas to read .csv
            self.df = pd.read_csv(file_path)

            # Extract data/hour values
            self.df['Hour'] = self.df['Date/Hour'].str.extract(r'(\d{2}:\d{2}:\d{2})')
        except:
            self.textBrowser.setText("Arquivo Incompatível!")
            self.groupBoxGrid.setEnabled(False)
            self.groupBoxOther.setEnabled(False)     
            return False
            
        self.textBrowser.setText(file_path.split('/')[-1])

        # Get column 'Hour'
        self.df['Hour'] = pd.to_datetime(self.df['Hour'], format='%H:%M:%S').dt.time

        # Convert to datetime
        self.df['Hour_num'] = self.df['Hour'].apply(lambda x: x.hour * 3600 + x.minute * 60 + x.second)

        self.groupBoxGrid.setEnabled(True)
        self.groupBoxOther.setEnabled(True)
        self.graphWidget.setEnabled(True)
        return True

    def update_graph(self):
        interval = 3600
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())