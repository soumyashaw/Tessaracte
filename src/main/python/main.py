from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
import sys
#"\u00b2"
class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        overallLayout = QHBoxLayout(self)

        self.formulaDict = {}
        self.readFormulas()
        self.font2 = QFont()
        self.font2.setPointSize(11)        

        self.symbols = ['x', 'y', '7', '8', '9', 'DEL', 'C', 'sin', 'cos', '4', '5', '6', '/', '*', 'tan', '^', '1', '2', '3', '+', '-', 'exp', 'log', '.', '0', '=', '(', ')']
        self.buttons = {}
        self.inputBox = QGridLayout()
        self.equationListVbox = QVBoxLayout()
        self.equationListVbox2 = QVBoxLayout()
        
        self.equationList = QTabWidget()
        self.equationList.tab1 = QWidget()
        self.equationList.tab2 = QWidget()
        self.equationList.tab3 = QWidget()
        self.equationList.addTab(self.equationList.tab1, "Formula Book")
        self.equationList.addTab(self.equationList.tab2, "Favourites")
        self.equationList.addTab(self.equationList.tab3, "Usage")
        self.equationList.tab1.setLayout(self.formulaLayout())
        self.equationList.tab2.setLayout(self.historyLayout())
        self.equationList.setFixedWidth(300)
        self.equationList.setFixedHeight(550)       

        inputSpace = QTabWidget()
        inputSpace.tab1 = QWidget()
        inputSpace.tab2 = QWidget()
        
        inputSpace.addTab(inputSpace.tab1, "Input")
        inputSpace.addTab(inputSpace.tab2, "Usage")
        inputSpace.tab1.setLayout(self.inputsLayout())
        ##inputSpace.tab2.setLayout(preferenceLayout(self))
        inputSpace.tab1.setStatusTip("Input characters")
        inputSpace.setFixedHeight(200)

        buttonSpace = QWidget()
        buttonSpace.setLayout(self.buttonsLayout())
        buttonSpace.setFixedWidth(300)
        buttonSpace.setStatusTip("Interact")

        self.tabPlot = QTabWidget()
        self.tabPlot.tab1 = QWidget()
        self.tabPlot.tab2 = QWidget()
        self.tabPlot.addTab(self.tabPlot.tab1, "2D-plot")
        self.tabPlot.addTab(self.tabPlot.tab2, "Usage")
        ##self.tabPlot.tab1.setLayout(plotFigure2D(self))
        self.tabPlot.tab1.setStatusTip("Visualize equation in 2D")
        ##self.tabPlot.tab2.setLayout(plotFigure3D(self))
        self.tabPlot.tab2.setStatusTip("Usage of Plot")

        font = QFont()
        font.setPointSize(16)
        self.textedit = QTextEdit()
        self.textedit.setFont(font)
        self.textedit.setFixedHeight(60)
        self.textedit.setStatusTip("Input equation")

        quickSolve = QWidget()
        quickSolve.setLayout(self.qSolveAdapter())
        quickSolve.setFixedHeight(45)
        quickSolve.setStatusTip("Quick solver")

        splitter5 = QSplitter(Qt.Vertical)
        splitter5.addWidget(self.textedit)
        splitter5.addWidget(quickSolve)
        splitter5.addWidget(inputSpace)

        splitter4 = QSplitter(Qt.Vertical)
        splitter4.addWidget(buttonSpace)
        splitter4.addWidget(self.equationList)

        splitter3 = QSplitter(Qt.Horizontal)
        splitter3.addWidget(self.tabPlot)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter5)
        splitter2.addWidget(splitter3)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(splitter2)
        splitter1.addWidget(splitter4)

        overallLayout.addWidget(splitter1)
        self.setLayout(overallLayout)

        self.setWindowTitle("Tessaracte")
        self.changeStyle('Fusion')
        self.showMaximized()

    def formulaFormatter(self, formula):
        self.formatterDict = {'pi': chr(0x03C0), '^': ['<sup>', '</sup>'], '_': ['<sub>', '</sub>']}
        formulaList  = formula.split(' ')
        formulaListTemp = []
        formattedFormula = ''
        flag = 0
        for token in formulaList:
            if token == '^':
                formulaListTemp.append(self.formatterDict[token][0])
                flag = 1
            elif token == '_':
                formulaListTemp.append(self.formatterDict[token][0])
                flag = 2
            elif token in self.formatterDict.keys():
                formulaListTemp.append(self.formatterDict[token])
            elif flag == 1:
                formulaListTemp.append(token)
                formulaListTemp.append(self.formatterDict['^'][1])
                flag = 0
            elif flag == 2:
                formulaListTemp.append(token)
                formulaListTemp.append(self.formatterDict['_'][1])
                flag = 0
            else:
                formulaListTemp.append(token)

        for index in formulaListTemp:
            formattedFormula += index + ' '

        return formattedFormula

    def writeCSV(self):
        self.df.to_csv('F:\Tessaracte\src\main\python\database.csv', index=False)
        self.readFormulas()

    def readFormulas(self):
        self.df = pd.read_csv(r'F:\Tessaracte\src\main\python\database.csv')
        row = self.df.shape[0]
        col = self.df.shape[1]
        
        for i in range(row):
            value = []
            for j in range(1, col):
                value.append(self.df.iloc[i][j])
            self.formulaDict[self.df.iloc[i][0]] = value

    def addFormula(self):
        formula = self.updateFormula.toPlainText().split('|')
        print(formula)
        index = len(self.formulaDict) + 1000
        self.df.loc[len(self.df.index)] = [index, formula[0], formula[1], formula[2], 0]
        self.updateFormula.setText('')
        self.writeCSV()

    def searchFormula(self):
        indexList = []
        labelToSearch = self.updateFormula.toPlainText().strip(' ][')
        self.myQListWidget.clear()

        for i in range(len(self.formulaDict)):
            if labelToSearch in self.formulaDict[1000+i][2] and labelToSearch != '' and len(indexList)>0:
                indexList.append(1000 + i)
                self.df['freq'][i] += 1

        if labelToSearch == '':
            index = 1000
            for i in range(len(self.formulaDict)):
                myQCustomQWidget = QCustomQWidget()
                formulaDescription = str(self.formulaDict[index][1]).strip("][")
                formulaDisplay = str(self.formulaDict[index][0]).strip("][")
                myQCustomQWidget.setTextUp(formulaDescription)
                myQCustomQWidget.setTextDown(formulaDisplay)
                myQListWidgetItem = QListWidgetItem(self.myQListWidget)
                myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
                self.myQListWidget.addItem(myQListWidgetItem)
                self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
                index += 1

        elif len(indexList) == 0:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp('Formula/Consant Not Found')
            myQCustomQWidget.setTextDown('Check for Misspelt words')
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        else:
            index = 1000
            for i in range(len(self.formulaDict)):
                if index in indexList:
                    myQCustomQWidget = QCustomQWidget()
                    formulaDescription = str(self.formulaDict[index][1]).strip("][")
                    formulaDisplay = str(self.formulaDict[index][0]).strip("][")
                    myQCustomQWidget.setTextUp(formulaDescription)
                    myQCustomQWidget.setTextDown(formulaDisplay)
                    myQListWidgetItem = QListWidgetItem(self.myQListWidget)
                    myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
                    self.myQListWidget.addItem(myQListWidgetItem)
                    self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
                index += 1

        self.updateFormula.setText('')
        self.writeCSV()
        self.updateFavourites()

    def updateFavourites(self):
        self.myQListWidget2.clear()
        index = 1000
        for i in range(len(self.formulaDict)):
            if int(self.df['freq'][i]) >= 1:
                myQCustomQWidget = QCustomQWidget()
                formulaDescription = str(self.formulaDict[index][1]).strip("][")
                formulaDisplay = self.formulaFormatter(str(self.formulaDict[index][0]).strip("]["))
                myQCustomQWidget.setTextUp(formulaDescription)
                myQCustomQWidget.setTextDown(formulaDisplay)
                myQListWidgetItem = QListWidgetItem(self.myQListWidget2)
                myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
                self.myQListWidget2.addItem(myQListWidgetItem)
                self.myQListWidget2.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            index += 1

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))

    def formulaLayout(self):
        self.myQListWidget = QListWidget(self)
        index = 1000
        for i in range(len(self.formulaDict)):
            myQCustomQWidget = QCustomQWidget()
            formulaDescription = str(self.formulaDict[index][1]).strip("][")
            formulaDisplay = self.formulaFormatter(str(self.formulaDict[index][0]).strip("]["))
            myQCustomQWidget.setTextUp(formulaDescription)
            myQCustomQWidget.setTextDown(formulaDisplay)
            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            index += 1
        self.equationListVbox.addWidget(self.myQListWidget)
        #self.myQListWidget.itemClicked.connect(self.Clicked)
        self.updateFormula = QTextEdit()
        self.updateFormula.setFixedHeight(30)
        self.addFormulaButton = QPushButton('Add Formula')
        self.searchFormulaButton = QPushButton('Search Formula')
        self.addFormulaButton.clicked.connect(self.addFormula)
        self.searchFormulaButton.clicked.connect(self.searchFormula)
        #self.clearButton.clicked.connect(self.clearHistory)
        #self.clearButton.setStatusTip("Clear history")
        buttonSplitter = QSplitter(Qt.Horizontal)
        buttonSplitter.addWidget(self.addFormulaButton)
        buttonSplitter.addWidget(self.searchFormulaButton)
        self.equationListVbox.addWidget(self.updateFormula)
        self.equationListVbox.addWidget(buttonSplitter)
        return self.equationListVbox

    def historyLayout(self):
        self.myQListWidget2 = QListWidget(self)
        index = 1000
        for i in range(len(self.formulaDict)):
            if int(self.df['freq'][i]) >= 1:
                myQCustomQWidget = QCustomQWidget()
                formulaDescription = str(self.formulaDict[index][1]).strip("][")
                formulaDisplay = self.formulaFormatter(str(self.formulaDict[index][0]).strip("]["))
                myQCustomQWidget.setTextUp(formulaDescription)
                myQCustomQWidget.setTextDown(formulaDisplay)
                myQListWidgetItem = QListWidgetItem(self.myQListWidget)
                myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
                self.myQListWidget2.addItem(myQListWidgetItem)
                self.myQListWidget2.setItemWidget(myQListWidgetItem, myQCustomQWidget)
            index += 1
        self.equationListVbox2.addWidget(self.myQListWidget2)
        return self.equationListVbox2

    def inputsLayout(self):
        inputLayout = QHBoxLayout(self)
        inputWidget = QWidget()
        for i in range(4):
            for j in range(7):
                if (i * 7 + j) < len(self.symbols):
                    self.buttons[(i, j)] = QPushButton(self.symbols[i * 7 + j])
                    self.buttons[(i, j)].setFont(self.font2)
                    self.buttons[(i, j)].resize(100, 100)
                    self.buttons[(i, j)].clicked.connect(self.onInputPress(self.symbols[i * 7 + j]))
                    self.inputBox.addWidget(self.buttons[(i, j)], i, j)
        inputWidget.setLayout(self.inputBox)
        inputLayout.addWidget(inputWidget)
        return inputLayout

    def buttonsLayout(self):
        vbox = QVBoxLayout()
        interactionModeLayout = QVBoxLayout()
        self.interactionModeButton = QPushButton('Tessaracte')
        self.interactionModeButton.setFont(self.font2)
        self.interactionModeButton.clicked.connect(self.interactionMode)
        interactionModeLayout.addWidget(self.interactionModeButton)
        interactionModeWidget = QWidget(self)
        interactionModeWidget.setLayout(interactionModeLayout)
        interactionModeWidget.setFixedSize(275, 50)
        topButtonSplitter = QSplitter(Qt.Horizontal)
        topButtonSplitter.addWidget(interactionModeWidget)
        permanentButtons = QWidget(self)
        topButtonSplitter.addWidget(permanentButtons)
        self.bottomButton = QFrame()
        self.buttonSplitter = QSplitter(Qt.Vertical)
        self.buttonSplitter.addWidget(topButtonSplitter)
        self.buttonSplitter.addWidget(self.bottomButton)
        vbox.addWidget(self.buttonSplitter)
        return vbox

    def qSolveAdapter(self):
        eqFormatterLayout = QVBoxLayout()
        self.eqFormatterLabel = QLabel()
        font3 = QFont("Helvetica")
        font3.setPointSize(13)
        font3.setItalic(True)
        self.eqFormatterLabel.setFont(font3)
        # self.eqFormatterLabel.setText('Test')
        eqFormatterLayout.addWidget(self.eqFormatterLabel)
        return eqFormatterLayout

    def onInputPress(self, name):
        def calluser():
            if name == 'C':
                self.textedit.setText('')
            elif name == 'DEL':
                cursor = self.textedit.textCursor()
                cursor.deletePreviousChar()
            else:
                self.textedit.insertPlainText(str(name))
        return calluser

    def interactionMode(self):
        # Show buttons for solving
        equation = self.formulaFormatter(self.textedit.toPlainText())
        self.eqFormatterLabel.setText(equation)
        try:
            self.quadraticSolver(self.textedit.toPlainText())
        except:
            self.eqFormatterLabel.setText('Error in Input Equation')

    def quadraticSolver(self, equation):
        equation = equation.split(' ')
        a = float(equation[int(equation.index('^')-3)])
        b = float(equation[int(equation.index('^')+3)])
        c = float(equation[int(equation.index('^')+7)])
        d = b ** 2 - 4 * a * c
        if d >= 0:
            p = (-b + d ** 0.5) / 2 * a
            q = (-b - d ** 0.5) / 2 * a
            print("Roots are", p,'&', q)

        if d < 0:
            r1 = -b / (2 * a)
            i1 = d ** 0.5 / (2 * a)
            r2 = -b / (2 * a)
            i2 = d ** 0.5 / (2 * a)
            print("roots are", round(r1, 2) + i1, round(r2, 2) - i2)

class QCustomQWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.textQVBoxLayout = QVBoxLayout()
        self.textUpQLabel = QLabel()
        self.textDownQLabel = QLabel()
        font2 = QFont()
        font2.setPointSize(12)
        self.textUpQLabel.setFont(font2)
        self.textDownQLabel.setFont(font2)
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QHBoxLayout()
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        self.textUpQLabel.setStyleSheet('''color: blue;''')
        self.textDownQLabel.setStyleSheet('''color: black;''')

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

if __name__ == '__main__':
    appctxt = QApplication([])       # 1. Instantiate ApplicationContext
    appctxt.setWindowIcon(QIcon('Icon.ico'))
    gallery = WidgetGallery()
    gallery.show()
    exit_code = appctxt.exec_()      # 2. Invoke appctxt.exec_()
    sys.exit(exit_code)
