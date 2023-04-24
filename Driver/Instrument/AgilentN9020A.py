########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
#######################                                                #################################
####################### AUTHOR: SALVADOR JESÚS MEGÍAS ANDREU           #################################
####################### EMAIL: salvadorjmegias@gmail.com               #################################
####################### UNIVERSITY EMAIL: salvadorjesus@correo.ugr.es  #################################
#######################                                                #################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################


# Librerías o Modulos necesarios a importar
from robot.api.deco import keyword
import pyvisa as visa
import numpy as np
from struct import unpack
import pylab
import time
from matplotlib import pyplot as plot


############################################################################################
##############                 CLASS AGILENT_N9020A     #####################################
##############        SPECTRUM ANALYZER CONTROLLED     #####################################
##############  BY ETHERNET CONTROL                    #####################################
############################################################################################

class AgilentN9020A:
    # La medida con la que vamos a trabajar van a ser los MHz
    medida = 'MHZ'

    ############################################################################################
    ############## CONSTRUCTOR #################################################################
    ############################################################################################

    # Cuando creemos un objeto de la clase, ejecutaremos el setup() conectándose automáticamente a la máquina
    # mediante conexión TCP

    def __init__(self):

        self.scope = self.setup()
        self.scope.write(":SYST:PRES")
        time.sleep(1)
        print(self.scope)
        # sel.nPoints = int(self.scope.query('SWE:POIN?'))

    ############################################################################################
    ############## IDENTITY & SETUP ############################################################
    ############################################################################################

    # Muestra la información propia ofrecida por la máquina

    def identity(self):
        info = self.scope.query('*IDN?')
        info = info.split(",")
        print("Fabricante: ", info[0])
        print("Modelo: ", info[1])
        print("Número de serie: ", info[2])
        print("Firmware: ", info[3])

    # Establece una conexión TCP con la máquina mediante su IP devolviendo el objeto conectado para poder manejarlo

    def setup(self):
        # 192.168.1.200 IP AGILENT MACHINE  Port 5025
        rm = visa.ResourceManager('@py')  # Calling PyVisaPy library
        scope = rm.open_resource('TCPIP::192.168.3.106::INSTR')  # Connecting via LAN
        return scope

    # Finaliza la conexión con la máquina
    def disconnect(self):
        self.scope.close()

    ################################################################################################################################
    # AL CONTRARIO QUE LA MÁQUINA ANRITSU, AGILENT SOLO TIENE MODO SPECTRUM ANALYZER, POR LO QUE NO ES NECESARIO ACTIVAR NINGÚN MODO
    # EL MODO SPECTRUM ANALYZER VIENE POR DEFECTO
    ################################################################################################################################

    # Activa el modo Spectrum en la máquina (por si acaso)

    def setSpectrum(self):
        self.scope.write('INST SA')
        self.instAgilent = 'SA'
        # print("Ha seleccionado el Spectrum Analyzer")

    # Función con la que recogemos todos los datos de la máquina una vez nos conectamos a esta (para tener los datos y no tener que reescribirlos si no es necesario)
    # Dejamos la máquina finalmente en el modo en el que estaba cuando nos conectamos, no modificando así nada
    def getInitialParamsAgilent(self):

        self.instAgilent = str(self.scope.query('INST?'))

        # Seleccionamos el spectrum para poder recoger los datos del spectrum
        self.setSpectrum()
        self.inicialFreq = float(self.scope.query('FREQ:START?')) / 1e6
        self.finalFreq = float(self.scope.query('FREQ:STOP?')) / 1e6
        self.centralFreq = float(self.scope.query('FREQ:CENT?')) / 1e6
        self.referenceLevel = float(self.scope.query('DISP:WIND:TRAC:Y:RLEV?'))
        self.nPoints = int(self.scope.query('SWE:POIN?'))
        self.span = float(self.scope.query('FREQ:SPAN?')) / 1e6

        self.scope.write('INST ' + self.instAgilent)

    ############################################################################################
    ######### FUNCTIONS FOR SPECTRUM ANALYZER ##################################################
    ############################################################################################

    # Muestra todos los parámetros del Espectro en ese momento
    def getParamsSpectrum(self):
        print("Frecuencia central: ", self.centralFreq, "MHz")  # Muestra la frecuencia central
        print("Frecuencia inicial: ", self.inicialFreq, "MHz")  # Muestra la frecuencia inicial
        print("Frecuencia final: ", self.finalFreq, "MHz")  # Muestra la frecuencia final
        print("Nivel de referencia: ", self.referenceLevel, "dBm")  # Muestra el nivel de referencia

    # Modifica todos los parámetros del Spectrum Analyzer (la medida de las frecuencias está en MHz)
    @keyword
    def setParamsSpectrum(self, inicialFreq, finalFreq, referenceLevel):
        # Guarda todos los datos en variables del objeto de la clase
        self.inicialFreq = float(inicialFreq)
        self.finalFreq = float(finalFreq)
        self.referenceLevel = float(referenceLevel)
        self.centralFreq = (self.finalFreq + self.inicialFreq) / 2.0

        self.scope.write('FREQ:START ' + str(inicialFreq) + self.medida)  # Modifica la frecuencia inicial
        self.scope.write('FREQ:STOP ' + str(finalFreq) + self.medida)  # Modifica la frecuencia final
        self.scope.write('FREQ:CENT ' + str(self.centralFreq) + self.medida)  # Modifica la frecuencia central
        self.scope.write('DISP:WIND:TRAC:Y:RLEV ' + str(referenceLevel))  # Modifica el nivel de referencia
        # Se define el número de puntos observables y medibles al valor que tenga la máquina en ese momento (por defecto son 10001)
        self.nPoints = int(self.scope.query('SWE:POIN?'))

    # Modifica todos los parámetros del Spectrum Analyzer mediante el uso de span (la medida de las frecuencias está en MHz)
    @keyword
    def setParamsSpectrumSpan(self, centralFreq, span, referenceLevel):
        self.setCentralFreqMHz(centralFreq)  # Modifica la frecuencia central y su atributo de la clase
        self.setSpanMHz(
            span)  # llama a la función modificando el valor de span inicialFreq y finalFreq y los atributos de la clase
        self.setReferenceLevelDBM(
            referenceLevel)  # llama a la función modificando el valor de referencelevel y el atributo de la clase
        # Se define el número de puntos observables y medibles al valor que tenga la máquina en ese momento (por defecto son 10001)
        self.nPoints = int(self.scope.query('SWE:POIN?'))

    # Modifica el valor del span, inicialFreq y finalFreq y aparte los atributos de la clase correspondientes a la frecuencia inicial y final y el span
    # (Hace falta haber definido la frecuencia central)
    @keyword
    def setSpanMHz(self, span):
        self.span = float(span)
        mitad = self.span / 2.0
        self.scope.write('FREQ:SPAN ' + str(span) + self.medida)

        self.inicialFreq = self.centralFreq - mitad
        self.scope.write('FREQ:START ' + str(self.inicialFreq) + self.medida)
        self.finalFreq = self.centralFreq + mitad
        self.scope.write('FREQ:STOP ' + str(self.finalFreq) + self.medida)

    # Muestra el Span en ese momento
    @keyword
    def getSpanMHz(self):
        print("Span: ", self.span, " MHz")

    # Modifica el valor de la frecuencia central y el atributo del objeto de la clase correspondiente
    @keyword
    def setCentralFreqMHz(self, centralFreq):
        self.centralFreq = float(centralFreq)
        self.scope.write('FREQ:CENT ' + str(centralFreq) + self.medida)

    # Muestra la frecuencia central en ese momento
    def getCentralFreqMHz(self):
        print("Frecuencia central: ", self.centralFreq, " MHz")

    # Modifica la frecuencia incial y el atributo del objeto de la clase correspondiente
    @keyword
    def setInicialFreqMHz(self, inicialFreq):
        self.inicialFreq = float(inicialFreq)
        self.scope.write('FREQ:START ' + str(inicialFreq) + self.medida)
        self.centralFreq = (self.inicialFreq + self.finalFreq) / 2.0

    # Muestra la frecuencia inicial en ese momento

    def getInicialFreqMHz(self):
        print("Frecuencia inicial: ", self.inicialFreq, " MHz")

    # Modifica la frecuencia final y el atributo del objeto de la clase correspondiente

    def setFinalFreqMHz(self, finalFreq):
        self.finalFreq = float(finalFreq)
        self.scope.write('FREQ:STOP ' + str(finalFreq) + self.medida)
        self.centralFreq = (self.inicialFreq + self.finalFreq) / 2.0

    # Muestra la frecuencia final en ese momento

    def getFinalFreqMHz(self):
        print("Frecuencia final: ", self.finalFreq, " MHz")

    # Modifica el nivel de referencia y el atributo del objeto de la clase correspondiente
    @keyword
    def setReferenceLevelDBM(self, referenceLevel):
        self.referenceLevel = float(referenceLevel)
        self.scope.write('DISP:WIND:TRAC:Y:RLEV ' + str(referenceLevel))

    # Muestra el nivel de referencia en ese momento

    def getReferenceLevelDBM(self):
        print("Nivel de referencia: ", self.referenceLevel, " dBm")

    # Muestra y devuelve el número de puntos observables y medibles en ese momento

    def getNumPoints(self):
        puntos = int(self.scope.query('SWE:POIN?'))
        # print("Número de puntos: ",puntos)
        return puntos

    # Modifica el número de puntos observables y medibles y el atributo del objeto de la clase correspondiente

    def setNumPoints(self, npoints):
        self.nPoints = int(npoints)
        self.scope.write('SWE:POIN ' + str(npoints))

    # Muestra y devuelve la frecuencia donde se encuentra la potencia máquina y la potencia máxima

    def getMaxFreqPower(self):
        self.scope.write('CALC:MARK:MAX')
        # print("Frecuencia donde se encuentra la potencia máxima: ",self.scope.query('CALC:MARK:X?')," MHz")
        # print("Potencia máxima: ",self.scope.query('CALC:MARK:Y?')," dBm")
        self.maxfreq = float(self.scope.query('CALC:MARK:X?')) / 1e6
        power = float(self.scope.query('CALC:MARK:Y?'))
        return power

    # Función que devuelve la potencia referente a una frecuencia dada
    @keyword
    def getPowerDBM(self, freq):
        self.scope.write('CALC:MARK:X ' + str(freq) + self.medida)
        print("Potencia asociada a la frecuencia dada: ", self.scope.query('CALC:MARK:Y?'), " dBm")

    ############################################################################################
    ############## PLOT INFORMATION  ###########################################################
    ############################################################################################

    # Función que guarda una imagen png y la muestra en pantalla de la señal del Spectrum completa en ese momento

    def plotInfoAgilent(self):

        puntos = self.getNumPoints()  # guardamos el número de puntos a representar con plot

        self.scope.write('FORM ASC')  # Pide a la máquina que lo que se le pide lo devuelva en formato ASCII
        datos = self.scope.query(
            'TRAC? TRACE1')  # Pide a la máquina los datos del Spectrum (los datos son las potencias de los 10001 puntos observables y medibles)
        datosManipulables = datos.split(",")  # separa todos los datos separados por comas y los guarda en una lista
        datosManipulables = [float(i) for i in
                             datosManipulables]  # transformo los datos de string a float para poder trabajar con ellos

        self.datosCapturados = datosManipulables.copy()  # Para poder hacer uso de ellos en caso de querer buscar máximos, mínimos...

        freq = self.finalFreq - self.inicialFreq  # definimos la amplitud del intervalo de frecuencias a representar
        pointWidth = freq / float(
            puntos)  # defino la anchura que debe ocupar cada punto en la imagen (para saber donde colocar cada frecuencia en la imagen)

        # Creo una lista de todas las frecuencias a representar
        frequencies = []
        count = 0
        while len(frequencies) != puntos:
            frequencies.append(self.inicialFreq + (pointWidth * count))
            count += 1

        plot.clf()

        # Label for x-axis
        plot.xlabel("Frequency (MHz)")

        # Label for y-axis
        plot.ylabel("Power (dBm)")

        # title of the plot
        plot.title("Output of Spectrum Analyzer")

        # Add grid lines
        plot.grid()

        # Genero la imagen con las frecuencias calculadas y las potencias ofrecidas por la máquina

        plot.plot(frequencies, datosManipulables)
        plot.savefig('./images/graphAgilent.png')  # Dirección relativa donde se quiere que se guarde la imagen creada
        plot.show()

    ############################################################################################
    ############## PLOT INFORMATION  ###########################################################
    ############################################################################################

    @keyword
    # 获取峰值功率，maxhold界面下的最大功率
    def getPeakPower(self):
        self.scope.write(":DISP:VIEW NORM")
        self.scope.write(":TRACe1:TYPE MAXHold")
        time.sleep(1)
        self.scope.write("CALC:MARK:PEAK:TABL:STAT ON")  # 打开EAK捕捉
        self.scope.write("CALC:MARK:PEAK:TABL:READ GTDL")
        mPower = self.scope.query(":TRACe:MATH:PEAK?")
        mPower = round(float(mPower), 2)
        print("peakPower:{}\r\n".format(mPower))
        return mPower

    @keyword
    def getChannelPower(self, span=10):
        self.setSpanMHz(span)
        mChanPower = round(float(self.scope.query("MEASure:CHPower:CHPower?")), 2)
        print('channel power:{} / 2Mhz'.format(mChanPower))
        return mChanPower

    @keyword
    # 临道泄露功率
    def getACP(self, offset=3):
        self.scope.write("ACP:OFFS1:LIST " + str(offset) + self.medida + ",0,0,0,0,0")
        self.acpPower = self.scope.query(":READ:ACP1?")
        result = self.acpPower.split(",")
        if len(result) != 3:
            return 0
        mRefCarrierPower = float(result[0])
        mLowerACPower = round(float(result[1]), 2)
        mUpperACPower = round(float(result[2]), 2)
        print('ACP:', self.acpPower, 'CarrierPower:', mRefCarrierPower, 'LowerACPower:', mLowerACPower, 'UpperACPower:',
              mUpperACPower)
        return mLowerACPower

    @keyword
    # 占用带宽OBW  分辨率带宽Res BW
    def getOccupiedBandWidth(self, Span=0.2, RBW=0, cnt=20):
        # 开始采集数据
        self.scope.write("DISP:OBW:VIEW:WIND:TRAC:Y:RLEV 125")  # 设置参考等级
        mRef = float(self.scope.query('DISP:OBW:VIEW:WIND:TRAC:Y:RLEV?'))

        self.scope.write("DISP:OBW:VIEW:WIND:TRAC:Y:COUP ON")  # 开启自动缩放功能
        self.scope.write("OBW:FREQ:SPAN " + str(Span) + self.medida)
        if RBW != 0:
            self.scope.write("OBW:BAND:AUTO OFF")  # 关闭自动带宽
            self.scope.write("OBW:BAND " + str(RBW))  # 设置分辨率带宽  VBW/RBW (10:1)    Span/RBW(106:1)
            mRbw = float(self.scope.query("OBW:BAND?"))
            print("RBW:{}\r\n".format(mRbw))

        mValue = 0
        for i in range(cnt):
            mValue += float(self.scope.query(":READ:OBWidth:OBWidth?"))
        self.occupiedBw = round(mValue / cnt, 2)
        print("OccupiedBW:{}\r\n".format(self.occupiedBw))
        return self.occupiedBw

    @keyword
    # 获取频偏数据 frequency offset  频偏是指实际信号的中心频率与理论或期望的中心频率之间的差异
    def getFreOffset(self):
        self.scope.write(":CALC:MARK1:MODE POS")  # 打开Mak1点 (1)
        self.scope.write("CALCulate:MARKer1:X")  # 将Mark1点放置于频率为中心频点处
        power = self.scope.query("CALC:MARK1:Y?")  # 采样最大功率 (1)
        self.scope.write(":CALC:BWID ON")  # 打开频偏 (1)
        self.scope.write(":CALC:BWID OFF")  # 关闭频偏 (2)
        mOffset = self.scope.query(":FREQuency:OFFSet?")
        print("offset:{}\r\n".format(power))

    @keyword
    # 杂散辐射
    def getSpurEm(self, band='10kHz',limit=-40.0, startFreq='9kHz', stopFreq='150kHz'):
        # 示例 startFreq：‘9kHz,150kHz,30MHz,1GHz’  stopFreq:'150kHz,30MHz,1GHz,2.1GHz'
        self.scope.write(":CONFigure:SPURious")
        self.scope.write(":SPURious:LIST:STATe 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")  # 仅开启一个range
        self.scope.write("SPUR:BAND " + band)
        self.scope.write("CALC:SPUR:LIM:ABS:DATA:STOP " + str(limit))
        self.scope.write(":SPURious:REPT:MODE LIMTest")
        self.scope.write("SPUR:FREQ:STAR " + startFreq)
        self.scope.write("SPUR:FREQ:STOP " + stopFreq)
        #self.scope.write("SPUR:BWID:AUTO ON")
        mSpurEm = self.scope.query(':READ:SPURious?')
        print("SpurEm:{}\r\n".format(mSpurEm))

        result = mSpurEm.split(",")
        if len(result) < 1:
            return 0
        ret = round(float(result[0]), 2)
        if ret == 0.00:
            ret = 1
        else:
            ret = 0
        return ret

    @keyword
    # 谐波测量 单位dbc
    def getHarmonic(self, freq, referenceLevel=20):
        self.scope.write("CONFigure:HARMonics")
        self.scope.write('DISP:HARM:VIEW:WIND:TRAC:Y:RLEV ' + str(referenceLevel) + 'dbm')  # rle
        self.scope.write("HARMonics:FREQuency:FUNDamental:AUTO OFF")
        self.scope.write("HARM:FREQ:FUND " + str(freq) + self.medida)
        self.Harm = self.scope.query("READ:HARMonics:AMPLitude:ALL?")
        result = self.Harm.split(",")
        return result

    @keyword
    # 二次谐波
    def getHarmonic2nd(self, freq, referenceLevel=20):
        self.scope.write("CONFigure:HARMonics")
        self.scope.write('DISP:HARM:VIEW:WIND:TRAC:Y:RLEV ' + str(referenceLevel) + 'dbm')  # rle
        self.scope.write("HARMonics:FREQuency:FUNDamental:AUTO OFF")
        self.scope.write("HARM:FREQ:FUND " + str(freq) + self.medida)
        result = self.scope.query("READ:HARMonics:AMPLitude:ALL?")
        result = result.split(",")
        if len(result) < 2:
            return 0
        mHarm = round(float(result[1]), 2)
        return mHarm


    @keyword
    # 三次谐波
    def getHarmonic3nd(self, freq, referenceLevel=20):
        self.scope.write("CONFigure:HARMonics")
        self.scope.write('DISP:HARM:VIEW:WIND:TRAC:Y:RLEV ' + str(referenceLevel) + 'dbm')  # rle
        self.scope.write("HARMonics:FREQuency:FUNDamental:AUTO OFF")
        self.scope.write("HARM:FREQ:FUND " + str(freq) + self.medida)
        result = self.scope.query("READ:HARMonics:AMPLitude:ALL?")
        result = result.split(",")
        if len(result) < 3:
            return 0
        mHarm = round(float(result[2]), 2)
        return mHarm


if __name__ == '__main__':
    my_agN = AgilentN9020A()
    my_agN.setParamsSpectrum(213, 233, 20)
    ahah = my_agN.getSpurEm()
    print(ahah)
