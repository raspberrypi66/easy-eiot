import smbus2 as smbus  
import time

class Hs300x(object):
    i2c_address=0x44
    def __init__(self,bus):
        self.bus = bus

    def isAvailable(self):
        try:
            self.bus.write_byte(self.i2c_address,0x00)
            return True
        except IOError:
            return False

    def MeasurementReq(self):

        self.bus.write_quick(self.i2c_address)
        time.sleep(0.01)

        read=smbus.i2c_msg.read(self.i2c_address,4)
        time.sleep(0.1)
        self.bus.i2c_rdwr(read)
        result=list(read)
        rawHumidMSB=result[0]
        rawHumid=result[1]
        rawHumid=(rawHumidMSB<<8)+rawHumid

        rawTempMSB = result[2]
        rawTemp = result[3]
        rawTemp =((rawTempMSB <<8)+rawTemp)

        rawStatus=rawTemp >> 14

        rawTemp=rawTemp >> 2

        if(rawHumid == 0x3FFF): return 0

        if(rawTemp  == 0x3FFF): return 0

        self._humidity=(rawHumid & 0x3FFF)*0.006163516
        self._temperature=(rawTemp * 0.010071415) - 40
        return rawStatus+1

    def getHumidity(self):
        return self._humidity 

    def getTemperature(self):
        return self._temperature

def main():
    bus=smbus.SMBus(1)
    hsSensor = Hs300x(bus)
    while(1):
        if(hsSensor.MeasurementReq()):
            print(hsSensor.getHumidity())
            print(hsSensor.getTemperature())
     
        time.sleep(1)

if __name__ == "__main__":
    main()
