# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'komiwojazer_qgis_dialog_base.ui'
#
# Created: Sat Apr 21 11:37:34 2018
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_KomiwojazerDialogBase(object):
    def setupUi(self, KomiwojazerDialogBase):
        KomiwojazerDialogBase.setObjectName(_fromUtf8("KomiwojazerDialogBase"))
        KomiwojazerDialogBase.resize(438, 518)
        self.button_box = QtGui.QDialogButtonBox(KomiwojazerDialogBase)
        self.button_box.setGeometry(QtCore.QRect(80, 470, 341, 32))
        self.button_box.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setCenterButtons(True)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.label = QtGui.QLabel(KomiwojazerDialogBase)
        self.label.setGeometry(QtCore.QRect(30, 20, 371, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName(_fromUtf8("label"))
        self.apiLabel = QtGui.QLabel(KomiwojazerDialogBase)
        self.apiLabel.setGeometry(QtCore.QRect(30, 370, 371, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.apiLabel.setFont(font)
        self.apiLabel.setAutoFillBackground(False)
        self.apiLabel.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.apiLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.apiLabel.setWordWrap(False)
        self.apiLabel.setObjectName(_fromUtf8("apiLabel"))
        self.mapLayerComboBox = QgsMapLayerComboBox(KomiwojazerDialogBase)
        self.mapLayerComboBox.setGeometry(QtCore.QRect(30, 60, 371, 27))
        self.mapLayerComboBox.setObjectName(_fromUtf8("mapLayerComboBox"))
        self.googleRadioButton = QtGui.QRadioButton(KomiwojazerDialogBase)
        self.googleRadioButton.setGeometry(QtCore.QRect(140, 290, 161, 17))
        self.googleRadioButton.setObjectName(_fromUtf8("googleRadioButton"))
        self.orsRadioButton = QtGui.QRadioButton(KomiwojazerDialogBase)
        self.orsRadioButton.setGeometry(QtCore.QRect(140, 320, 161, 17))
        self.orsRadioButton.setObjectName(_fromUtf8("orsRadioButton"))
        self.layoutWidget = QtGui.QWidget(KomiwojazerDialogBase)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 100, 371, 151))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.nameFieldLabel = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(10)
        self.nameFieldLabel.setFont(font)
        self.nameFieldLabel.setObjectName(_fromUtf8("nameFieldLabel"))
        self.gridLayout.addWidget(self.nameFieldLabel, 0, 0, 1, 1)
        self.fieldComboBox = QgsFieldComboBox(self.layoutWidget)
        self.fieldComboBox.setObjectName(_fromUtf8("fieldComboBox"))
        self.gridLayout.addWidget(self.fieldComboBox, 0, 1, 1, 1)
        self.routingModeLabel = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(10)
        self.routingModeLabel.setFont(font)
        self.routingModeLabel.setObjectName(_fromUtf8("routingModeLabel"))
        self.gridLayout.addWidget(self.routingModeLabel, 1, 0, 1, 1)
        self.routingModeComboBox = QtGui.QComboBox(self.layoutWidget)
        self.routingModeComboBox.setObjectName(_fromUtf8("routingModeComboBox"))
        self.gridLayout.addWidget(self.routingModeComboBox, 1, 1, 1, 1)
        self.travelModeLabel = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(10)
        self.travelModeLabel.setFont(font)
        self.travelModeLabel.setObjectName(_fromUtf8("travelModeLabel"))
        self.gridLayout.addWidget(self.travelModeLabel, 2, 0, 1, 1)
        self.travelModeComboBox = QtGui.QComboBox(self.layoutWidget)
        self.travelModeComboBox.setObjectName(_fromUtf8("travelModeComboBox"))
        self.gridLayout.addWidget(self.travelModeComboBox, 2, 1, 1, 1)
        self.apiTextEdit = QtGui.QLineEdit(KomiwojazerDialogBase)
        self.apiTextEdit.setGeometry(QtCore.QRect(30, 410, 371, 31))
        self.apiTextEdit.setObjectName(_fromUtf8("apiTextEdit"))
        self.label_2 = QtGui.QLabel(KomiwojazerDialogBase)
        self.label_2.setGeometry(QtCore.QRect(30, 390, 381, 21))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(KomiwojazerDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), KomiwojazerDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), KomiwojazerDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(KomiwojazerDialogBase)
        KomiwojazerDialogBase.setTabOrder(self.mapLayerComboBox, self.button_box)

    def retranslateUi(self, KomiwojazerDialogBase):
        KomiwojazerDialogBase.setWindowTitle(_translate("KomiwojazerDialogBase", "Travelling Salesman Problem (TSP)", None))
        self.label.setText(_translate("KomiwojazerDialogBase", "Select point layer ", None))
        self.apiLabel.setText(_translate("KomiwojazerDialogBase", "provide your API Key (optional):", None))
        self.googleRadioButton.setText(_translate("KomiwojazerDialogBase", "Google Maps API", None))
        self.orsRadioButton.setText(_translate("KomiwojazerDialogBase", "OpenRouteService API", None))
        self.nameFieldLabel.setText(_translate("KomiwojazerDialogBase", "Field with name", None))
        self.routingModeLabel.setText(_translate("KomiwojazerDialogBase", "Routing Mode", None))
        self.travelModeLabel.setText(_translate("KomiwojazerDialogBase", "Travel Mode", None))
        self.label_2.setText(_translate("KomiwojazerDialogBase", "For Google Maps you need \"distance matrix\" and \"directions\" API key", None))

from qgis.gui import QgsFieldComboBox, QgsMapLayerComboBox
