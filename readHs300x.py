import smbus2 as smbus
import time
import hs300x

bus=smbus.SMBus(1)
hsSensor = hs300x.Hs300x(bus)
print(hsSensor.isAvailable())
while(1 and hsSensor.isAvailable()):
    if(hsSensor.MeasurementReq()):
        print("Humidity : "+str(hsSensor.getHumidity()))
        print("Temperature : "+str(hsSensor.getTemperature()))

    time.sleep(1)

