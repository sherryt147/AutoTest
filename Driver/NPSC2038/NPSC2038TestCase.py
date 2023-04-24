import NPSC2038Driver
import Instrument.AgilentN9020A as AgilentN9020A
import Instrument.KeysightSMBV100A as KeysightSMBV100A
import pandas as pd
import time,datetime
from robot.api.deco import keyword


SaveExcelfile_name = "PowerTestExcel"+time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())).replace(":", "-")+ ".xlsx"


class NPSC2038TestCase:
    def __init__(self):
        try:
            self.my_npsc2038 = NPSC2038Driver.NPSC2038Driver()
            self.myN9020A = AgilentN9020A.AgilentN9020A()
            self.mySMV100A = KeysightSMBV100A.KeysightSMBV100A()
        except:
            print('Error In NPSC2038TestCase Init')
        pass
    
    def getPoweraverage(self,num=5):
        # myN9020A = AgilentN9020A.AgilentN9020A()
        power = []
        for n in range(num):
            power.append(self.myN9020A.getChannelPower())
        power_ave = sum(power) / num
        print('Power :', power_ave)
        return power_ave

    def TestPowerStep_All2Excel(self):
        # Set Npsc2038 Transmit  Power (-40dBm~20dBm)
        dec_pwrlist = [-40,-37,-34,-31,-28,-25,-22]
        for dec in range(-20,20,1):
            dec_pwrlist.append(dec)
        print(dec_pwrlist)
        # self.my_npsc2038.set_mode('FSK')
        # self.my_npsc2038.set_datarate('38.4')
        self.my_npsc2038.set_freq_tx(223)
        self.my_npsc2038.set_power(1)
        # self.my_npsc2038.write_BB_fifo('12345678')
        # self.my_npsc2038.start_tramsmit()
        # Set AgilentN9020A
        self.myN9020A.setCentralFreqMHz(223)
        self.myN9020A.setSpanMHz(10)
        self.myN9020A.setReferenceLevelDBM(20)
        df = pd.DataFrame(columns=['0x16寄存器值', 'Mix校准(0x09)', 'VC值', 'PA值', 'Power'])
        # df.to_excel('test_power.xlsx', index=False)  0xE0, 0xC0, 0xA0,0x80, 0x60,
        lis16 = [0x0,0xc,0x3, 0x8,0x2]
        lis09 = [0, 12, 2, 14, 16, 28, 18, 30, 32, 44, 34, 46, 48, 60, 50, 62, 
                 192, 204, 194, 206, 208, 220, 210, 222, 224, 236, 226, 238, 240, 252, 242, 254]
        for n in lis16:#0x16 (C,8,4,0,1,2,3)
            for v09 in lis09:#0x09 
                for i in range(8):
                    tmp = i << 5
                    for c in range(0,32,4):#0x08
                        self.my_npsc2038.set_power(c | tmp, n, v09)
                        power = self.getPoweraverage()+0.5
                        new_data = {'0x16寄存器值': n, 'Mix校准(0x09)': v09, 'VC值': tmp, 'PA值': c, 'Power': power}
                        df = df.append(new_data, ignore_index=True)
                        df.to_excel(SaveExcelfile_name, index=False)
                        
    @keyword
    def TestPowerStep_20dBm(self,rf_loss = 0):
        dec_pwrbase = -20
        pwr_sum = 0
        self.my_npsc2038.chip_BB_Reset()
        self.my_npsc2038.set_freq_tx(223)
        # self.my_npsc2038.start_tramsmit()
        self.myN9020A.setCentralFreqMHz(223)
        self.myN9020A.setSpanMHz(10)
        self.myN9020A.setReferenceLevelDBM(20)
        for i in range(41):           
            self.my_npsc2038.set_power(dec_pwrbase+i)
            power = self.getPoweraverage()+rf_loss
            pwr_diffance = power - (dec_pwrbase+i)
            print('设定发射功率为:',(dec_pwrbase+i),'实际发射功率为:',power,'误差:',pwr_diffance)   
            pwr_sum = pwr_sum +     abs(pwr_diffance)         
        return pwr_sum/41

        
    @keyword
    def TestPowerStep_Minus20dBm(self,rf_loss = 0):
        dec_pwrlist = [-40,-37,-34,-31,-28,-25,-22]
        pwr_sum = 0
        self.my_npsc2038.chip_BB_Reset()
        self.my_npsc2038.set_freq_tx(223)
        # self.my_npsc2038.start_tramsmit()
        self.myN9020A.setCentralFreqMHz(223)
        self.myN9020A.setSpanMHz(10)
        self.myN9020A.setReferenceLevelDBM(-10)
        for i in range(len(dec_pwrlist)):           
            self.my_npsc2038.set_power(dec_pwrlist[i])
            power = self.getPoweraverage()+rf_loss
            pwr_diffance = power - dec_pwrlist[i]
            print('设定发射功率为:',dec_pwrlist[i],'实际发射功率为:',power,'误差:',pwr_diffance)   
            pwr_sum = pwr_sum +     abs(pwr_diffance)         
        return pwr_sum/len(dec_pwrlist)
    
    @keyword
    def TestSensibility(self):
        for i in range(10):
            self.mySMV100A.preConfiguration(-85+i,223)
            self.mySMV100A.setIqWv("'/var/user/fsk9600_nzc32_ncs2_sf0_12cc_len20B.wv'")
            self.my_npsc2038.chip_BB_Reset()
            self.my_npsc2038.test_223_9600_RX()
            self.mySMV100A.executeTrigger()
            time.sleep(1)
            tmp = self.my_npsc2038.test_223_rx_done()
            if tmp == 0:
                print("当前灵敏度为：",-105+i-3.5)
                return
            


if __name__ == '__main__':  
    my_testcase = NPSC2038TestCase()
    # my_testcase.TestPowerStep_20dBm()
    # my_testcase.TestPowerStep_Minus20dBm()
    my_testcase.TestSensibility()
    # my_testcase.myN9020A.
    print('Test End')
    #powerStepText()
    # my_smbv = ksMBV.KeysightSMBV100A()
    # my_smbv.preConfiguration(-90,223)
    # my_npsc2038 = NSCP2038Driver.NSCP2038Driver()
    # my_npsc2038.test_223_200K_RX_FPGA()
    # my_npsc2038.write_RF_reg(0x07,0x39)
    # # my_npsc2038.write_BB_reg(0x31,0x00)
    # # my_npsc2038.write_BB_reg(0x32,0x00)
    # # my_npsc2038.write_BB_reg(0x33,0x10)

    # my_npsc2038.SetRxMode()
    # # print('Config Ok\r\n')
    # my_smbv.executeTrigger()
    # time.sleep(0.5)
    # my_npsc2038.write_BB_reg(0x7e,0x00)
    # my_npsc2038.write_BB_reg(0x2,0x2)
    # time.sleep(1)
    # my_npsc2038.test_223_rx_done_FPGA()
    # my_npsc2038.read_RF_reg(0x02)
    # my_npsc2038.read_RF_reg(0x05)
    # my_npsc2038.write_BB_reg(0x7e,0x00)
    # my_npsc2038.write_BB_reg(0x01,0x5a)
    # my_npsc2038.write_BB_reg(0x01,0xa5)
    # my_npsc2038.read_BB_reg(0x01)

