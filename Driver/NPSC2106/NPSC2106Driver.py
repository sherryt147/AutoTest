from robot.api.deco import keyword
import NPSC2106Reg
import time
import BoardDriver.SerialLibrary as SerialLibrary
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))


DriverPort = 'COM7'
DriverBaudrate = 115200
DefaultConfigName = "CMT2300Config_20dbm.exp"

# CMT2300A Config Buffer
g_cmt2300aCmtBank = []
g_cmt2300aSystemBank = []
g_cmt2300aFrequencyBank = []
g_cmt2300aDataRateBank = []
g_cmt2300aBasebandBank = []
g_cmt2300aTxBank = []


class NPSC2106Driver:
    def __init__(self):
        self.my_serial = SerialLibrary.SerialLibrary(
            DriverPort, DriverBaudrate)
        # 打开CMT2300A配置工具生成的配置文件，并读取相关数据，转换成数组
        self.CMT2300A_GetConfig()
        
    def CMT2300A_GetConfig(self,configName = DefaultConfigName):
        g_cmt2300aCmtBank.clear()
        g_cmt2300aSystemBank.clear()
        g_cmt2300aFrequencyBank.clear()
        g_cmt2300aDataRateBank.clear()
        g_cmt2300aBasebandBank.clear()
        g_cmt2300aTxBank.clear()
        CMT2300ConfigName = current_dir +"/CMT2300Config/" + configName
        print(CMT2300ConfigName)
        with open(CMT2300ConfigName, 'rt') as f:
            CMT_Bank_Flag = ""
            System_Bank = ""
            Frequency = ""
            Data_Rate = ""
            Baseband = ""
            TX_Bank = ""
            Flag = ""
            i = 0
            for line in f.readlines():
                if CMT_Bank_Flag and Flag:
                    g_cmt2300aCmtBank.append(int(line[8:10], 16))
                    i = i+1
                    if(i >= 12):
                        CMT_Bank_Flag = ""
                        Flag = ""
                        i = 0
                        print(g_cmt2300aCmtBank)
                if System_Bank and Flag:
                    g_cmt2300aSystemBank.append(int(line[8:10], 16))
                    i = i+1
                    if(i >= 12):
                        System_Bank = ""
                        Flag = ""
                        i = 0
                        print(g_cmt2300aSystemBank)
                if Frequency and Flag:
                    g_cmt2300aFrequencyBank.append(int(line[8:10], 16))
                    i = i+1
                    if(i >= 8):
                        Frequency = ""
                        Flag = ""
                        i = 0
                        print(g_cmt2300aFrequencyBank)
                if Data_Rate and Flag:
                    g_cmt2300aDataRateBank.append(int(line[8:10], 16))
                    i = i+1
                    if(i >= 24):
                        Data_Rate = ""
                        Flag = ""
                        i = 0
                        print(g_cmt2300aDataRateBank)
                if Baseband and Flag:
                    g_cmt2300aBasebandBank.append(int(line[8:10], 16))
                    i = i+1
                    if(i >= 29):
                        Baseband = ""
                        Flag = ""
                        i = 0
                        print(g_cmt2300aBasebandBank)
                if TX_Bank and Flag:
                    g_cmt2300aTxBank.append(int(line[8:10], 16))
                    i = i+1
                    if(i >= 11):
                        TX_Bank = ""
                        Flag = ""
                        i = 0
                        print(g_cmt2300aTxBank)

                if '[CMT Bank]' in line:
                    CMT_Bank_Flag = line.strip()
                    print(CMT_Bank_Flag)
                elif '[System Bank]' in line:
                    System_Bank = line.strip()
                    print(System_Bank)
                elif '[Frequency Bank]' in line:
                    Frequency = line.strip()
                    print(Frequency)
                elif '[Data Rate Bank]' in line:
                    Data_Rate = line.strip()
                    print(Data_Rate)
                elif '[Baseband Bank]' in line:
                    Baseband = line.strip()
                    print(Baseband)
                elif '[TX Bank]' in line:
                    TX_Bank = line.strip()
                    print(TX_Bank)
                elif 'Addr  Value' in line:
                    Flag = line.strip()
                    print(Flag)
        
    @keyword
    def CMT2300A_ReadReg(self, addr):
        # 将addr和value转换为16进制，并加上前缀0x
        addr_hex = hex(addr)[2:].zfill(2)
        command = "AT+READ2106REG=" + addr_hex + "\r\n"
        self.my_serial.write_to_serial(command)
        readstr = self.my_serial.read_from_serial()
        data_str = readstr.split(":")[1].strip()
        print("Read 2106 Value:", addr_hex, ":", data_str)
        data_hex = int(data_str, 16) & 0xff
        return data_hex

    @keyword
    def CMT2300A_WriteReg(self, addr, value):
        # 将addr和value转换为16进制，并加上前缀0x
        addr_hex = hex(addr)[2:].zfill(2)
        value_hex = hex(value)[2:].zfill(2)
        print("Write 2106 Value:", addr_hex, ":", value_hex)
        # 拼接AT+WRITERF=指令字符串
        command = "AT+WRITE2106REG=" + addr_hex + value_hex+"\r\n"
        self.my_serial.write_to_serial(command)
        self.my_serial.read_from_serial()
        return True

    @keyword
    def CMT2300A_WriteFifo(self, pbuf):
        # cmt_spi3_write_fifo(buf, len)
        print("Write 2106 Fifo Data:", pbuf)
        command = "AT+WRITE2106FIFO=" + pbuf + "\r\n"
        self.my_serial.write_to_serial(command)
        self.my_serial.read_from_serial()
        return

    def CMT2300A_DelayMs(self, time_s):
        time_ms = int(time_s/1000)
        time.sleep(time_ms)

    @keyword
    def CMT2300A_Init(self):
        tmp = 0
        self.CMT2300A_SoftReset()
        self.CMT2300A_DelayMs(20)
        self.CMT2300A_GoStby()
        tmp = self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_MODE_STA)
        print(tmp)
        tmp |= NPSC2106Reg.CMT2300A_MASK_CFG_RETAIN
        tmp &= ~NPSC2106Reg.CMT2300A_MASK_RSTN_IN_EN
        print(tmp)
        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_MODE_STA, tmp)
        tmp = self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_EN_CTL)
        tmp |= NPSC2106Reg.CMT2300A_MASK_LOCKING_EN
        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_EN_CTL, tmp)
        self.CMT2300A_EnableLfosc(False)
        self.CMT2300A_ClearInterruptFlags()

    def CMT2300A_EnableLfosc(self, bEnable=True):
        tmp = self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_SYS2)
        if bEnable:
            tmp |= NPSC2106Reg.CMT2300A_MASK_LFOSC_RECAL_EN
            tmp |= NPSC2106Reg.CMT2300A_MASK_LFOSC_CAL1_EN
            tmp |= NPSC2106Reg.CMT2300A_MASK_LFOSC_CAL2_EN
        else:
            tmp &= ~NPSC2106Reg.CMT2300A_MASK_LFOSC_RECAL_EN
            tmp &= ~NPSC2106Reg.CMT2300A_MASK_LFOSC_CAL1_EN
            tmp &= ~NPSC2106Reg.CMT2300A_MASK_LFOSC_CAL2_EN

        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_SYS2, tmp)

    def CMT2300A_EnableLfoscOutput(self, bEnable):
        tmp = self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_INT2_CTL)
        if bEnable:
            tmp |= NPSC2106Reg.CMT2300A_MASK_LFOSC_OUT_EN
        else:
            tmp &= ~NPSC2106Reg.CMT2300A_MASK_LFOSC_OUT_EN
        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_INT2_CTL, tmp)

    def CMT2300A_ClearInterruptFlags(self):
        nFlag1, nFlag2 = 0, 0
        nClr1, nClr2 = 0, 0
        nRet = 0
        nIntPolar = 0

        nIntPolar = self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_INT1_CTL)
        nIntPolar = 1 if (
            nIntPolar & NPSC2106Reg.CMT2300A_MASK_INT_POLAR) else 0

        nFlag1 = self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_INT_FLAG)
        nFlag2 = self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_INT_CLR1)

        if nIntPolar:
            # Interrupt flag active-low
            nFlag1 = ~nFlag1
            nFlag2 = ~nFlag2

        if NPSC2106Reg.CMT2300A_MASK_LBD_FLG & nFlag1:
            nClr2 |= NPSC2106Reg.CMT2300A_MASK_LBD_CLR         # Clear LBD_FLG

        if NPSC2106Reg.CMT2300A_MASK_COL_ERR_FLG & nFlag1:
            # Clear COL_ERR_FLG by PKT_DONE_CLR
            nClr2 |= NPSC2106Reg.CMT2300A_MASK_PKT_DONE_CLR

        if NPSC2106Reg.CMT2300A_MASK_PKT_ERR_FLG & nFlag1:
            # Clear PKT_ERR_FLG by PKT_DONE_CLR
            nClr2 |= NPSC2106Reg.CMT2300A_MASK_PKT_DONE_CLR

        if NPSC2106Reg.CMT2300A_MASK_PREAM_OK_FLG & nFlag1:
            nClr2 |= NPSC2106Reg.CMT2300A_MASK_PREAM_OK_CLR    # Clear PREAM_OK_FLG
            nRet |= NPSC2106Reg.CMT2300A_MASK_PREAM_OK_FLG    # Return PREAM_OK_FLG

        if NPSC2106Reg.CMT2300A_MASK_SYNC_OK_FLG & nFlag1:
            nClr2 |= NPSC2106Reg.CMT2300A_MASK_SYNC_OK_CLR    # Clear SYNC_OK_FLG
            nRet |= NPSC2106Reg.CMT2300A_MASK_SYNC_OK_FLG    # Return SYNC_OK_FLG

        if NPSC2106Reg.CMT2300A_MASK_NODE_OK_FLG & nFlag1:
            nClr2 |= NPSC2106Reg.CMT2300A_MASK_NODE_OK_CLR    # Clear NODE_OK_FLG
            nRet |= NPSC2106Reg.CMT2300A_MASK_NODE_OK_FLG    # Return NODE_OK_FLG

        if NPSC2106Reg.CMT2300A_MASK_CRC_OK_FLG & nFlag1:
            nClr2 |= NPSC2106Reg.CMT2300A_MASK_CRC_OK_CLR    # Clear CRC_OK_FLG
            nRet |= NPSC2106Reg.CMT2300A_MASK_CRC_OK_FLG    # Return CRC_OK_FLG

        if NPSC2106Reg.CMT2300A_MASK_PKT_OK_FLG & nFlag1:
            nClr2 |= NPSC2106Reg.CMT2300A_MASK_PKT_DONE_CLR  # Clear PKT_OK_FLG
            nRet |= NPSC2106Reg.CMT2300A_MASK_PKT_OK_FLG    # Return PKT_OK_FLG

        if NPSC2106Reg.CMT2300A_MASK_SL_TMO_FLG & nFlag2:
            nClr1 |= NPSC2106Reg.CMT2300A_MASK_SL_TMO_CLR    # Clear SL_TMO_FLG
            nRet |= NPSC2106Reg.CMT2300A_MASK_SL_TMO_EN     # Return SL_TMO_FLG by SL_TMO_EN

        if NPSC2106Reg.CMT2300A_MASK_RX_TMO_FLG & nFlag2:
            nClr1 |= NPSC2106Reg.CMT2300A_MASK_RX_TMO_CLR    # Clear RX_TMO_FLG
            nRet |= NPSC2106Reg.CMT2300A_MASK_RX_TMO_EN     # Return RX_TMO_FLG by RX_TMO_EN

        if NPSC2106Reg.CMT2300A_MASK_TX_DONE_FLG & nFlag2:
            nClr1 |= NPSC2106Reg.CMT2300A_MASK_TX_DONE_CLR
            nRet |= NPSC2106Reg.CMT2300A_MASK_TX_DONE_EN

        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_INT_CLR1, nClr1)
        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_INT_CLR2, nClr2)

        if nIntPolar:
            nRet = ~nRet

        return nRet

    def CMT2300A_SoftReset(self):
        """
        Soft reset.
        """
        self.CMT2300A_WriteReg(0x7F, 0xFF)

    def CMT2300A_GetChipStatus(self):
        """
        Get the chip status.

        Returns:
        CMT2300A_STA_PUP
        CMT2300A_STA_SLEEP
        CMT2300A_STA_STBY
        CMT2300A_STA_RFS
        CMT2300A_STA_TFS
        CMT2300A_STA_RX
        CMT2300A_STA_TX
        CMT2300A_STA_EEPROM
        CMT2300A_STA_ERROR
        CMT2300A_STA_CAL
        """
        reg = self.CMT2300A_ReadReg(
            NPSC2106Reg.CMT2300A_CUS_MODE_STA) & NPSC2106Reg.CMT2300A_MASK_CHIP_MODE_STA

        return reg

    def CMT2300A_AutoSwitchStatus(self, nGoCmd):
        """
        Auto switch the chip status, and 10 ms as timeout.

        Args:
        nGoCmd: the chip next status

        Returns:
        TRUE or FALSE
        """
        nWaitStatus = 0
        if nGoCmd == NPSC2106Reg.CMT2300A_GO_SLEEP:
            nWaitStatus = NPSC2106Reg.CMT2300A_STA_SLEEP
        elif nGoCmd == NPSC2106Reg.CMT2300A_GO_STBY:
            nWaitStatus = NPSC2106Reg.CMT2300A_STA_STBY
        elif nGoCmd == NPSC2106Reg.CMT2300A_GO_TFS:
            nWaitStatus = NPSC2106Reg.CMT2300A_STA_TFS
        elif nGoCmd == NPSC2106Reg.CMT2300A_GO_TX:
            nWaitStatus = NPSC2106Reg.CMT2300A_STA_TX
        elif nGoCmd == NPSC2106Reg.CMT2300A_GO_RFS:
            nWaitStatus = NPSC2106Reg.CMT2300A_STA_RFS
        elif nGoCmd == NPSC2106Reg.CMT2300A_GO_RX:
            nWaitStatus = NPSC2106Reg.CMT2300A_STA_RX

        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_MODE_CTL, nGoCmd)
        # nBegTick = self.CMT2300A_GetTickCount()

        # while self.CMT2300A_GetTickCount() - nBegTick < 10:
        self.CMT2300A_DelayMs(10)

        if nWaitStatus == self.CMT2300A_GetChipStatus():

            return True

        if nGoCmd == NPSC2106Reg.CMT2300A_GO_TX:
            self.CMT2300A_DelayMs(1)
            if NPSC2106Reg.CMT2300A_MASK_TX_DONE_FLG & self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_INT_CLR1):
                return True

        if nGoCmd == NPSC2106Reg.CMT2300A_GO_RX:
            self.CMT2300A_DelayMs(1)
            if NPSC2106Reg.CMT2300A_MASK_PKT_OK_FLG & self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_INT_FLAG):
                return True

        return False

    def CMT2300A_GoTx(self):
        return self.CMT2300A_AutoSwitchStatus(NPSC2106Reg.CMT2300A_GO_TX)

    def CMT2300A_GoSleep(self):
        """
        Entry SLEEP mode.

        Returns:
        TRUE or FALSE
        """
        return self.CMT2300A_AutoSwitchStatus(NPSC2106Reg.CMT2300A_GO_SLEEP)

    def CMT2300A_GoStby(self):
        """
        Entry Sleep mode.

        Returns:
        TRUE or FALSE
        """
        return self.CMT2300A_AutoSwitchStatus(NPSC2106Reg.CMT2300A_GO_STBY)

    def CMT2300A_SetInterruptPolar(self, bActiveHigh):
        tmp = self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_INT1_CTL)

        if bActiveHigh:
            tmp &= ~NPSC2106Reg.CMT2300A_MASK_INT_POLAR
        else:
            tmp |= NPSC2106Reg.CMT2300A_MASK_INT_POLAR

        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_INT1_CTL, tmp)

    def CMT2300A_ClearTxFifo(self):
        tmp = self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_FIFO_FLAG)
        self.CMT2300A_WriteReg(
            NPSC2106Reg.CMT2300A_CUS_FIFO_CLR, NPSC2106Reg.CMT2300A_MASK_FIFO_CLR_TX)
        return tmp

    def CMT2300A_EnableWriteFifo(self):
        tmp = self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_FIFO_CTL)
        tmp |= NPSC2106Reg.CMT2300A_MASK_SPI_FIFO_RD_WR_SEL
        tmp |= NPSC2106Reg.CMT2300A_MASK_FIFO_RX_TX_SEL
        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_FIFO_CTL, tmp)

    def CMT2300A_ConfigRegBank(self, base_addr, bank, length):
        for i in range(length):
            self.CMT2300A_WriteReg(i + base_addr, bank[i])
        return True

    def CMT2300A_ConfigGpio(self, nGpioSel):

        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_IO_SEL, nGpioSel)

    def CMT2300A_RFConfig(self):

        self.CMT2300A_ConfigGpio(NPSC2106Reg.CMT2300A_GPIO3_SEL_INT2)

        nInt2Sel = NPSC2106Reg.CMT2300A_INT_SEL_TX_DONE
        nInt2Sel &= NPSC2106Reg.CMT2300A_MASK_INT2_SEL
        nInt2Sel |= (~NPSC2106Reg.CMT2300A_MASK_INT2_SEL) & self.CMT2300A_ReadReg(
            NPSC2106Reg.CMT2300A_CUS_INT2_CTL)
        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_INT2_CTL, nInt2Sel)
        self.CMT2300A_EnableLfosc(False)
        self.CMT2300A_GoSleep()

    def CMT2300A_ConfigBankReg(self):
        # Config registers */
        self.CMT2300A_ConfigRegBank(
            NPSC2106Reg.CMT2300A_CMT_BANK_ADDR, g_cmt2300aCmtBank, NPSC2106Reg.CMT2300A_CMT_BANK_SIZE)
        self.CMT2300A_ConfigRegBank(NPSC2106Reg.CMT2300A_SYSTEM_BANK_ADDR,
                                    g_cmt2300aSystemBank, NPSC2106Reg.CMT2300A_SYSTEM_BANK_SIZE)
        self.CMT2300A_ConfigRegBank(NPSC2106Reg.CMT2300A_FREQUENCY_BANK_ADDR,
                                    g_cmt2300aFrequencyBank, NPSC2106Reg.CMT2300A_FREQUENCY_BANK_SIZE)
        self.CMT2300A_ConfigRegBank(NPSC2106Reg.CMT2300A_DATA_RATE_BANK_ADDR,
                                    g_cmt2300aDataRateBank, NPSC2106Reg.CMT2300A_DATA_RATE_BANK_SIZE)
        self.CMT2300A_ConfigRegBank(NPSC2106Reg.CMT2300A_BASEBAND_BANK_ADDR,
                                    g_cmt2300aBasebandBank, NPSC2106Reg.CMT2300A_BASEBAND_BANK_SIZE)
        self.CMT2300A_ConfigRegBank(
            NPSC2106Reg.CMT2300A_TX_BANK_ADDR, g_cmt2300aTxBank, NPSC2106Reg.CMT2300A_TX_BANK_SIZE)
        
    @keyword
    def set_freq_tx(self, freq):
        pass

    @keyword
    def set_datarate(self, dr):
        pass

    @keyword
    def set_power(self, power):
        if(power == 'MAX'):
            ConfigName = "CMT2300Config_20dbm.exp"
        elif(power == 'MIN'):
            ConfigName = "CMT2300Config_-30dbm.exp"
        else:
            ConfigName = "CMT2300Config_"+str(power)+"dbm.exp"
        self.CMT2300A_GetConfig(ConfigName)
        print(ConfigName)
        # self.CMT2300A_ConfigBankReg()
        pass

    @keyword
    def start_tramsmit(self):
        self.CMT2300A_Init()
 
        self.CMT2300A_ConfigBankReg()

        tmp = (~0x07) & self.CMT2300A_ReadReg(NPSC2106Reg.CMT2300A_CUS_CMT10)
        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_CMT10, tmp | 0x02)
        self.CMT2300A_RFConfig()

        TxBufStr = '1234567890'
        self.CMT2300A_GoStby()
        self.CMT2300A_ClearInterruptFlags()
        self.CMT2300A_ClearTxFifo()
        self.CMT2300A_WriteReg(NPSC2106Reg.CMT2300A_CUS_PKT15, len(TxBufStr))
        self.CMT2300A_EnableWriteFifo()

        self.CMT2300A_WriteFifo(TxBufStr)
        self.CMT2300A_GoTx()
        time.sleep(1)
        self.CMT2300A_ClearInterruptFlags()
        self.CMT2300A_GoTx()
        time.sleep(1)
        # self.CMT2300A_GoTx()
        # for i in range(100):
        #     self.CMT2300A_GoTx()
        #     time.sleep(1)
        #     self.CMT2300A_ClearInterruptFlags()
        #     # self.CMT2300A_GoSleep()
        # pass


if __name__ == '__main__':
    my_npsc2106 = NPSC2106Driver()
    my_npsc2106.set_power(20)
    # my_npsc2106.CMT2300A_GetConfig("CMT2300Config_13dbm_434.exp")
    my_npsc2106.start_tramsmit()
