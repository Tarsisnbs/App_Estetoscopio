# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1227, 680)
        MainWindow.setCursor(QCursor(Qt.ArrowCursor))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        MainWindow.setIconSize(QSize(100, 100))
        MainWindow.setToolButtonStyle(Qt.ToolButtonIconOnly)
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOriginal_Sound = QAction(MainWindow)
        self.actionOriginal_Sound.setObjectName(u"actionOriginal_Sound")
        self.actionFiltered_Sound = QAction(MainWindow)
        self.actionFiltered_Sound.setObjectName(u"actionFiltered_Sound")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_6 = QGridLayout(self.centralwidget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.ch2 = QGroupBox(self.centralwidget)
        self.ch2.setObjectName(u"ch2")
        self.gridLayout = QGridLayout(self.ch2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 3, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 0, 2, 1)

        self.horizontalSpacer = QSpacerItem(728, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 1, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.gridLayout.addLayout(self.verticalLayout_2, 0, 2, 1, 1)


        self.gridLayout_6.addWidget(self.ch2, 3, 0, 1, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"\n"
"background-color: rgb(255, 255, 255);")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.recButton = QPushButton(self.groupBox)
        self.recButton.setObjectName(u"recButton")
        self.recButton.setEnabled(True)

        self.gridLayout_2.addWidget(self.recButton, 0, 0, 1, 1)

        self.pauseButton = QPushButton(self.groupBox)
        self.pauseButton.setObjectName(u"pauseButton")

        self.gridLayout_2.addWidget(self.pauseButton, 0, 3, 1, 1)

        self.playButton = QPushButton(self.groupBox)
        self.playButton.setObjectName(u"playButton")

        self.gridLayout_2.addWidget(self.playButton, 0, 1, 1, 1)

        self.stopButton = QPushButton(self.groupBox)
        self.stopButton.setObjectName(u"stopButton")

        self.gridLayout_2.addWidget(self.stopButton, 0, 2, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox, 1, 0, 1, 1)

        self.adv_pars_Box = QGroupBox(self.centralwidget)
        self.adv_pars_Box.setObjectName(u"adv_pars_Box")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.adv_pars_Box.sizePolicy().hasHeightForWidth())
        self.adv_pars_Box.setSizePolicy(sizePolicy)
        self.gridLayout_7 = QGridLayout(self.adv_pars_Box)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.groupBoxPA = QGroupBox(self.adv_pars_Box)
        self.groupBoxPA.setObjectName(u"groupBoxPA")
        self.gridLayout_9 = QGridLayout(self.groupBoxPA)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.label_21 = QLabel(self.groupBoxPA)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_9.addWidget(self.label_21, 0, 0, 1, 1)

        self.comboBox_tipoPA = QComboBox(self.groupBoxPA)
        self.comboBox_tipoPA.addItem("")
        self.comboBox_tipoPA.addItem("")
        self.comboBox_tipoPA.addItem("")
        self.comboBox_tipoPA.addItem("")
        self.comboBox_tipoPA.addItem("")
        self.comboBox_tipoPA.setObjectName(u"comboBox_tipoPA")

        self.gridLayout_9.addWidget(self.comboBox_tipoPA, 0, 1, 1, 2)

        self.label_23 = QLabel(self.groupBoxPA)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_9.addWidget(self.label_23, 1, 0, 1, 1)

        self.ordem_PA = QSpinBox(self.groupBoxPA)
        self.ordem_PA.setObjectName(u"ordem_PA")
        self.ordem_PA.setValue(4)

        self.gridLayout_9.addWidget(self.ordem_PA, 1, 1, 1, 1)

        self.label_22 = QLabel(self.groupBoxPA)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_9.addWidget(self.label_22, 2, 0, 1, 1)

        self.slider_rp_PA = QSlider(self.groupBoxPA)
        self.slider_rp_PA.setObjectName(u"slider_rp_PA")
        self.slider_rp_PA.setSliderPosition(3)
        self.slider_rp_PA.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.slider_rp_PA, 2, 1, 1, 1)

        self.lcd_rp_PA = QLCDNumber(self.groupBoxPA)
        self.lcd_rp_PA.setObjectName(u"lcd_rp_PA")
        self.lcd_rp_PA.setProperty("intValue", 3)

        self.gridLayout_9.addWidget(self.lcd_rp_PA, 2, 2, 1, 1)

        self.label_20 = QLabel(self.groupBoxPA)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_9.addWidget(self.label_20, 3, 0, 1, 1)

        self.slider_rs_PA = QSlider(self.groupBoxPA)
        self.slider_rs_PA.setObjectName(u"slider_rs_PA")
        self.slider_rs_PA.setSliderPosition(40)
        self.slider_rs_PA.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.slider_rs_PA, 3, 1, 1, 1)

        self.lcd_rs_PA = QLCDNumber(self.groupBoxPA)
        self.lcd_rs_PA.setObjectName(u"lcd_rs_PA")
        self.lcd_rs_PA.setProperty("intValue", 40)

        self.gridLayout_9.addWidget(self.lcd_rs_PA, 3, 2, 1, 1)


        self.gridLayout_7.addWidget(self.groupBoxPA, 1, 0, 1, 1)

        self.groupBoxNT = QGroupBox(self.adv_pars_Box)
        self.groupBoxNT.setObjectName(u"groupBoxNT")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBoxNT.sizePolicy().hasHeightForWidth())
        self.groupBoxNT.setSizePolicy(sizePolicy1)
        self.groupBoxNT.setMaximumSize(QSize(110, 16777215))
        self.gridLayout_8 = QGridLayout(self.groupBoxNT)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_16 = QLabel(self.groupBoxNT)
        self.label_16.setObjectName(u"label_16")
        sizePolicy1.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.label_16, 1, 1, 1, 1)

        self.q_NT = QSpinBox(self.groupBoxNT)
        self.q_NT.setObjectName(u"q_NT")

        self.gridLayout_8.addWidget(self.q_NT, 1, 2, 1, 1)


        self.gridLayout_7.addWidget(self.groupBoxNT, 2, 0, 1, 1, Qt.AlignHCenter)

        self.pushButton = QPushButton(self.adv_pars_Box)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_7.addWidget(self.pushButton, 4, 0, 1, 1)

        self.refreshButton = QPushButton(self.adv_pars_Box)
        self.refreshButton.setObjectName(u"refreshButton")

        self.gridLayout_7.addWidget(self.refreshButton, 5, 0, 1, 1)

        self.groupBoxPB = QGroupBox(self.adv_pars_Box)
        self.groupBoxPB.setObjectName(u"groupBoxPB")
        self.gridLayout_10 = QGridLayout(self.groupBoxPB)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_12 = QLabel(self.groupBoxPB)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_10.addWidget(self.label_12, 0, 0, 1, 1)

        self.comboBox_tipoPB = QComboBox(self.groupBoxPB)
        self.comboBox_tipoPB.addItem("")
        self.comboBox_tipoPB.addItem("")
        self.comboBox_tipoPB.addItem("")
        self.comboBox_tipoPB.addItem("")
        self.comboBox_tipoPB.addItem("")
        self.comboBox_tipoPB.setObjectName(u"comboBox_tipoPB")

        self.gridLayout_10.addWidget(self.comboBox_tipoPB, 0, 1, 1, 2)

        self.label_11 = QLabel(self.groupBoxPB)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_10.addWidget(self.label_11, 1, 0, 1, 1)

        self.ordem_PB = QSpinBox(self.groupBoxPB)
        self.ordem_PB.setObjectName(u"ordem_PB")
        self.ordem_PB.setValue(4)

        self.gridLayout_10.addWidget(self.ordem_PB, 1, 1, 1, 1)

        self.label_14 = QLabel(self.groupBoxPB)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_10.addWidget(self.label_14, 2, 0, 1, 1)

        self.slider_rp_PB = QSlider(self.groupBoxPB)
        self.slider_rp_PB.setObjectName(u"slider_rp_PB")
        self.slider_rp_PB.setValue(3)
        self.slider_rp_PB.setOrientation(Qt.Horizontal)

        self.gridLayout_10.addWidget(self.slider_rp_PB, 2, 1, 1, 1)

        self.lcd_rp_PB = QLCDNumber(self.groupBoxPB)
        self.lcd_rp_PB.setObjectName(u"lcd_rp_PB")
        self.lcd_rp_PB.setProperty("intValue", 3)

        self.gridLayout_10.addWidget(self.lcd_rp_PB, 2, 2, 1, 1)

        self.label_15 = QLabel(self.groupBoxPB)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_10.addWidget(self.label_15, 3, 0, 1, 1)

        self.slider_rs_PB = QSlider(self.groupBoxPB)
        self.slider_rs_PB.setObjectName(u"slider_rs_PB")
        self.slider_rs_PB.setSliderPosition(40)
        self.slider_rs_PB.setOrientation(Qt.Horizontal)

        self.gridLayout_10.addWidget(self.slider_rs_PB, 3, 1, 1, 1)

        self.lcd_rs_PB = QLCDNumber(self.groupBoxPB)
        self.lcd_rs_PB.setObjectName(u"lcd_rs_PB")
        self.lcd_rs_PB.setSmallDecimalPoint(False)
        self.lcd_rs_PB.setProperty("intValue", 40)

        self.gridLayout_10.addWidget(self.lcd_rs_PB, 3, 2, 1, 1)


        self.gridLayout_7.addWidget(self.groupBoxPB, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.adv_pars_Box)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_5 = QGroupBox(self.groupBox_3)
        self.groupBox_5.setObjectName(u"groupBox_5")

        self.verticalLayout_3.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.groupBox_3)
        self.groupBox_6.setObjectName(u"groupBox_6")

        self.verticalLayout_3.addWidget(self.groupBox_6)

        self.groupBox_4 = QGroupBox(self.groupBox_3)
        self.groupBox_4.setObjectName(u"groupBox_4")

        self.verticalLayout_3.addWidget(self.groupBox_4)


        self.verticalLayout.addLayout(self.verticalLayout_3)


        self.gridLayout_7.addWidget(self.groupBox_3, 0, 1, 3, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_7.addItem(self.verticalSpacer_5, 3, 0, 1, 1)


        self.gridLayout_6.addWidget(self.adv_pars_Box, 1, 1, 4, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"")
        self.groupBox_2.setCheckable(True)
        self.groupBox_2.setChecked(True)
        self.gridLayout_5 = QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.freqtime_toggButon = QPushButton(self.groupBox_2)
        self.freqtime_toggButon.setObjectName(u"freqtime_toggButon")
        self.freqtime_toggButon.setCheckable(True)

        self.gridLayout_5.addWidget(self.freqtime_toggButon, 0, 1, 1, 1)

        self.clearButton = QPushButton(self.groupBox_2)
        self.clearButton.setObjectName(u"clearButton")

        self.gridLayout_5.addWidget(self.clearButton, 0, 2, 1, 1)

        self.adv_pars_Buton = QPushButton(self.groupBox_2)
        self.adv_pars_Buton.setObjectName(u"adv_pars_Buton")
        self.adv_pars_Buton.setEnabled(True)
        self.adv_pars_Buton.setAutoFillBackground(False)
        self.adv_pars_Buton.setCheckable(True)

        self.gridLayout_5.addWidget(self.adv_pars_Buton, 0, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.sliderPA = QSlider(self.groupBox_2)
        self.sliderPA.setObjectName(u"sliderPA")
        self.sliderPA.setMinimum(1)
        self.sliderPA.setMaximum(1000)
        self.sliderPA.setSliderPosition(100)
        self.sliderPA.setOrientation(Qt.Horizontal)
        self.sliderPA.setTickPosition(QSlider.TicksAbove)

        self.gridLayout_4.addWidget(self.sliderPA, 2, 1, 1, 1)

        self.sliderNT = QSlider(self.groupBox_2)
        self.sliderNT.setObjectName(u"sliderNT")
        self.sliderNT.setStyleSheet(u"color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.sliderNT.setMinimum(1)
        self.sliderNT.setMaximum(100)
        self.sliderNT.setSliderPosition(60)
        self.sliderNT.setOrientation(Qt.Horizontal)
        self.sliderNT.setInvertedAppearance(False)
        self.sliderNT.setInvertedControls(False)
        self.sliderNT.setTickPosition(QSlider.TicksAbove)

        self.gridLayout_4.addWidget(self.sliderNT, 5, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 5, 0, 1, 1)

        self.lab_PB = QLabel(self.groupBox_2)
        self.lab_PB.setObjectName(u"lab_PB")

        self.gridLayout_4.addWidget(self.lab_PB, 1, 2, 1, 1)

        self.sliderPB = QSlider(self.groupBox_2)
        self.sliderPB.setObjectName(u"sliderPB")
        self.sliderPB.setMinimum(1)
        self.sliderPB.setMaximum(1000)
        self.sliderPB.setSliderPosition(100)
        self.sliderPB.setOrientation(Qt.Horizontal)
        self.sliderPB.setTickPosition(QSlider.TicksAbove)
        self.sliderPB.setTickInterval(10)

        self.gridLayout_4.addWidget(self.sliderPB, 1, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 2, 0, 1, 1)

        self.lab_NT = QLabel(self.groupBox_2)
        self.lab_NT.setObjectName(u"lab_NT")

        self.gridLayout_4.addWidget(self.lab_NT, 5, 2, 1, 1)

        self.lab_PA = QLabel(self.groupBox_2)
        self.lab_PA.setObjectName(u"lab_PA")

        self.gridLayout_4.addWidget(self.lab_PA, 2, 2, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_4, 2, 0, 1, 4)

        self.exitButton = QPushButton(self.groupBox_2)
        self.exitButton.setObjectName(u"exitButton")

        self.gridLayout_5.addWidget(self.exitButton, 0, 3, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox_2, 4, 0, 1, 1)

        self.ch1 = QGroupBox(self.centralwidget)
        self.ch1.setObjectName(u"ch1")
        self.ch1.setAutoFillBackground(False)
        self.gridLayout_3 = QGridLayout(self.ch1)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(728, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 2, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_4, 0, 0, 2, 1)


        self.gridLayout_6.addWidget(self.ch1, 2, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.adv_pars_Box.raise_()
        self.groupBox.raise_()
        self.label.raise_()
        self.groupBox_2.raise_()
        self.ch1.raise_()
        self.ch2.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1227, 25))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSave = QMenu(self.menuFile)
        self.menuSave.setObjectName(u"menuSave")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuSave.menuAction())
        self.menuSave.addAction(self.actionOriginal_Sound)
        self.menuSave.addAction(self.actionFiltered_Sound)

        self.retranslateUi(MainWindow)
        self.slider_rp_PB.valueChanged.connect(self.lcd_rp_PB.display)
        self.slider_rs_PB.valueChanged.connect(self.lcd_rs_PB.display)
        self.sliderPB.sliderMoved.connect(self.lab_PB.setNum)
        self.sliderNT.sliderMoved.connect(self.lab_NT.setNum)
        self.slider_rs_PA.valueChanged.connect(self.lcd_rs_PA.display)
        self.slider_rp_PA.sliderMoved.connect(self.lab_PA.setNum)
        self.slider_rp_PA.valueChanged.connect(self.lcd_rp_PA.display)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionOriginal_Sound.setText(QCoreApplication.translate("MainWindow", u"Original Sound", None))
        self.actionFiltered_Sound.setText(QCoreApplication.translate("MainWindow", u"Filtered Sound", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.recButton.setText(QCoreApplication.translate("MainWindow", u"REC", None))
        self.pauseButton.setText(QCoreApplication.translate("MainWindow", u"PAUSE", None))
        self.playButton.setText(QCoreApplication.translate("MainWindow", u"PLAY", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.adv_pars_Box.setTitle(QCoreApplication.translate("MainWindow", u"Par\u00e2metros Avan\u00e7ados", None))
        self.groupBoxPA.setTitle(QCoreApplication.translate("MainWindow", u"Filtro Passa Altas", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Tipo", None))
        self.comboBox_tipoPA.setItemText(0, QCoreApplication.translate("MainWindow", u"Butterworth", None))
        self.comboBox_tipoPA.setItemText(1, QCoreApplication.translate("MainWindow", u"Bessel", None))
        self.comboBox_tipoPA.setItemText(2, QCoreApplication.translate("MainWindow", u"Chebyshev I", None))
        self.comboBox_tipoPA.setItemText(3, QCoreApplication.translate("MainWindow", u"Chebyshev II", None))
        self.comboBox_tipoPA.setItemText(4, QCoreApplication.translate("MainWindow", u"El\u00edptico", None))

        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Ordem", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"RP[db]", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"RS[db]", None))
        self.groupBoxNT.setTitle(QCoreApplication.translate("MainWindow", u"Filtro Notch", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"      Q", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"DEFAUT PARS", None))
        self.refreshButton.setText(QCoreApplication.translate("MainWindow", u"REFRESH", None))
        self.groupBoxPB.setTitle(QCoreApplication.translate("MainWindow", u"Filtro Passa Baixas", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Tipo", None))
        self.comboBox_tipoPB.setItemText(0, QCoreApplication.translate("MainWindow", u"Butterworth", None))
        self.comboBox_tipoPB.setItemText(1, QCoreApplication.translate("MainWindow", u"Bessel", None))
        self.comboBox_tipoPB.setItemText(2, QCoreApplication.translate("MainWindow", u"Chebyshev I", None))
        self.comboBox_tipoPB.setItemText(3, QCoreApplication.translate("MainWindow", u"Chebyshev II", None))
        self.comboBox_tipoPB.setItemText(4, QCoreApplication.translate("MainWindow", u"El\u00edptico", None))

        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Ordem", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"RP[db]", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"RS[db]", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.freqtime_toggButon.setText(QCoreApplication.translate("MainWindow", u"Dom\u00ednio da Frequ\u00eancia", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"CLEAR", None))
        self.adv_pars_Buton.setText(QCoreApplication.translate("MainWindow", u"PAR\u00c2METROS AVAN\u00c7ADOS", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"PB", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"NT", None))
        self.lab_PB.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"PA", None))
        self.lab_NT.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.lab_PA.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.exitButton.setText(QCoreApplication.translate("MainWindow", u"EXIT", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Ajuste de Banda:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Electronic Stethoscope - CST em Eletr\u00f4nica Industrial CTISM/UFSM</span></p></body></html>", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSave.setTitle(QCoreApplication.translate("MainWindow", u"Save ", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

