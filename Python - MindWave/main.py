## Imagination Machine 2.0 by Clara Leivas, 2018 
## licensed under CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/

import serial
import time
import sys
from mindwave import mindwave
from plot import plot

## Global Variables ##
plotterPort = 0 
mwPort = 0 

freData = [0 for x in range(8)]
preFreData = [0 for x in range(8)] 
freDif = [[0 for x in range(10)] for y in range(8)]
freAv = [0 for x in range(8)] 
difCount = 0

## Functions ##
def init_plotter():                  #initialize serial connection
    global plotterPort                      #must be declared in each function
    plotterPort = serial.Serial()
    plotterPort.baudrate = 115200
    plotterPort.port = "/dev/cu.usbmodem14211"

    plotterPort.timeout = 1
    plotterPort.open()

    if plotterPort.isOpen():
        print("Open: " + plotterPort.name)
        
        time.sleep(3)
        while plotterPort.in_waiting:
            print(plotterPort.readline())
            
        plotterPort.write("g90 g0 \r\n".encode())
        time.sleep(1)
        while plotterPort.in_waiting:
            print(plotterPort.readline())
        
    else:
        print("Port not open")
        
# def init_pumps():
        
def init_mw():                  #initialize serial connection
    global mwPort                      #must be declared in each function
    mwPort = serial.Serial()
    mwPort.baudrate = 9600
    mwPort.port = "/dev/cu.MindWave"
    mwPort.timeout = 1
    mwPort.open()

    if mwPort.isOpen():
        print("Open: " + mwPort.name)
    else:
        print("Port not open")
        
        
def getDif():
    global difCount
    for i in range(8):
        freDif[i][difCount] = abs(freData[i] - preFreData[i])
        #print(freData[i])
        #print(preFreData[i])
        #print(freDif[i][difCount])
        
    print(difCount)
        
    difCount+=1
    if difCount >=10:
            difCount = 0

def getAv():
    for i in range(8):
        s = 0
        for j in range(10):
            s +=  freDif[i][j]
        freAv[i] = s/10
    print(freAv)
    
def close():
    mwPort.flushInput()
    mwPort.flushOutput()
    mwPort.close()
    
    plotterPort.flushInput()
    plotterPort.flushOutput()
    plotterPort.close()
    
    sys.exit()
    
    
        
#####SETUP################################################
init_plotter()
init_mw()

#####MAIN#################################################
if __name__ == '__main__':
    mw = mindwave(mwPort)
    p = plot(plotterPort)
    
    initTime = 10
    for i in range(0, initTime):
        mw.run()
        print(i)
        
    runTime = 30
    i = 0
    while 1:
        mw.run()
        
        if mw.newEEG and i<runTime:
            freData[0] = mw.delta
            freData[1] = mw.theta
            freData[2] = mw.low_alfa
            freData[3] = mw.high_alfa
            freData[4] = mw.low_beta
            freData[5] = mw.high_beta
            freData[6] = mw.low_gamma
            freData[7] = mw.mid_gamma
            
            if i>0:
                getDif()
            if i>10:
                getAv()
                p.draw(freAv[1],freAv[2],freAv[3],freAv[4],freAv[5] )
                
            preFreData = freData[:]
            i+=1
            
        elif i>=runTime:
            p.reset()
            close()
    
    
