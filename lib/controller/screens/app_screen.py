import binascii

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QBoxLayout, QPushButton, QHBoxLayout, QFormLayout, QLabel, QFileDialog, \
    QGraphicsOpacityEffect, QMessageBox

from lib.controller import START_ADDRESS, END_ADDRESS
from lib.controller.pcan.PCANBasic import *
from lib.controller.screens import FILE_DATA_LEN, PORT_NOT_FOUND
from lib.controller.util.helper import setlogger, applog
from lib.controller.views.pages.home_screen import Ui_MainWindow

from intelhex import IntelHex
import numpy as np

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.bin_chunks = []

        self.pcan_port = None
        self.pcan_baudrate = PCAN_BAUD_250K
        self.pcan = None

        setlogger()
        self.set_actions()

        self.shortcut = QShortcut(QKeySequence("Ctrl+C"), self)
        self.shortcut.activated.connect(self.close)

        # self.enable_port_settings(False)
        # self.update_ports()

    def set_actions(self):
        self.ui.upload_btn.clicked.connect(self.browse_file)
        # self.ui.scan_port.clicked.connect(self.update_ports)
        # self.ui.connect_btn.clicked.connect(self.connect_port)
        self.ui.flash_btn.clicked.connect(self.start_flashing_bin_file)

        self.ui.port_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.scan_port.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.baud_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.connect_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.flash_btn.setCursor(Qt.CursorShape.PointingHandCursor)

    def browse_file(self):
        file_dialog = QFileDialog()
        filename = file_dialog.getOpenFileName(None, 'Open Bin File', '', "Hex files (*.hex)")
        ih = IntelHex(filename[0])

        ih.tobinfile("test.bin", start=0x2000, end=0xFFFFFF)
        bin_data = ih.tobinarray(start=0x2000, end=0xFFFFFF)

        self.bin_chunks = list(self.divide_chunks(bin_data, 8))
        applog(self.bin_chunks)

        applog("BIN CHUNks")

        for ele in self.bin_chunks:
            applog(ele)

    def start_flashing_bin_file(self):
        self.pcan_port = PCAN_USBBUS1
        self.pcan = PCANBasic()
        self.pcan_status = self.pcan.Initialize(self.pcan_port, self.pcan_baudrate)

        print("Status of Pcan bus ", self.pcan_status)
        print(TPCANStatus(self.pcan_status))
        print(hex(self.pcan_status))
        print(TPCANStatus(0x00200))
        if self.pcan_status == PCAN_ERROR_OK:
            print("connecting with PCAN Bus")
            self.read_pcan_message()
        if self.pcan_status == TPCANStatus(0x00200):
            print("Driver not loaded")

    def read_pcan_message(self):
        pckt = self.pcan.Read(self.pcan_port)
        print("pckt from the controller")
        print(pckt)
        print(pckt[0])
        print("hex ", hex(pckt[0]))
        print("STAtus ", TPCANStatus(pckt[0]))
        msg = pckt[1]
        print("msg from the controller")
        print("ID", msg.ID)
        print(np.ctypeslib.as_array(msg.DATA))
        print("MSGTYPE", msg.MSGTYPE)

        if(msg.MSGTYPE == PCAN_MESSAGE_STANDARD):
            print("STANDARD TYPE")
        print("LEN", msg.LEN)
        # TPCANMsg
        print("DATA")
        print(msg.DATA)

        print("**********************")
        print(msg.DATA[0])
        print(msg.DATA[1])
        print(msg.DATA[2])
        print(msg.DATA[3])
        print(msg.DATA[4])
        print(msg.DATA[5])
        print(msg.DATA[6])
        print(msg.DATA[7])





    def get_msg_template(self, msgtype):
        """
        Gets the string representation of the type of a CAN message

        Parameters:
            msgtype = Type of a CAN message

        Returns:
            The type of the CAN message as string
        """
        if (msgtype & PCAN_MESSAGE_STATUS.value) == PCAN_MESSAGE_STATUS.value:
            return 'STATUS'

        if (msgtype & PCAN_MESSAGE_ERRFRAME.value) == PCAN_MESSAGE_ERRFRAME.value:
            return 'ERROR'

        if (msgtype & PCAN_MESSAGE_EXTENDED.value) == PCAN_MESSAGE_EXTENDED.value:
            strTemp = 'EXT'
        else:
            strTemp = 'STD'

        if (msgtype & PCAN_MESSAGE_RTR.value) == PCAN_MESSAGE_RTR.value:
            strTemp += '/RTR'
        else:
            if (msgtype > PCAN_MESSAGE_EXTENDED.value):
                strTemp += ' ['
                if (msgtype & PCAN_MESSAGE_FD.value) == PCAN_MESSAGE_FD.value:
                    strTemp += ' FD'
                if (msgtype & PCAN_MESSAGE_BRS.value) == PCAN_MESSAGE_BRS.value:
                    strTemp += ' BRS'
                if (msgtype & PCAN_MESSAGE_ESI.value) == PCAN_MESSAGE_ESI.value:
                    strTemp += ' ESI'
                strTemp += ' ]'

        return strTemp




    def divide_chunks(self, dlist, n):
        # looping till length l
        for i in range(0, len(dlist), n):
            d = dlist[i:i + n]
            yield d


    def validate_port(self):
        if self.ui.port_combo.currentText() == "Select":
            self.set_status_msg("Select Valid Port", False)
            return False
        else:
            return True


    def enable_port_settings(self, state):
        self.ui.port_combo.setEnabled(state)
        self.ui.scan_port.setEnabled(state)
        self.ui.baud_combo.setEnabled(state)
        self.ui.connect_btn.setEnabled(state)

    def set_status_msg(self, msg, state):
        self.ui.con_status_msg.setText(msg)
        self.ui.con_status_msg.setStyleSheet("Color:green") if state else self.ui.con_status_msg.setStyleSheet(
            "Color:Red")

        self.unfade(self.ui.con_status_msg, 1000)
        self.fade(self.ui.con_status_msg, 1000)


    def enable_flash_btn(self, state):
        self.ui.flash_btn.setVisible(state)


    def update_ports(self):
        self.port_combo.clear()
        self.port_combo.addItem("Select")
        port_list = [ports.device for ports in serial.tools.list_ports.comports()]
        if port_list:
            self.port_combo.addItems(port_list)


    def divide_chunks(self, dlist, n):
        # looping till length l
        for i in range(0, len(dlist), n):
            d = dlist[i:i + n]
            yield d

    def fade(self, widget, duration):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(duration)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def unfade(self, widget, duration):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(duration)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()


    def showDialog(self, title, description):
        print("From show dialog")
        msgBox = QMessageBox()
        msgBox.setText(description)
        msgBox.setWindowTitle(title)
        msgBox.exec()
