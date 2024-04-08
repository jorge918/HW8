import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from Rankine_GUI import Ui_Form
from Rankine_Classes_MVC import rankineController
from UnitConversions import UnitConverter as UC
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        """
        MainWindow constructor
        """
        super().__init__()
        self.setupUi(self)
        self.AssignSlots()
        self.MakeCanvas()

        self.input_widgets = [self.rb_SI, self.le_PHigh, self.le_PLow, self.le_TurbineInletCondition, self.rdo_Quality, self.le_TurbineEff, self.cmb_XAxis, self.cmb_YAxis, self.chk_logX, self.chk_logY]
        self.display_widgets = [self.lbl_PHigh, self.lbl_PLow, self.lbl_SatPropLow, self.lbl_SatPropHigh, self.lbl_TurbineInletCondition, self.lbl_H1, self.lbl_H1Units, self.lbl_H2, self.lbl_H2Units, self.lbl_H3, self.lbl_H3Units, self.lbl_H4, self.lbl_H4Units, self.lbl_TurbineWork, self.lbl_TurbineWorkUnits, self.lbl_PumpWork, self.lbl_PumpWorkUnits, self.lbl_HeatAdded, self.lbl_HeatAddedUnits, self.lbl_ThermalEfficiency, self.canvas, self.figure, self.ax]

        # Instantiate rankineController and pass input/display widgets
        self.RC = rankineController(self.input_widgets, self.display_widgets)

        self.setNewPHigh()
        self.setNewPLow()
        self.Calculate()

        self.oldXData = 0.0
        self.oldYData = 0.0
        self.show()

    def AssignSlots(self):
        """
        Setup signals and slots for my program
        """
        self.btn_Calculate.clicked.connect(self.Calculate)
        self.rdo_Quality.clicked.connect(self.SelectQualityOrTHigh)
        self.rdo_THigh.clicked.connect(self.SelectQualityOrTHigh)
        self.le_PHigh.editingFinished.connect(self.setNewPHigh)
        self.le_PLow.editingFinished.connect(self.setNewPLow)
        self.rb_SI.clicked.connect(self.SetUnits)
        self.rb_English.clicked.connect(self.SetUnits)
        self.cmb_XAxis.currentIndexChanged.connect(self.SetPlotVariables)
        self.cmb_YAxis.currentIndexChanged.connect(self.SetPlotVariables)
        self.chk_logX.toggled.connect(self.SetPlotVariables)
        self.chk_logY.toggled.connect(self.SetPlotVariables)

    def MakeCanvas(self):
        """
        Create a place to make graph of Rankine cycle
        """
        self.figure = Figure(figsize=(1, 1), tight_layout=True, frameon=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot()
        self.Layout_Plot.addWidget(NavigationToolbar2QT(self.canvas, self))
        self.Layout_Plot.addWidget(self.canvas)
        self.canvas.mpl_connect("motion_notify_event", self.mouseMoveEvent_Canvas)

    def mouseMoveEvent_Canvas(self, event):
        """
        Event handler for mouse movement on the graph canvas
        """
        self.oldXData = event.xdata if event.xdata is not None else self.oldXData
        self.oldYData = event.ydata if event.ydata is not None else self.oldYData
        sUnit = 'kJ/(kg*K)' if self.rb_SI.isChecked() else 'BTU/(lb*R)'
        TUnit = 'C' if self.rb_SI.isChecked() else 'F'
        self.setWindowTitle('s:{:0.2f} {}, T:{:0.2f} {}'.format(self.oldXData, sUnit, self.oldYData, TUnit))

    def Calculate(self):
        """
        Calculate method - calls updateModel() of the controller
        """
        self.RC.updateModel()

    def SelectQualityOrTHigh(self):
        """
        Method to handle radio button selection
        """
        self.RC.selectQualityOrTHigh()

    def SetPlotVariables(self):
        """
        Method to handle changes in plot variables
        """
        self.RC.updatePlot()

    def SetUnits(self):
        """
        Method to handle unit changes
        """
        self.RC.updateUnits()

    def setNewPHigh(self):
        """
        Method to handle changes in PHigh
        """
        self.RC.setNewPHigh()

    def setNewPLow(self):
        """
        Method to handle changes in PLow
        """
        self.RC.setNewPLow()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Rankine calculator')
    sys.exit(app.exec())
