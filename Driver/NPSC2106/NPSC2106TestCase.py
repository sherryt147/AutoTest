import NPSC2106.NPSC2106Driver as NPSC2106Driver
import Instrument.AgilentN9020A as AgilentN9020A
import pandas as pd
import time,datetime
from robot.api.deco import keyword



SaveExcelfile_name = "PowerTestExcel"+time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())).replace(":", "-")+ ".xlsx"


class NPSC2106TestCase:
    def __init__(self):
        self.my_npsc2106 = NPSC2106Driver.NPSC2106Driver()
        self.myN9020A = AgilentN9020A.AgilentN9020A()
        
        pass
    
    def getPoweraverage(self,num=5):
        # myN9020A = AgilentN9020A.AgilentN9020A()
        power = []
        for n in range(num):
            power.append(self.myN9020A.getChannelPower())
        power_ave = sum(power) / num
        print('Power :', power_ave)
        return power_ave
    
    @keyword
    def TestPowerStep(self):
        # Set Npsc2106 Transmit  Power (-30dBm~20dBm)

        # Set AgilentN9020A
        self.myN9020A.setCentralFreqMHz(470)
        self.myN9020A.setSpanMHz(10)
        self.myN9020A.setReferenceLevelDBM(20)
        df = pd.DataFrame(columns=['设定功率', '实际功率', '偏差值'])
        for i in range(-30,21,1):
            self.my_npsc2106.set_power(i)
            self.my_npsc2106.start_tramsmit()
            power = self.getPoweraverage()
            new_data = {'设定功率': i, '实际功率': power, '偏差值': i-power}
            df = df.append(new_data, ignore_index=True)
            df.to_excel(SaveExcelfile_name, index=False)
        
        


if __name__ == '__main__':  
    my_testcase = NPSC2106TestCase()
    my_testcase.TestPowerStep()
