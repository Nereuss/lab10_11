from machine import Pin, TouchPad
from tcs34725 import *
from machine import Pin, I2C
from time import ticks_ms
import dht

sensor = dht.DHT11(Pin(17))
sensor.measure()
temp = sensor.temperature()
hum = sensor.humidity()

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

r_led = Pin(18, Pin.OUT)
y_led = Pin(5, Pin.OUT)
g_led = Pin(16, Pin.OUT)
interval = 100
state = 0
prev_time = 0
r = TouchPad(Pin(27))
y = TouchPad(Pin(2))
g = TouchPad(Pin(4))

#1.1
class dht_sensor:
    description = "Class to store temp and humidity"
    def __init__(self):
        self.dhtLog = []
    def set_logString(self, temp:int, hum:int):
        self.dhtLog.append("\nTemp: " + str(temp) + " - Humidity: " + str(hum))
    #1.3 Prints all the logged dhtLogs if there are more recordings
    def printDhtLog(self):
        print(*self.dhtLog)
        
#2.1 - 2.2
class rgb_sensor:
    def __init__(self):
        self.rgbLog = []
    def tupleToList(self, data):
        return list(data)
    def set_logString(self, data):
        # Formating tuple to list
        rgb = list(data)
        # We need to convert the float values to string which can be done by str() and then we can plus it together
        self.rgbLog.append("\nRed: " + str(rgb[0]) + " - Green: " + str(rgb[1]) + " - Blue: " + str(rgb[2]))
    def printRgbLog(self):
        # Prints all the logged colors if there are more recordings
        print(*self.rgbLog)
    
def sensorCheck(cTime, state):
    prev_time = cTime
    if state == 1:
        state = 0   
    else:
        state = 1

# initiate a objects of classes
dhtSensor = dht_sensor()
rgbSensor = rgb_sensor()
      
print(dht_sensor.description)

# 1.2 - 1.3
dhtSensor.set_logString(temp, hum)
# second reading
dhtSensor.set_logString(temp, hum)
# 1.3 Will print the whole list if there are multiple recordings
dhtSensor.printDhtLog()



if i2c.scan() !=[]:
    sensor = TCS34725(i2c)
    sensor.gain(60)
    data = sensor.read(True)
    print(html_rgb(data))
    
    #2.2
    print(rgbSensor.tupleToList(html_rgb(data)))
    rgbSensor.set_logString(html_rgb(data))
    rgbSensor.printRgbLog()

#3.1 - 3.2
while True:
    # Set to global so Sensor check function grab it from the while loop
    currentTime = time.ticks_ms()
    # Wanted to not repeat code somehow but was at this time not sure how and was in a rush
    # Maybe it would be best to pass if else to a funct so it would not have to be repeated
    if (r.read() < 200 and currentTime - prev_time > interval):
        prev_time = currentTime
        if state == 1:
            state = 0
            print(r.read())   
        else:
            state = 1
        r_led.value(state)
    
    if (y.read() < 200 and currentTime - prev_time > interval):
        prev_time = currentTime
        if state == 1:
            state = 0
            print(y.read())   
        else:
            state = 1
        y_led.value(state)
    
    if (g.read() < 200 and currentTime - prev_time > interval):
        prev_time = currentTime
        if state == 1:
            state = 0
            print(g.read())   
        else:
            state = 1
        g_led.value(state) 
    
    start_time = time.ticks_ms()







