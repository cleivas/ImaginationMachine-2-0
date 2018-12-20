## Imagination Machine 2.0 by Clara Leivas, 2018 
## licensed under CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/

# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-



class mindwave:
    SYNC = 0xAA
    EXCODE = 0x55
    EEG_POW = 0x83 
    EEG_POW_LENGTH = 24
    RAW = 0x80
    RAW_LENGTH = 2
    ATTENTION = 0x04
    MEDITATION = 0x05
    POOR_SIGNAL = 0x02

    def __init__(self, mwserial):
        self.mw = mwserial
        self.payload = bytearray(255)

        self.delta = 0
        self.theta = 0
        self.low_alfa = 0
        self.high_alfa = 0
        self.low_beta = 0
        self.high_beta = 0
        self.low_gamma = 0
        self.mid_gamma = 0
        
        self.meditation = 0
        self.attention = 0
        self.poor_signal = 0


    def run(self):
        self.newEEG = False
        self.newMeditation = False
        self.newAttention = False
        self.getPayload()

    def getPayload(self):
        # step 1 - check sync byte
        if self.readByte('i') == self.SYNC:
            # step 2 - check sync byte
            if self.readByte('i') == self.SYNC:

                # step 3 - check payload length
                payloadLength = self.readByte('i')
                if payloadLength > 169:
                    print("Payload length too long ...")
                    return

                # step 4 - accumulate sum of payload bytes
                checksumAccumilator = 0
                for i in range(0, payloadLength):
                    self.payload[i] = self.readByte('i')
                    checksumAccumilator += self.payload[i]

                # step 5 - compare checksum and accumulated checksum
                checksum = self.readByte('i')
                checksumAccumilator &= 255 #Same as constrain csa to 255, and csa=255-ccsa
                checksumAccumilator = ~checksumAccumilator & 255
                #print("checksumAccumilator:{}".format(checksumAccumilator))
                #print("checksum:{}".format(checksum))

                # parse payload data if everything is OK
                if checksum == checksumAccumilator:
                    self.parse(payloadLength, self.payload)
            else:
                print("Trying to Sync ...")
        else:
            print("Trying to Sync ...")


    def parse(self, payLoadLength, payload):
        pll = payLoadLength
        #print("Payload length:{}".format(pll))
        #print("Good to go, let's parse!")

        i=0
        while i<pll: # if code byte is equal to 0x83 it's the eeg band power data, next byte is length of data set. Otherwise length is 1 byte
            #print(hex(payload[i]))
            
            if payload[i] == self.RAW:
                i+=1
                if payload[i] == self.RAW_LENGTH:
                    #Here's where you'd get the raw data
                    #But for now let's skip over those two bytes
                    i+=self.RAW_LENGTH
                    i+=1
                    
            elif payload[i] == self.POOR_SIGNAL:
                #print("checking signal")
                i+=1
                self.poor_signal = payload[i]
                #print(self.poor_signal)
                if self.poor_signal > 2:
                    print("POOR SIGNAL ...")
                    i=pll
                if self.poor_signal == 200:
                    print("Headset not touching skin")
                    
            elif payload[i] == self.EEG_POW:
                i += 1
                length = payload[i]
                print("EEG POW")
                if length == self.EEG_POW_LENGTH:
                    self.getBandAmplitudes(i, length)
                    i+=self.EEG_POW_LENGTH
                    i+=1
                else:
                    print("Error in EEG POW length")
                    
            elif payload[i] == self.ATTENTION:
                i += 1
                if payload[i]>0 and payload[i]<101:
                    self.attention = payload[i]
                    #print("Attention value:{}")
                    #print(payload[i])
                    i+=1
                    self.newAttention = True
                    print("Attention       :{}".format(self.attention))
                    
            elif payload[i] == self.MEDITATION:
                i += 1
                if payload[i]>0 and payload[i]<101:
                    self.meditation = payload[i]
                    #print("Meditation value:{}")
                    #print(payload[i])
                    i+=1
                    self.newMeditation = True
                    print("Meditation       :{}".format(self.meditation))

            else:
                i+=1
                #print("no useful data")

    def getBandAmplitudes(self, start_index, length):
        si = start_index
        l = length
        #print("length:{}".format(l))
        #print("getting band amplitudes")

        j=si
        self.delta = (self.payload[j]<<16)+(self.payload[j+1]<<8)+self.payload[j+2]
        j+=3
        self.theta = (self.payload[j]<<16)+(self.payload[j+1]<<8)+self.payload[j+2]
        j+=3
        self.low_alfa = (self.payload[j]<<16)+(self.payload[j+1]<<8)+self.payload[j+2]
        j+=3
        self.high_alfa = (self.payload[j]<<16)+(self.payload[j+1]<<8)+self.payload[j+2]
        j+=3
        self.low_beta = (self.payload[j]<<16)+(self.payload[j+1]<<8)+self.payload[j+2]
        j+=3
        self.high_beta = (self.payload[j]<<16)+(self.payload[j+1]<<8)+self.payload[j+2]
        j+=3
        self.low_gamma = (self.payload[j]<<16)+(self.payload[j+1]<<8)+self.payload[j+2]
        j+=3
        self.mid_gamma = (self.payload[j]<<16)+(self.payload[j+1]<<8)+self.payload[j+2]
        j+=3

        if l!=j-si:
            print("Something went wrong when converting EEG band Power values")
        else:
            self.newEEG = True
            #print("New correct data available!")

        
        print("Delta        :{}".format(self.delta))
        print("Theta        :{}".format(self.theta))
        print("Low Alfa     :{}".format(self.low_alfa))
        print("High Alfa    :{}".format(self.high_alfa))
        print("Low Beta     :{}".format(self.low_beta))
        print("High Beta    :{}".format(self.high_beta))
        print("Low Gamma    :{}".format(self.low_gamma))
        print("Mid Gamma    :{}".format(self.mid_gamma))
        




    def readByte(self, return_type):
        inByte = self.mw.read()
        inInt = int.from_bytes(inByte, byteorder='little')  # convert to int
        inHex = hex(inInt)  # convert to hex
        #print(inHex,)

        if return_type == 'b':
            return inByte
        elif return_type == 'i':
            return inInt
        elif return_type == 'h':
            return inHex
        else:
            return -10



