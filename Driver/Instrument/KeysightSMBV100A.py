########################################################################################################
#######################                                                #################################
####################### AUTHOR: xiaoge                                 #################################
####################### EMAIL: salvadorjmegias@gmail.com               #################################
####################### UNIVERSITY EMAIL: salvadorjesus@correo.ugr.es  #################################
#######################                                                #################################
########################################################################################################

# Librerías o Modulos necesarios a importar
from robot.api.deco import keyword
import pyvisa as visa
import numpy as np
from struct import unpack
import time
from matplotlib import pyplot as plot


class KeysightSMBV100A:
    mIDN = "*IDN?\n"  # *查询ID
    mDefault = "SOUR:PRES\n"  # 恢复默认设置 * /
    mCmd_CLS = "*CLS\n"  # 清除设置 * /
    mCmd_ERR = "SYST:ERR:COUN?\n"  # 查询错误 * /
    mCmd_SelFile = "SOURce1:BB:ARB:WAV:SEL '/var/user/fsk9600_nsf0_12cc_len250.wv'\n"  # 选择信号源中的波形文件
    mCmd_ImpFile = "SOURce1:BB:ARB:WAV:SEL '/var/user/fsk9600_nsf0_12cc_len250.wv'\n"
    mCmd_AUTO = "SOURce1:BB:ARB:TRIG:SEQ AUTO\n"  # *设置为AUTO * /
    mCmd_TraSingle = "SOURce1:BB:ARB:SEQ SING\n"  # BB:ARB:TRIG:SEQ SINGLE
    mExecTrig = "SOURce1:BB:ARB:TRIG:EXEC\n"

    mCmd_RF_ON = "OUTP ON\n"  # 打开RF输出 * /
    mCmd_RF_OFF = "OUTP OFF\n"  # 关闭RF输出 * /
    mCmd_FREQ = "FREQ 490.11MHz\n"  # 设置频率 * /
    mCmd_POWLEV = "SOUR:POW:LEV:IMM:AMPL -116.3\n"  # 设置能级 * /
    mCmd_ARB_ON = "SOUR:BB:ARB:STATE ON\n"  # 使能ARB模式 * /
    mCmd_ARB_OFF = "SOUR:BB:ARB:STATE OFF\n"  # 关闭ARB模式 * /
    mBCmd_STATUS = "BB:ARB:TRIG:RMOD?\n"  # 查询运行状态 * /

    mCmd_PEP = "POW:PEP?\n"
    mCmd_LEVEL = "POW:LEVEL?\n"
    mCmd_MOD_OFF = "SOUR:MOD:STATE OFF\n"  # 关闭MOD，单音信号 * /

    def __init__(self, powLev=-90.0):
        self.powLev = powLev
        self.scope = self.setup()
        print(self.scope)

    def setup(self):
        # 192.168.2.5 IP keysight MACHINE
        rm = visa.ResourceManager('@py')  # Calling PyVisaPy library
        scope = rm.open_resource('TCPIP::192.168.3.105::INSTR')  # Connecting via LAN
        return scope

    def setFreq(self, centralFreq):  # 仪器频率设置命令
        self.centralFreq = "FREQ " + str(centralFreq) + "MHz" + "\n"
        self.scope.write(self.centralFreq)

    def setPowLev(self, Level):  # 仪器能级设置  sets the RF level at output A to Level dBm.
        self.powLev = "SOUR:POW:LEV:IMM:AMPL " + str(Level) + "\n"
        self.scope.write(self.powLev)
        time.sleep(0.1)
        # self.scope.write(self.mCmd_MOD_OFF)
        # time.sleep(0.1)
        # self.scope.write(self.mCmd_RF_ON)
        # time.sleep(0.1)

    def setIqWv(self, file):
        # 加载IQ数据文件
        self.mCmd_ImpFile = "BB:ARB:WAV:SEL " + file + "\n"
        self.scope.write(self.mCmd_ImpFile)  # 导入文件
        time.sleep(0.1)

    def openRF(self):
        self.scope.write(self.mCmd_RF_ON)
        time.sleep(0.1)

    def closeRF(self):
        self.scope.write(self.mCmd_RF_OFF)
        time.sleep(0.1)

    def preConfiguration(self, Level=-90.0, cenFreq=230.0):
        self.scope.write(self.mDefault)
        time.sleep(0.1)
        self.scope.write(self.mCmd_ImpFile)
        time.sleep(0.1)
        self.scope.write(self.mCmd_TraSingle)
        time.sleep(0.1)
        self.scope.write(self.mCmd_ARB_ON)
        time.sleep(0.1)
        self.scope.write(self.mCmd_RF_ON)
        time.sleep(0.1)
        self.setPowLev(Level)
        self.setFreq(cenFreq)

    def executeTrigger(self):
        self.scope.write(self.mExecTrig)


if __name__ == '__main__':
    my = KeysightSMBV100A()
    my.setFreq(223)
