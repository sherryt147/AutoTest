import serial
import sys
from robot.api.deco import keyword
import serial.tools.list_ports

def check_port(port):
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if p.device == port:
            return True
    return False


class SerialLibrary:
    def __init__(self, port, baudrate):
        if check_port(port):
            self.ser = serial.Serial(port=port, baudrate=baudrate)
            if self.ser.is_open:
                print("串口已成功打开")
            else:
                print("串口已被占用")
                sys.exit ()
        else:
            print("未找到",port,"，请检查串口是否存在")
            sys.exit ()
        # self.ser = serial.Serial(port=port, baudrate=baudrate)
        # 检查串口是否已经被占用
        # if self.ser.is_open:
        #     raise ValueError("串口已经被占用！")

        # # 尝试打开串口，若失败则提示错误信息并退出程序
        # try:
        #     self.ser.open()
        # except serial.SerialException as e:
        #     print("无法打开串口 {}: {}".format(self.ser.name, e))
        #     sys.exit(1)

        # # 检查串口是否已经成功打开
        # if not self.ser.is_open:
        #     raise ValueError("无法打开串口 {}！".format(self.ser.name))
            
        # print("成功打开串口 {}，波特率为 {}。".format(self.ser.name, baudrate))

        

    @keyword
    def read_from_serial(self):
        return self.ser.readline().decode().strip()

    @keyword
    def write_to_serial(self, message):
        self.ser.write(message.encode())


