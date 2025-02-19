import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import QtWidgets
from frontend import Ui_MainWindow  
import pandas as pd
import re

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

        # Habilita o grid nas direções X e Y
        plot_item.showGrid(x=True, y=True)

        # Define Titulos e cores dos eixos 
        self.plot_graph.setBackground('w')
        plot_item.setLabel('bottom', 'Tempo (min)', color='#151515')
        plot_item.getAxis('bottom').setTextPen('#151515')
        plot_item.getAxis('left').setTextPen('#151515')  

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
        valores_1 = []
        valores_2 = []
        valores_3 = []
        valores_4 = []
        valores_5 = []

        self.plot_graph.clear()

        for val in self.df[type_column]:

            val_split = val.split()

            # Compara o numero de elementos  
            if len(val_split) == 5:
                val1, val2, val3, val4, val5 = val_split
                valores_1.append(float(re.sub(r'[a-zA-Z]+', '', val1).strip()))
                valores_2.append(float(re.sub(r'[a-zA-Z]+', '', val2).strip()))
                valores_3.append(float(re.sub(r'[a-zA-Z]+', '', val3).strip()))
                valores_4.append(float(re.sub(r'[a-zA-Z]+', '', val4).strip()))
                valores_5.append(float(re.sub(r'[a-zA-Z]+', '', val5).strip()))
            elif len(val_split) == 3:
                val1, val2, val3 = val_split
                valores_1.append(float(re.sub(r'[a-zA-Z]+', '', val1).strip()))
                valores_2.append(float(re.sub(r'[a-zA-Z]+', '', val2).strip()))
                valores_3.append(float(re.sub(r'[a-zA-Z]+', '', val3).strip()))
            elif len(val_split) == 2:
                val1, val2 = val_split
                valores_1.append(float(re.sub(r'[a-zA-Z]+', '', val1).strip()))
                valores_2.append(float(re.sub(r'[a-zA-Z]+', '', val2).strip()))
            else:
                val1 = val_split
                valores_1.append(float(re.sub(r'[a-zA-Z]+', '', val1[0]).strip()))


        if len(val_split) == 5:
            max_geral = max(max(valores_1), max(valores_2), max(valores_3), max(valores_4), max(valores_5))
            min_geral = min(min(valores_1), min(valores_2), min(valores_3), min(valores_4), min(valores_5))
        elif len(val_split) == 3:
            max_geral = max(max(valores_1), max(valores_2), max(valores_3))
            min_geral = min(min(valores_1), min(valores_2), min(valores_3))
        elif len(val_split) == 2:
            max_geral = max(max(valores_1), max(valores_2))
            min_geral = min(min(valores_1), min(valores_2))
        else:
            max_geral = max(valores_1)
            min_geral = min(valores_1)

        ymax = (max_geral + (max_geral-min_geral)*2)
        ymin = (min_geral - (max_geral-min_geral)*2)

        if min_geral == 0.0:
            ymin = 0.0
            ymax = max_geral*1.5
            if max_geral == 0.0:
                ymin = - 1
                ymax = 1

        self.plot_graph.getViewBox().setLimits(yMin= ymin, yMax=ymax) 

        # Criar e adicionar as linhas ao gráfico utilizando setData
        if valores_5:
            linha1 = self.plot_graph.plot(pen='r', name='Bateria')  # Linha vermelha
            linha2 = self.plot_graph.plot(pen='g', name='PFC')  # Linha vermelha
            linha3 = self.plot_graph.plot(pen='b', name='Inversor')  # Linha vermelha
            linha4 = self.plot_graph.plot(pen='#9C00C3', name='Painel')  # Linha amarela
            linha5 = self.plot_graph.plot(pen='c', name='Interno')  # Linha azul
            linha1.setData(self.df['Hour_num'], valores_1)
            linha2.setData(self.df['Hour_num'], valores_2)
            linha3.setData(self.df['Hour_num'], valores_3)
            linha4.setData(self.df['Hour_num'], valores_4)
            linha5.setData(self.df['Hour_num'], valores_5)
            self.plot_graph.setTitle("Temperatura", color='#151515')
        elif valores_3:
            linha1 = self.plot_graph.plot(pen='r', name='Fase A')  # Linha vermelha
            linha2 = self.plot_graph.plot(pen='g', name='Fase B')  # Linha verde
            linha3 = self.plot_graph.plot(pen='b', name='Fase C')  # Linha azul
            linha1.setData(self.df['Hour_num'], valores_1)
            linha2.setData(self.df['Hour_num'], valores_2)
            linha3.setData(self.df['Hour_num'], valores_3)
            self.plot_graph.setTitle(type_column, color='#151515')
        elif valores_2:
            linha1 = self.plot_graph.plot(pen='r', name='Positivo')  # Linha vermelha
            linha2 = self.plot_graph.plot(pen='g', name='Negativo')  # Linha verde
            linha1.setData(self.df['Hour_num'], valores_1)
            linha2.setData(self.df['Hour_num'], valores_2)
            self.plot_graph.setTitle(type_column, color='#151515')
        else:
            linha1 = self.plot_graph.plot(pen='r')  # Linha vermelha
            linha1.setData(self.df['Hour_num'], valores_1)
            self.plot_graph.setTitle(type_column, color='#151515')
        
        self.plot_graph.setRange(xRange=(0, MAX_REGISTERS), yRange=(ymin, ymax))

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