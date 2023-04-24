########################################################################################################
#######################                                                #################################
####################### AUTHOR: xiaoge                                 #################################
####################### EMAIL: salvadorjmegias@gmail.com               #################################
####################### UNIVERSITY EMAIL: salvadorjesus@correo.ugr.es  #################################
#######################                                                #################################
########################################################################################################

from robot.api.deco import keyword
import pyvisa as visa
import time
class SMUChannel:
    
    def __init__(self, channel, smu):
        self.channel = channel
        self.smu = smu
        
        self.__voltage_range = 20
        self.__current_range = 2
        
        
    def set_mode_voltage_source(self):
        """
        Sets the channel into voltage source mode.
        In this mode you set the voltage and can measure current, resistance and power.
        """
        self.smu._set_source_mode(self.channel, KeysightB2900.VOLTAGE_MODE)

    def set_mode_current_source(self):
        """
        Sets the channel into current source mode.
        In this mode you set the current and can measure voltage, resistance and power.
        """
        self.smu._set_source_mode(self.channel, KeysightB2900.CURRENT_MODE)

    def set_voltage_limit(self, value):
        """
        Limits the voltage output of the current source.
        If you are in voltage source mode the voltage limit has no effect.
        """
        if value <= self.__voltage_range:
            self.smu._set_limit(self.channel, KeysightB2900.CURRENT_MODE, value)
        else:
            raise ValueError("The limit is not within the range. Please set the range first")

    def set_current_limit(self, value):
        """
        Limits the current output of the voltage source.
        If you are in current source mode the current limit has no effect.
        """
        if value <= self.__current_range:
            self.smu._set_limit(self.channel, KeysightB2900.VOLTAGE_MODE, value)
        else:
            raise ValueError("The limit is not within the range. Please set the range first")

    
    def set_voltage(self, value):
        """
        Sets the output level of the voltage source.
        """
        self.smu._set_level(self.channel, KeysightB2900.VOLTAGE_MODE, value)

    def set_current(self, value):
        """
        Sets the output level of the current source.
        """
        self.smu._set_level(self.channel, KeysightB2900.CURRENT_MODE, value)

    def enable_output(self):
        """
        Sets the source output state to on.

        Note:
           When the output is switched on, the SMU sources either voltage or current, as set by
           set_mode_voltage_source() or set_mode_current_source()
        """
        self.smu._set_output_state(self.channel, KeysightB2900.STATE_ON)

    def disable_output(self):
        """
        Sets the source output state to off.

        Note:
           When the output is switched off, the SMU goes in to High Z mode (meaning: the output is opened).
        """
        self.smu._set_output_state(self.channel, KeysightB2900.STATE_OFF)
        
        
    def measure_voltage(self):
        """
        Perform spot measurement and retrieve voltage.

        Note:
           When the output is switched off, the SMU turns on output automatically and performs a measurement.
        """
        return self.smu._measure(self.channel, KeysightB2900.VOLTAGE_MODE)
    
    def measure_current(self):
        """
        Perform spot measurement and retrieve current.

        Note:
           When the output is switched off, the SMU turns on output automatically and performs a measurement.
        """
        return self.smu._measure(self.channel, KeysightB2900.CURRENT_MODE)

class KeysightB2900:
    dev = None
    dev_id = ""
    
    # define strings that are used in the LUA commands
    CHAN1 = "2"
    CHAN2 = "1"

    CURRENT_MODE = "CURR"
    VOLTAGE_MODE = "VOLT"

    STATE_ON = "ON"
    STATE_OFF = "OFF"

    SPEED_FAST = 0.01
    SPEED_MED = 0.1
    SPEED_NORMAL = 1
    SPEED_HI_ACCURACY = 10

    mCmd_Confirm = "SYST:ERR:COUN?\n"  # 查询命令是否正确
    mCmd_ID = "*IDN?\n"  # 查询设备信息
    mCmd_OUTP1_STAT_OFF = "OUTP1:STAT OFF\n"
    mCmd_CLS = "*CLS\n"
    mCmd_MATH_STAT_OFF = "CALC1:MATH:STAT OFF\n"  # 禁用数学表达式
    mCmd_CLIM_STAT_OFF = "CALC1:CLIM:STAT OFF\n"  # 禁用复合极限测试
    mCmd_RES_MODE_MAN = "SENS1:RES:MODE MAN\n"
    mCmd_VOLT_RANG_AUTO_OFF = "SOUR1:VOLT:RANG:AUTO OFF\n"
    mCmd_VOLT_RANG = "SOUR1:VOLT:RANG 20\n"
    mCmd_VOLT_MODE_FIX = "SOUR1:VOLT:MODE FIX\n"
    mCmd_FUNC_DC = "SOUR1:FUNC DC\n"
    mCmd_VOLT = "SOUR1:VOLT 5\n"
    mCmd_VOLT_TRIG = "SOUR1:VOLT:TRIG 5\n"

    mCmd_CURR_PROT = "SENS1:CURR:PROT 0.3\n"
    mCmd_FUNC_MODE_VOLT = "SOUR1:FUNC:MODE VOLT\n"
    mCmd_ASC = "FORM ASC\n"
    mCmd_BORD_NORM = "FORM:BORD NORM\n"
    mCmd_ELEM_SENS = "FORM:ELEM:SENS VOLT,CURR,TIME\n"
    mCmd_FUNC_OFF = "SENS1:FUNC:OFF:ALL\n"
    mCmd_FUNC_ON_VOLT = "SENS1:FUNC:ON \"VOLT\"\n"
    mCmd_VOLT_APER_AUTO_OFF = "SENS1:CURR:APER:AUTO OFF\n"
    mCmd_VOLT_APER = "SENS1:CURR:APER 5E-04\n"
    mCmd_FUNC_ON_CURR = "SENS1:FUNC:ON \"CURR\"\n"

    mCmd_CURR_APER_AUTO = "SENS1:CURR:APER:AUTO OFF\n"
    # mCmd_CURR_APER = "SENS1:CURR:APER 0.0005\n"
    mCmd_CURR_APER = "SENS1:CURR:NPLC 0.1\n"
    mCmd_CURR_RANG_AUTO_OFF = "SENS1:CURR:RANG:AUTO OFF\n"
    mCmd_CURR_RANG = "SENS1:CURR:RANG 1\n"
    mCmd_REM_OFF = "SENS1:REM OFF\n"
    mCmd_HCAP_OFF = "OUTP1:HCAP OFF\n"
    mCmd_FILT_ON = "OUTP1:FILT ON\n"
    mCmd_FILT_AUTO_OFF = "OUTP1:FILT:AUTO OFF\n"
    mCmd_FILT_TCON = "OUTP1:FILT:TCON 5E-06\n"
    mCmd_FUNC_TRIG_CONT_ON = "SOUR1:FUNC:TRIG:CONT ON\n"

    mCmd_ALL_COUN = "ARM1:ALL:COUN 1\n"
    mCmd_ACQ_DEL_1 = "ARM1:ACQ:DEL 0\n"
    mCmd_TRAN_DEL_1 = "ARM1:TRAN:DEL 0\n"
    mCmd_LXI_LAN_DIS_ALL = "ARM1:LXI:LAN:DIS:ALL\n"
    mCmd_ALL_SOUR_AINT = "ARM1:ALL:SOUR AINT\n"
    mCmd_ALL_TIM_MIN = "ARM1:ALL:TIM MIN\n"
    mCmd_TRAN_COUN = "TRIG1:TRAN:COUN 1\n"
    mCmd_ACQ_COUN = "TRIG1:ACQ:COUN 500\n"
    mCmd_TRAN_DEL_2 = "TRIG1:TRAN:DEL 0\n"
    mCmd_ACQ_DEL_2 = "TRIG1:ACQ:DEL 0\n"

    mCmd_TRAN_SOUR_TIM = "TRIG1:TRAN:SOUR TIM\n"
    mCmd_TRAN_TIM_MIN = "TRIG1:TRAN:TIM MIN\n"
    mCmd_ACQ_SOUR_TIM = "TRIG1:ACQ:SOUR TIM\n"
    mCmd_ACQ_TIM = "TRIG1:ACQ:TIM 0.002\n"
    mCmd_SOUR1_WAIT_OFF = "SOUR1:WAIT OFF\n"
    mCmd_SENS1_WAIT_OFF = "SENS1:WAIT OFF\n"
    mCmd_OUTP1_STAT_ON = "OUTP1:STAT ON\n"
    mCmd_OPER_PTR = "STAT:OPER:PTR 7020\n"
    mCmd_OPER_NTR = "STAT:OPER:NTR 7020\n"
    mCmd_OPER_ENAB = "STAT:OPER:ENAB 7020\n"

    mCmd_SRE = "*SRE 128\n"
    mCmd_COUN_RES_AUTO_ON = "SYST:TIME:TIM:COUN:RES:AUTO ON\n"

    mCmd_INIT = "INIT (@1)\n"
    mCmd_DATA = "SENS1:DATA? 0\n"
    mCmd_TEST = ":SENS:CURR:APER +2\n"

    def __init__(self):
        rm = visa.ResourceManager('@py')

        self.scope = rm.open_resource('TCPIP::192.168.3.192::INSTR')
        self.dev_id = self.scope.query("*IDN?")

        self.chan1 = SMUChannel("1", self)
        # self.chan2 = SMUChannel("2", self)

    def close(self):
        if self.scope != None:
            self.scope.close()
            self.scope = None

    def reset(self):

        if self.scope == None:
            raise RuntimeError("Device not connected.")

        self.scope.write("*RST")

    def set_display(self):
        # todo
        pass

    def write_command(self, command):

        if self.scope == None:
            raise RuntimeError("Device not connected.")

        self.scope.write(command)

    def write_query(self, query):

        if self.scope == None:
            raise RuntimeError("Device not connected.")

        data = self.scope.query(query)
        return data

    """
    #####################################################################################
    commands for setting the parameters of channels
    those should not be accessed directly but through the channel class
    #####################################################################################
    """
    def _set_measurement_speed(self, channel, speed, sense_mode):
        """defines how many PLC (Power Line Cycles) a measurement takes"""
        cmd = f':SENS{channel}:{sense_mode}:NPLC {speed}'
        self.write_command(cmd)

    def _set_source_mode(self, channel, source_mode):
        cmd = f':SOUR{channel}:FUNC:MODE {source_mode}'
        self.write_command(cmd)

    def _set_sense_wire_mode(self, channel, four_wire_on):
        """set 2-wire or 4-wire sense mode"""
        cmd = f':SENS{channel}:REM {four_wire_on}'
        self.write_command(cmd)

    def _set_limit(self, channel, sense_mode, value):
        """command used to set the limits for voltage or current"""
        cmd = f':SENS{channel}:{sense_mode}:PROT {value}'
        self.write_command(cmd)

    def _set_level(self, channel, source_mode, value):
        cmd = f':SOUR{channel}:{source_mode} {value}'
        self.write_command(cmd)

    def _set_output_state(self, channel, on_off):
        cmd = f':OUTP{channel} {on_off}'
        self.write_command(cmd) 

    def _measure(self, channel, mode):
        query = f'MEAS:{mode}? (@{channel})'
        return self.write_query(query)

    def setVolt(self, volt):
        self.volt = str(volt)
        self.voltTrig = str(volt)
        self.mCmd_VOLT = "SOUR1:VOLT " + self.volt + "\n"
        self.mCmd_VOLT_TRIG = "SOUR1:VOLT:TRIG" + self.voltTrig + "\n"

    def setCurrent(self, curr):
        self.current = curr
        self.mCmd_CURR_PROT = "SENS1:CURR:PROT " + self.current + "\n"

    def B2900_PreConfiguration(self):
        self.write_command(self.mCmd_CLS)
        self.write_command(self.mCmd_MATH_STAT_OFF)
        self.write_command(self.mCmd_CLIM_STAT_OFF)
        self.write_command(self.mCmd_RES_MODE_MAN)
        self.write_command(self.mCmd_VOLT_RANG_AUTO_OFF)
        self.write_command(self.mCmd_VOLT_RANG)
        self.write_command(self.mCmd_VOLT_MODE_FIX)
        self.write_command(self.mCmd_FUNC_DC)
        self.write_command(self.mCmd_VOLT)
        self.write_command(self.mCmd_VOLT_TRIG)

        self.write_command(self.mCmd_CURR_PROT)
        self.write_command(self.mCmd_FUNC_ON_VOLT)
        self.write_command(self.mCmd_ASC)
        self.write_command(self.mCmd_BORD_NORM)
        self.write_command(self.mCmd_ELEM_SENS)
        self.write_command(self.mCmd_FUNC_OFF)
        self.write_command(self.mCmd_FUNC_ON_VOLT)
        self.write_command(self.mCmd_VOLT_APER_AUTO_OFF)
        self.write_command(self.mCmd_VOLT_APER)
        self.write_command(self.mCmd_FUNC_ON_CURR)

        self.write_command(self.mCmd_CURR_APER_AUTO)
        self.write_command(self.mCmd_CURR_APER)
        self.write_command(self.mCmd_CURR_RANG_AUTO_OFF)
        self.write_command(self.mCmd_CURR_RANG)
        self.write_command(self.mCmd_REM_OFF)
        self.write_command(self.mCmd_HCAP_OFF)
        self.write_command(self.mCmd_FILT_ON)
        self.write_command(self.mCmd_FILT_AUTO_OFF)
        self.write_command(self.mCmd_FILT_TCON)
        self.write_command(self.mCmd_FUNC_TRIG_CONT_ON)

    
if __name__ == '__main__':
    my = KeysightB2900()
    my.chan1.disable_output()
    my.chan1.set_voltage(5)
    my.chan1.set_current(0.4)
    my.chan1.enable_output()
    pt = my.chan1.measure_current()
    print(pt)
    # my.B2900_PreConfiguration()
    
