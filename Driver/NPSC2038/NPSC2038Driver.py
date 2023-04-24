import BoardDriver.SerialLibrary as SerialLibrary
import time
from robot.api.deco import keyword


DriverPort = 'COM14'
DriverBaudrate = 115200

FSK_76800_SF0_TXBUF = ['0xC7','0x2D','0x55','0xDC']

FSK_9600_SF0_LEN20_TXBUF = [
    '0xEF','0xF2','0x9D','0x5C','0x90','0xD3','0xEF','0x52','0xBA','0xAD',
    '0xEB','0xBD','0xE0','0xBC','0xE4','0x98','0xAA','0x4A','0x1E','0xC0']

FSK_9600_SF0_TXBUF = [
    '0xD4','0x9E','0xE4','0x8C','0x9C','0x60','0xE8','0xD6',
    '0xC3','0x84','0xC7','0xE7','0x26','0xD3','0x88','0x14',
    '0x17','0xDA','0x5D','0xA1','0x63','0xF9','0x0D','0x82',
    '0xFA','0x79','0x39','0x10','0xB7','0x46','0x65','0x81',
    '0xE7','0x21','0xBE','0x70','0x5B','0x04','0xE3','0xBE',
    '0xBE','0x58','0xC3','0x72','0xE4','0x2B','0xCE','0xCA',
    '0xBE','0x73','0x94','0x17','0x18','0xAC','0x7F','0x68',
    '0x57','0x6F','0x6A','0x9A','0x11','0x58','0x85','0xB4',
    '0x59','0xBE','0xAE','0xEC','0x63','0xDD','0x51','0x5F',
    '0xED','0x7D','0xC6','0x02','0x19','0x30','0xF1','0x60',
    '0x2C','0x38','0x0F','0xB1','0x32','0xAD','0x4A','0x42',
    '0xAA','0x30','0x5E','0xDB','0xD6','0x9E','0xF7','0xFC',
    '0x93','0x3C','0x79','0xC7','0x8C','0x2D','0x1E','0x7B',
    '0xE4','0x04','0xA7','0x6C','0x75','0x71','0x5C','0x7B',
    '0x49','0x42','0xBF','0xDF','0x5E','0x54','0xAD','0xD6',
    '0xA6','0x7E','0x49','0xDE','0xC4','0x9C','0x87','0x43',
    '0x22','0x15','0x1E','0xFF','0xD7','0xDC','0x35','0x59',
    '0x42','0x47','0xDA','0x38','0x39','0xD2','0x06','0xB7',
    '0xB8','0x2D','0xE5','0x6C','0x45','0xC9','0xC9','0xC7',
    '0x66','0xC2','0xA0','0x0F','0xB4','0xB6','0x93','0xE7',
    '0x59','0xB5','0x18','0xFF','0x36','0xED','0xB0','0x31',
    '0xC4','0x33','0x5A','0x5A','0x98','0xED','0x53','0xF3',
    '0x85','0x6E','0x49','0x2B','0xCF','0x73','0xDA','0x8B',
    '0xDC','0x20','0x3B','0x65','0xF9','0xF5','0xDE','0x35',
    '0x6D','0xAB','0x87','0x3C','0xBD','0xCC','0x5B','0x40',
    '0x97','0xD0','0xD7','0x83','0x0F','0x33','0x05','0xBA',
    '0x2C','0x9E','0x53','0xC6','0xCA','0xD9','0xC6','0x1B',
    '0x02','0xEC','0xE6','0xE0','0x45','0xBC','0x13','0x89',
    '0x8E','0x34','0x40','0xFD','0x30','0x77','0xC0','0x0B',
    '0xF0','0x44','0x59','0xBD','0x32','0x6A','0x4A','0xD0',
    '0x66','0x2E','0xA8','0xDC','0x00','0x91','0xAC','0xAD',
    '0xFF','0x9C',
]
#reg Map
CFG_PHR0_REG = 0x1a
CFG_SEL1_REG = 0x0e

#NPSC2038 驱动
class NPSC2038Driver:
    def __init__(self):
        self.my_serial = SerialLibrary.SerialLibrary(DriverPort,DriverBaudrate)
        self.write_RF_reg(0x1A,0x00)
        self.read_RF_reg(0x1A)
        self.write_RF_reg(0x01,0x89)
        self.read_RF_reg(0x01)
        self.write_RF_reg(0x06,0x04)
        self.read_RF_reg(0x6)
        self.write_RF_reg(0x09,0xfc)
        self.read_RF_reg(0x9)

    @keyword
    def chip_reset(self):
        self.write_BB_reg(0x01,0x5A)
        self.write_BB_reg(0x01,0xA5)    
        pass
    @keyword
    def chip_close(self):
        self.write_RF_reg(0x01,0x00)
        self.write_RF_reg(0x02,0x0)    
        #2mA@3.3V
        pass
    @keyword
    def set_mode(self,mode):
        module = 0
        if(mode == 'FSK'):
            module = 1
        elif(mode == 'MSK'):
            module = 0
        elif(mode == 'GFSK'):
            module = 3
        elif(mode == 'GMSK'):
            module = 2
        else:
            return False
        cfg = self.read_BB_reg(CFG_PHR0_REG)
        new_cfg = (int(cfg,16) & 0xE3) | (module << 2)  # 将2-4位修改为mode的值
        self.write_BB_reg(CFG_PHR0_REG,new_cfg)
        return True
    
    def get_mode(self):
        module = ''
        cfg = self.read_BB_reg(CFG_PHR0_REG)
        new_mode = (int(cfg,16) & ~0xE3) >>2  #取出2：4位数值
        if(new_mode == 0x00):
           module = 'MSK'
        elif(new_mode == 0x01):
           module = 'FSK' 
        elif(new_mode == 0x02):
           module = 'GMSK' 
        elif(new_mode == 0x03):
           module = 'GFSK' 
        else:
            module = 'Error:'+str(new_mode)
        print('芯片模式处于'+module)
        return module

    @keyword
    def set_sf(self,sf):
        
        return True

    @keyword
    def set_coderate(self,cr):
        
        return True
    def set_Spread_Spectrum(self,ss=0):
        #0:关闭
        cfg = self.read_BB_reg(0x1d)
        new_cfg = (int(cfg,16) & 0x0F)|(ss<<4)  
        self.write_BB_reg(0x1d,new_cfg)
        self.read_BB_reg(0x1d)
        pass
    def set_fifo_size(self,size):
        size_h = size>>8
        size_l = size - (size_h<<8)
        print('Size Value',size_h,size_l)
        cfg = self.read_BB_reg(0x1d)
        new_cfg = (int(cfg,16) & 0xF0)|(size_h) 
        self.write_BB_reg(0x1d,new_cfg)
        cfg = self.read_BB_reg(0x1e)
        new_cfg = (int(cfg,16) & 0x00)|(size_l) 
        self.write_BB_reg(0x1e,new_cfg)
        return 
    def set_fifo_value(self,size):
        txbuf = ''
        for i in range(size):
            txbuf  = txbuf+ str(55)
        self.write_BB_fifo(txbuf)
        return

    @keyword
    def set_datarate(self,dr = '76.8'):
        tmp = 0   
        filter_width = 0 #0:200KHz  1:500KHz
        if(dr == '9.6'):         
            tmp = 0
        elif(dr == '19.2'):      
            tmp = 1
        elif(dr == '38.4'):      
            tmp = 2
        elif(dr == '76.8'):
            if(self.get_mode()=='FSK'):
                filter_width = 1
            tmp = 3
        elif(dr == '153.6'):
            filter_width = 1
            tmp = 4
        elif(dr == '307.2'):
            filter_width = 1
            tmp = 5
        cfg = self.read_RF_reg(0x06)
        new_cfg = (int(cfg,16) & 0xFB) | (filter_width)  
        self.write_RF_reg(0x06,new_cfg)
        cfg = self.read_BB_reg(CFG_SEL1_REG)
        new_cfg = (int(cfg,16) & 0xF8) | (tmp)  
        self.write_BB_reg(CFG_SEL1_REG,new_cfg)
        return True
    
    @keyword
    def set_freq_tx(self,frequency):
        """
        设置频率

        参数：
        frequency：float，频率，单位为MHz

        返回：
        None
        """
        
        if isinstance(frequency, str):
            try:
                frequency = float(frequency)
            except ValueError:
                print("Input is not a valid number.")
                return None
        elif not isinstance(frequency, (int, float)):
            print("Input type is not supported.")
            return None
        # 分频比 TX 默认为1
        driver = 1
        # 乘以2和8
        frequency *= 2 * 8
        
        # 循环除以2，直到小于4000
        while frequency > 4000:
            frequency /= 2.0
            driver = driver +1
        print("driver:",driver)
        print("frequency:",frequency)

        # 计算N和F
        N_F = frequency / 24.579/2
        print(f"N_F = {N_F}")
        N = int(N_F)
        F = round((N_F - N) * 2**20)

        # 将F转换为3个字节的16进制值
        F_hex = hex(F)[2:].zfill(6)
        F1 = int(F_hex[0:2], 16)
        F2 = int(F_hex[2:4], 16)
        F3 = int(F_hex[4:6], 16)

        # 输出结果
        print(f"设置频率为 {frequency:.6f} MHz")
        print(f"N = {N}")
        print(f"F1 = {F1}")
        print(f"F2 = {F2}")
        print(f"F3 = {F3}")
                
        self.write_RF_reg(0x12,0x8A)#分频比
        time.sleep(0.1)
        self.write_RF_reg(0x12,(driver+0x0C))#分频比
        self.write_RF_reg(0xA,N)#
        self.write_RF_reg(0xD,F1)#
        self.write_RF_reg(0xC,F2)#
        self.write_RF_reg(0xB,F3)#
        
        for i in range(0x1f, -1, -1):
            # 写寄存器0xf
            self.write_RF_reg(0xf, i)
            time.sleep(0.05)
            # 读取寄存器0x0E
            reg_0x0E = self.read_RF_reg(0x0E)

            # 判断读取的值是否是0x40或者0x41，如果是则跳出循环
            if reg_0x0E == '40' :
                break
            if reg_0x0E == '41' :
                break
        #0x12,0x0A,0x0B,0x0C,0x0D,0x0f 0x0E
        return True
    @keyword
    def set_freq_rx(self,frequency):
        """
        设置频率

        参数：
        frequency：float，频率，单位为MHz

        返回：
        None
        """
        
        if isinstance(frequency, str):
            try:
                frequency = float(frequency)
            except ValueError:
                print("Input is not a valid number.")
                return None
        elif not isinstance(frequency, (int, float)):
            print("Input type is not supported.")
            return None
        
        # 分频比 
        driver = 0
        # 乘以2和8
        frequency *= 2 * 8
        
        # 循环除以2，直到小于4000
        while frequency > 4000:
            frequency /= 2.0
            driver = driver +1
        print("driver:%d",driver)
        print("frequency:%d",frequency)

        # 计算N和F
        N_F = frequency / 24.579/2
        print(f"N_F = {N_F}")
        N = int(N_F)
        F = round((N_F - N) * 2**20)

        # 将F转换为3个字节的16进制值
        F_hex = hex(F)[2:].zfill(6)
        F1 = int(F_hex[0:2], 16)
        F2 = int(F_hex[2:4], 16)
        F3 = int(F_hex[4:6], 16)

        # 输出结果
        print(f"设置频率为 {frequency:.6f} MHz")
        print(f"N = {N}")
        print(f"F1 = {F1}")
        print(f"F2 = {F2}")
        print(f"F3 = {F3}")
                
        self.write_RF_reg(0x12,0x8A)#分频比
        time.sleep(0.1)
        self.write_RF_reg(0x12,(driver+0x0C))#分频比
        self.write_RF_reg(0xA,N)#
        self.write_RF_reg(0xD,F1)#
        self.write_RF_reg(0xC,F2)#
        self.write_RF_reg(0xB,F3)#
        
        for i in range(0x1f, -1, -1):
            # 写寄存器0xf
            self.write_RF_reg(0xf, i)
            time.sleep(0.05)
            # 读取寄存器0x0E
            reg_0x0E = self.read_RF_reg(0x0E)

            # 判断读取的值是否是0x40或者0x41，如果是则跳出循环
            if reg_0x0E == '40' :
                break
            if reg_0x0E == '41' :
                break
        #0x12,0x0A,0x0B,0x0C,0x0D,0x0f 0x0E
        return True
    @keyword
    def set_power(self,power,voltage=0x00,Mixer=1):
        #0x08,0x09,0x16
        #09 MAX 2E   08 MAX 5F
        # 09 Min E0 , C0,80,40,
        v08_list = [0xFC,0x38,0x9C,0xF0,0x90,0x68,0xE4,0xC8,0xA4,0x2C,0x68,0xC,0xDC,0xF0,0x64,0xF4,0xB8,0x9C,0x4,0xE0,0xFC,0x88,0x40,0x58,0x20,0x0,0x6C,0x5C,0x60,0xAC,0x40,0x44,0x20,0x44,0x54,0x10,0x44,0x50,0x30,0x2C,0x34,0x4C,0x1C,0x2C,0x14,0x1C,0x2C,0x40,0x60,0xE0,0x20,0xC,0x80,0x24,0x8,0x80,0x60,0x80,0x40,0x4,0x0]
        v09_list = [0x3E,0x2,0xFE,0xDE,0x3E,0xE2,0xFE,0xE,0x22,0x32,0xEE,0xFE,0x3C,0x1C,0xFE,0xDC,0x2C,0xDC,0xFE,0x32,0x0,0x1C,0x2,0xCC,0xD2,0x2,0xFC,0x0,0xFE,0x20,0x32,0xC,0xE,0x3C,0xC0,0xDC,0xCC,0xF0,0x30,0x10,0xF0,0xE0,0xD0,0xC0,0x20,0xE0,0xE0,0xC,0x2C,0xF0,0xC,0xF0,0x0,0xC0,0xC0,0x20,0x30,0xF0,0x10,0xD0,0xCC]
        v16_list = [0x3,0x3,0xC,0xC,0xC,0x3,0x3,0xC,0x3,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0x3,0xC,0xC,0x3,0xC,0x3,0x3,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC,0xC]
        if(power == 'MAX'):
            self.write_RF_reg(0x08,0xFF)
            self.write_RF_reg(0x09,0xBE)
            self.write_RF_reg(0x16,0x03)
            
        elif(power == 'MIN'):
            self.write_RF_reg(0x08,0x00)
            self.write_RF_reg(0x09,0xCC)
            self.write_RF_reg(0x16,0x0C)
        elif(isinstance(power,str)):
            try:
                pwr = int(power,16)
                print('是字符串转换为hex：',hex(pwr))
                self.write_RF_reg(0x08,pwr)
                self.write_RF_reg(0x09,Mixer)
                self.write_RF_reg(0x16,voltage)
            except:
                print('转换失败输入非hex',power)
                return False       
        else:
            i = 20-power
            if(i > len(v08_list)):
                print('Set Power Error:',power)
                return False
            self.write_RF_reg(0x08,v08_list[i])
            self.write_RF_reg(0x09,v09_list[i])
            self.write_RF_reg(0x16,v16_list[i])
        return True
        # self.write_RF_reg(0x16,0x0C)
        # self.write_RF_reg(0x09,0xE0)
        # self.write_RF_reg(0x08,0x00)

        
    @keyword
    def start_tramsmit(self):
        self.write_RF_reg(0x01,0x81)
        self.write_RF_reg(0x02,0x7F)
        self.write_BB_reg(0x0f,0x01)
        self.set_Spread_Spectrum()
        self.set_fifo_size(20)
        # self.write_BB_fifo('687853A8')
        self.set_fifo_value(20)
        self.write_BB_reg(0x11,0x40)
        self.write_BB_reg(0xd,0x20)
        # self.write_BB_reg(0x1e,0x04)
        # self.write_BB_reg(0x11,0x40)
        # self.write_BB_fifo('687853A8')
        # self.write_BB_reg(0xD,0x20)
        #新版FPGA
        # self.write_BB_reg(0x7e,0x00)
        # self.write_BB_reg(0x3,0x18)
        # self.write_BB_reg(0x4,0x01)
        # self.write_BB_reg(0xf,0x24)
        # self.write_BB_reg(0x12,0x00)
        # self.write_BB_reg(0x13,0x04)
        # self.write_BB_reg(0x06,0x40)
        # self.write_BB_fifo('687853A8')
        # self.write_BB_reg(0x2,0x02)
        # self.write_BB_reg(0x2,0x20)
        
        return True
    
    @keyword
    def start_receive(self):
        self.write_RF_reg(0x1A,0x01)
        self.write_RF_reg(0x1,0xff)
        self.write_RF_reg(0x2,0x8B)
        self.write_RF_reg(0x10,0x34)
        # self.write_RF_reg(0x12,0x88)
        # self.write_RF_reg(0x12,0x0C)
        # self.write_RF_reg(0xA,0x48)
        # self.write_RF_reg(0xD,0x08)
        # self.write_RF_reg(0xC,0x46)
        # self.write_RF_reg(0xB,0x68)
        # self.write_RF_reg(0xF,0x16)
        self.write_RF_reg(0x5,0x17)
        self.write_RF_reg(0x6,0xf)
        self.write_RF_reg(0x6,0xee)
        self.write_RF_reg(0x7,0x3f)

        reg = self.read_RF_reg(0x0e)#40
        if(reg != '40'):
            print('RF Error:0x0E:',reg)
        
        return True
    
    @keyword
    def receive_done(self):
        #37:error 17 :ok   低2位
        tmp = self.read_BB_reg(0x5B)
        # print(tmp,'\r\n')
        if(tmp == 0x17):
            print('接收全部正确')
            return 100
        
        self.write_BB_fifosize(str(len(FSK_9600_SF0_LEN20_TXBUF)))
        readv = self.read_BB_fifo(len(FSK_9600_SF0_LEN20_TXBUF))
        for i in range(len(FSK_9600_SF0_LEN20_TXBUF)):
            if FSK_9600_SF0_LEN20_TXBUF[i] != readv[i]:
                print(f'Byte {i} does not match')
                return '{:.2f}'.format(i/len(FSK_9600_SF0_LEN20_TXBUF))                
            if i == len(FSK_9600_SF0_LEN20_TXBUF)-1:
                print('All Match')
                return 100

    @keyword
    def delay_ms(self, time_s):
        if isinstance(time_s, str):
            try:
                time_s = float(time_s)
            except ValueError:
                print("Input is not a valid number.")
                return None
        elif not isinstance(time_s, (int, float)):
            print("Input type is not supported.")
            return None
        time_ms = int(time_s/1000)
        time.sleep(time_ms)

    def chip_BB_Reset(self):
        
        self.write_BB_reg(0x01,0x5A)
        self.write_BB_reg(0x01,0xA5)      
        return True
    @keyword
    def read_RF_reg(self,addr):
        # 将addr和value转换为16进制，并加上前缀0x
        addr_hex = hex(addr)[2:].zfill(2)
        # 拼接AT+WRITERF=指令字符串
        command = "AT+READRF=" + addr_hex +"\r\n"
        self.my_serial.write_to_serial(command)
        readstr = self.my_serial.read_from_serial()
        data_str = readstr.split(":")[1].strip()
        print("Read RF Reg:",addr_hex,":",data_str)
        return data_str
    def write_RF_reg(self,addr,value):
        # 将addr和value转换为16进制，并加上前缀0x
        addr_hex = hex(addr)[2:].zfill(2)
        value_hex = hex(value)[2:].zfill(2)
        print("Write RF Reg:",addr_hex,":",value_hex)
        # 拼接AT+WRITERF=指令字符串
        command = "AT+WRITERF=" + addr_hex + value_hex+"\r\n"
        self.my_serial.write_to_serial(command)
        self.my_serial.read_from_serial()
        return True
    @keyword
    def read_BB_reg(self,addr):
        # 将addr和value转换为16进制，并加上前缀0x
        addr_hex = hex(addr)[2:].zfill(2)
        # 拼接AT+WRITERF=指令字符串
        command = "AT+READBB=" + addr_hex +"\r\n"
        self.my_serial.write_to_serial(command)
        readstr = self.my_serial.read_from_serial()
        data_str = readstr.split(":")[1].strip()
        print("Read BB Reg:",addr_hex,":",data_str)
        return data_str
    def write_BB_reg(self,addr,value):
        # 将addr和value转换为16进制，并加上前缀0x
        addr_hex = hex(addr)[2:].zfill(2)
        value_hex = hex(value)[2:].zfill(2)
        print("Write BB Reg:",addr_hex,":",value_hex)
        # 拼接AT+WRITERF=指令字符串
        command = "AT+WRITEBB=" + addr_hex + value_hex+"\r\n"
        self.my_serial.write_to_serial(command)
        self.my_serial.read_from_serial()
        return True
    def write_BB_fifosize(self,value):
        # 拼接AT+WRITERF=指令字符串
        command = "AT+FIFOSIZEBB=" + value+"\r\n"
        print(command)
        print("Write Fifo Size:",value)
        self.my_serial.write_to_serial(command)
        read = self.my_serial.read_from_serial()
        print(read)
        return True
    def write_BB_fifo(self,value):
        # 拼接AT+WRITERF=指令字符串
        command = "AT+FIFOWRITEBB=" + value+"\r\n"
        print(command)
        self.my_serial.write_to_serial(command)
        read = self.my_serial.read_from_serial()
        print(read)
        return True

    def read_BB_fifo(self,size):
        # 拼接AT+WRITERF=指令字符串
        cnt = int(size/8)+1
        command = "AT+FIFOREADBB=\r\n"
        self.my_serial.write_to_serial(command)
        rv = self.my_serial.read_from_serial()
        print('The First:',rv,cnt)
        hex_all = []
        for i in range(cnt):
            readstr = self.my_serial.read_from_serial()
            # data_str = readstr.split(":")[1].strip()
            hex_array = ['0x' + x for x in readstr.split()]
            hex_all = hex_all+hex_array
            print(readstr)
        print(hex_all)
        return hex_all
    def test_223_TX(self):
        self.write_RF_reg(0x1A,0x00)
        self.write_RF_reg(0x1,0x89)
        self.write_RF_reg(0x06,0x04)
        self.write_RF_reg(0x09,0xfc)
        self.write_RF_reg(0x12,0x8A)
        self.write_RF_reg(0x12,0x0D)
        self.write_RF_reg(0xA,0x48)
        self.write_RF_reg(0xD,0x09)
        self.write_RF_reg(0xC,0x51)
        self.write_RF_reg(0xB,0x0A)
        self.write_RF_reg(0xF,0x15)
        self.write_BB_reg(0x0f,0x02)
        self.write_BB_reg(0x1e,0x04)
        self.write_BB_reg(0x11,0x40)
        self.write_BB_fifo('12345678')
        self.write_BB_reg(0xd,0x20)
    #76.8Kbps
    def test_223_200K_RX(self):
        self.write_RF_reg(0x1A,0x01)
        self.write_RF_reg(0x1,0xff)
        self.write_RF_reg(0x2,0x8B)
        self.write_RF_reg(0x10,0x34)
        self.write_RF_reg(0x12,0x88)
        self.write_RF_reg(0x12,0x0C)
        self.write_RF_reg(0xA,0x48)
        self.write_RF_reg(0xD,0x08)
        self.write_RF_reg(0xC,0x46)
        self.write_RF_reg(0xB,0x68)
        self.write_RF_reg(0xF,0x16)
        self.write_RF_reg(0x5,0x17)
        self.write_RF_reg(0x6,0xf)
        self.write_RF_reg(0x6,0xee)
        self.write_RF_reg(0x7,0x3f)

        reg = self.read_RF_reg(0x0e)#40
        if(reg != '40'):
            print('RF Error:0x0E:',reg)

        self.write_BB_reg(0xe,0x1B)
        self.write_BB_reg(0xf,0x02)
        self.write_BB_reg(0x1a,0x26)
        self.write_BB_reg(0x1d,0x00)
        

        self.write_BB_reg(0x46,0x00)
        self.write_BB_reg(0x47,0x10)
        self.write_BB_reg(0x48,0x00)
        self.write_BB_reg(0x49,0x00)
        #enter Rx
        self.write_BB_reg(0xd,0x2)
        self.write_BB_reg(0xd,0x10)

    def test_223_9600_RX(self):
        self.write_RF_reg(0x1A,0x01)
        self.write_RF_reg(0x1,0xff)
        self.write_RF_reg(0x2,0x8B)
        self.write_RF_reg(0x10,0x34)
        self.write_RF_reg(0x12,0x88)
        self.write_RF_reg(0x12,0x0C)
        self.write_RF_reg(0xA,0x48)
        self.write_RF_reg(0xD,0x08)
        self.write_RF_reg(0xC,0x46)
        self.write_RF_reg(0xB,0x68)
        self.write_RF_reg(0xF,0x16)
        self.write_RF_reg(0x5,0x17)
        self.write_RF_reg(0x6,0xf)
        self.write_RF_reg(0x6,0xd)
        self.write_RF_reg(0x7,0x3f)

        reg = self.read_RF_reg(0x0e)#40
        if(reg != '40'):
            print('RF Error:0x0E:',reg)

        self.set_datarate('9.6')
        self.write_BB_reg(0xf,0x01)
        self.write_BB_reg(0x1a,0x24)
        self.write_BB_reg(0x1d,0x00)
        

        self.write_BB_reg(0x46,0x00)
        self.write_BB_reg(0x47,0x10)
        self.write_BB_reg(0x48,0x00)
        self.write_BB_reg(0x49,0x00)
        #enter Rx
        self.write_BB_reg(0xd,0x2)
        self.write_BB_reg(0xd,0x10)

    def test_223_200K_RX_FPGA(self):
        self.write_RF_reg(0x1A,0x01)
        self.write_RF_reg(0x1,0xff)
        self.write_RF_reg(0x2,0x8B)
        self.write_RF_reg(0x10,0x34)
        self.write_RF_reg(0x12,0x88)
        self.write_RF_reg(0x12,0x0C)#可以换成08试试，可以关掉，关掉对纹波的处理
        self.write_RF_reg(0xA,0x48)
        self.write_RF_reg(0xD,0x08)
        self.write_RF_reg(0xC,0x46)
        self.write_RF_reg(0xB,0x68)
        self.write_RF_reg(0xF,0x16)
        self.write_RF_reg(0x5,0x17)
        self.write_RF_reg(0x6,0xf)
        self.write_RF_reg(0x6,0xd)
        self.write_RF_reg(0x7,0x39)

        tmp = self.read_RF_reg(0x0e)#40
        if(tmp != 40):
            print('Error:',tmp)
        self.write_BB_reg(0x7e,0x00)
        self.write_BB_reg(0x3,0x18)
        self.write_BB_reg(0x4,0x01)
        self.write_BB_reg(0xf,0x24)
        self.write_BB_reg(0x12,0x00)
        self.write_BB_reg(0x34,0x02)

        self.write_BB_reg(0x31,0x00)
        self.write_BB_reg(0x32,0x02)
        tmp = self.read_BB_reg(0x32)
        if(tmp == 0x02):
            print('Write OK')
        self.write_BB_reg(0x33,0x00)

        self.write_BB_reg(0x06,0x89)


        self.write_BB_reg(0xe,0x1B)
        self.write_BB_reg(0xf,0x02)
        self.write_BB_reg(0x1a,0x26)
        self.write_BB_reg(0x1d,0x00)
        
        #enter Rx
        self.write_BB_reg(0x2,0x2)
        self.write_BB_reg(0x2,0x10)

    def SetRxMode(self):
        #new Chip 第二版
        self.write_BB_reg(0x7e,0x00)#切页

        self.write_BB_reg(0x06,0x89)
        self.write_BB_reg(0x2,0x2)
        self.write_BB_reg(0x2,0x10)

    # 芯片第二版
    def test_223_rx_done(self):
        #37:error 17 :ok   低2位
        tmp = self.read_BB_reg(0x5B)
        print(tmp,'\r\n')
        
        self.write_BB_fifosize(str(len(FSK_9600_SF0_LEN20_TXBUF)))
        readv = self.read_BB_fifo(len(FSK_9600_SF0_LEN20_TXBUF))
        for i in range(len(FSK_9600_SF0_LEN20_TXBUF)):
            if FSK_9600_SF0_LEN20_TXBUF[i] != readv[i]:
                print(f'Byte {i} does not match')
                return -1
            if i == len(FSK_9600_SF0_LEN20_TXBUF)-1:
                print('All Match')
                return 0

    def test_223_rx_done_FPGA(self):
        self.write_BB_reg(0x7e,0x01)#切页
        tmp = self.read_BB_reg(0x18)
        print(tmp,'\r\n')
        
        self.write_BB_fifosize('250')
        readv = self.read_BB_fifo(250)
        for i in range(len(FSK_9600_SF0_TXBUF)):
            if FSK_9600_SF0_TXBUF[i] != readv[i]:
                print(f'Byte {i} does not match')
                return -1
            if i == (len(FSK_9600_SF0_TXBUF)-1):
                print('All Match')
                return 0
           
            
    def test_RF_RX_Config(self):
        # 03  80 00 C0 40
        # 03 
        self.write_RF_reg(0x03,0xC0)
        return
            
if __name__ == '__main__':            
    my_npsc2038 = NPSC2038Driver()
    # my_npsc2038.chip_BB_Reset()
    # my_npsc2038.chip_close()
    # my_npsc2038.chip_BB_Reset()
    # # my_npsc2038.set_fifo_value(1000)
    # my_npsc2038.set_freq_tx(223)
    # # # # my_npsc2038.set_power(0x00,0x0C,0xFC)
    # my_npsc2038.set_power(0,0x03,0xe0)
    my_npsc2038.set_power('68',12,0xee)
    # # # my_npsc2038.set_mode('FSK')
    # # # my_npsc2038.set_datarate('9.6')
    my_npsc2038.write_RF_reg(0x01,0x89)
    my_npsc2038.write_RF_reg(0x02,0xFF)
    # my_npsc2038.start_tramsmit()   

    # my_npsc2038.close_Spread_Spectrum()
    # my_npsc2038.set_fifo_size(1000)
    # my_npsc2038.test_223_TX()
    # my_npsc2038.write_RF_reg(0x03,0xBF)
    # my_npsc2038.write_RF_reg(0x04,0xFF)
    # my_npsc2038.test_223_200K_RX()
    # my_npsc2038.set_freq_rx(430)
    # my_npsc2038.start_receive()
    # my_npsc2038.write_RF_reg(0x01,0x45)
    # my_npsc2038.write_RF_reg(0x02,0x00)
    # time.sleep(5)
    # my_npsc2038.test_223_rx_done()
    # my_npsc2038.test_223_200K_RX_FPGA()
    # my_npsc2038.SetRxMode()
    # print('Config Ok\r\n')
    # time.sleep(5)
    # my_npsc2038.test_223_rx_done_FPGA()
    # cpt  = my_npsc2038.read_BB_fifo()
    # list1 = [0x0,0x3]
    # delist = []
    # for i in list1:
    #     for c in range(2):
    #         for p in range(2):
    #             for pc in range(2):
    #                 for t in list1:
    #                     delist.append(i<<6|c<<5|p<<4|t<<2|pc<<1)
    # print(delist,len(delist))








