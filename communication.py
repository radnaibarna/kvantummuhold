from abc import ABC, abstractmethod
import random
import atmosModell as atm


class Communicator(ABC): # a kommunikáló feleket modellező absztakt osztály
    def __init__(self, lat, lon):
        self.lon=lon 
        self.lat=lat
        self.athmoshpere=""
        self.name=""
        self.sector=""
        self.sentmessages=[]
        self.recievedmessages=[]
        self.Qber=0
    def AddAir(self, athmosphere):
        self.athmosphere=athmosphere

    def sendRadioBroadcast(self, message):
        pass

    def recieveRadioBroadcast(self, message):
        pass
    
    def AddName(self, name):
        self.name=name

    def AddSector(self, s):
        self.sector=s
    
    def GetLat(self):
        return self.lat

    def GetLon(self):
        return self.lon
    
class GroundStation(Communicator):
    def __init__(self, lat, lon, zenit, IsSecond):
        super().__init__(lat, lon)
        self.zenit=zenit
        self.IsSecond=IsSecond
        self.Bob=""
        self.recievedqubits=[]
        self.recievedbits=[]
        self.usedbases=[]
        self.correctbits=[]
        self.keybits=[]
    
    def AddAir(self, athmoshpere):
        self.athmoshpere=athmoshpere
        

    def sendRadioBroadcast(self, message):
        self.athmoshpere.BroadcastGroundToSatellite(message)
        self.sentmessages.append(message)

    def recieveRadioBroadcast(self, message):
        self.recievedmessages.append(message)
        if(message[0]=="matchingbases"):
            self.SetCorrectBits(message[1])
        elif(message[0]=="xoredkey"):
            self.recievedmessages.append(message)
            self.MakeKey(message[1])

    def MakeKey(self, xoredkey=0):
        if(self.IsSecond==0):
            if(len(self.correctbits)<256):
                self.keybits=self.correctbits
            else:
                key=[]
                for i in range(255):
                    key.append(self.correctbits[i])
                self.keybits=key
        elif(self.IsSecond==1):
            key=[]
            if(len(self.correctbits)<256):
                self.keybits=self.correctbits
            else:
                for i in range(255):
                    xoredbit=self.correctbits[i] ^ xoredkey[i]
                    key.append(xoredbit)
                self.keybits=key
        print(self.keybits)
    


    def SetCorrectBits(self, correctindexes):
        for i in correctindexes:
            self.correctbits.append(self.recievedbits[i])
        if(self.IsSecond==0):
            self.MakeKey()

    def AddName(self, name):
        self.name=name

    def AddSector(self, s):
        self.sector=s

    def RecieveQubit(self, q):
        if(q=="qubit lost"):
            return 0
        else:
            self.recievedqubits.append(q)
            a=random.randint(0,1)
            self.MeasureQubit(q, a)
            return 1
        

    def MeasureQubit(self, photon, base):
        measuredbyte=photon.Measure(base)
        self.usedbases.append(base)
        self.recievedbits.append(measuredbyte)
        pass

    def AddBob(self, Bob):
        self.Bob=Bob

    def isSecond(self):
        return self.IsSecond

    def SendMeasuredBases(self):
        message=[]
        message.append("usedbases")
        message.append(self.usedbases)
        #if(self.isSecond()==1):

        self.sendRadioBroadcast(message)

    def CheckParity(self, firstbit, secondbit):
        i=firstbit
        ones=0
        while(i<secondbit):
            if(self.correctbits[i]==1):
                ones+=1
            i+=1
        if(ones%2==1):
            return 0
        else:
            return 1
        

    def Reconcilation(self):
        for i in range(3):
            firstbit=random.randint(0,245)
            secondbit=firstbit+10
            parity=self.CheckParity(firstbit, secondbit)
            message=[]
            message.append("paritycheck")
            message.append(parity)
            message.append(firstbit)
            message.append(secondbit)
            self.sendRadioBroadcast(message)

    def PrintInfo(self):
        print("------------------------------")
        print(self.name)
        print("Mért bitek: ", self.recievedbits)
        print("Használt bázisok: ", self.usedbases)
        print("tényleges kulcs: ", self.correctbits)
        print("kulcs mérete: ", len(self.correctbits))
        print("végleges kulcs: ", self.keybits)

    

class Satellite(Communicator):
    def __init__(self, lat, lon, height, speed):
        super().__init__(lat, lon)
        self.height=height
        self.speed=speed
        self.FirstBaseQubits=[]
        self.FirstBaseBits=[]
        self.FirstCorrectBits=[]
        self.FirstBaseBases=[]
        self.SecondBaseQubits=[]
        self.SecondBaseBits=[]
        self.SecondCorrectBits=[]
        self.SecondBaseBases=[]
        self.GroundMeasurebases=[]
        self.FirstAllSentQubits=0
        self.SecondAllSentQubits=0

    def getHeight(self):
        return self.height
    
    def AddAir(self, athmoshpere):
        self.athmoshpere=athmoshpere

    def sendRadioBroadcast(self, message):
        self.athmoshpere.BroadcastSatelliteToGround(message)
        self.sentmessages.append(message)

    def recieveRadioBroadcast(self, message):
        if(message[0]=="usedbases"):
            self.recievedmessages.append(message)
            self.GroundMeasurebases=message[1]
        elif(message[0]=="paritycheck"):
            self.recievedmessages.append(message)
            self.CheckParity(message)

    def CheckParity(self, message):
        i=message[2]
        ones=0
        if(self.athmoshpere.IsSecond()==0):
            while(i<message[3]):
                if(self.FirstCorrectBits[i]==1):
                    ones+=1
                i+=1
            if(ones%2==message[1]):
                print("Eve valószínűleg jelen volt")
            else:
                print("Eve valószínűleg nem volt jelen")
        elif(self.athmoshpere.IsSecond()==1):
            while(i<message[3]):
                if(self.SecondCorrectBits[i]==1):
                    ones+=1
                i+=1
            if(ones%2==message[1]):
                print("Eve valószínűleg jelen volt")
            else:
                print("Eve valószínűleg nem volt jelen")
        

    def AddName(self, name):
        self.name=name

    def AddSector(self, s):
        self.sector=s

    def CompareLists(self, list_a, list_b):
        matching_indexes=[]
        if(len(list_a)<len(list_b)):
            for i in range(len(list_a)):
                if(list_a[i]==list_b[i]):
                    matching_indexes.append(i)
        else:
            for i in range(len(list_b)):
                if(list_a[i]==list_b[i]):
                    matching_indexes.append(i)

        return matching_indexes
        

    def SendMatchingBases(self):
        if(self.athmoshpere.IsSecond()==0):
            matchindexes=self.CompareLists(self.GroundMeasurebases, self.FirstBaseBases)
            self.Qber=float(len(matchindexes))/float(len(self.FirstBaseBits))
        else:
            matchindexes=self.CompareLists(self.GroundMeasurebases, self.SecondBaseBases)
            #self.Qber=float(len(matchindexes))/float(len(self.SecondBaseBits))
        for i in matchindexes:
            if(self.athmoshpere.IsSecond()==0):
                self.FirstCorrectBits.append(self.FirstBaseBits[i])
            else:
                self.SecondCorrectBits.append(self.SecondBaseBits[i])
        message=[]
        message.append("matchingbases")
        message.append(matchindexes)
        self.sendRadioBroadcast(message)


    def GenerateQubit(self):
        value=random.randint(0,1)
        measurebase=random.randint(0,1)
        qubit=Photon(measurebase, value)
        if(self.athmoshpere.IsSecond()==0):
            self.FirstBaseBases.append(measurebase)
            self.FirstBaseBits.append(value)
        elif(self.athmoshpere.IsSecond()==1):
            self.SecondBaseBases.append(measurebase)
            self.SecondBaseBits.append(value)
        return qubit

        
    def SendQubit(self, n): # A qubitküldést menedzselő osztály
        remaining=self.SendAmountOfQubit(n)
        sumofsentqubits=n
        while(remaining>0):
            remaining=self.SendAmountOfQubit(remaining)
            sumofsentqubits+=remaining
        if(self.athmoshpere.IsSecond()==0):
            self.FirstAllSentQubits=sumofsentqubits
        elif(self.athmoshpere.IsSecond()==1):
            self.SecondAllSentQubits=sumofsentqubits
            

    def SendAmountOfQubit(self, amount):
        remaining=amount
        for i in range(amount):
            qubit=self.GenerateQubit()
            succes=self.athmoshpere.SendQubit(qubit)
            
            if(succes==1):
                remaining=remaining-1
                if(self.athmoshpere.IsSecond()==0):
                    self.FirstBaseQubits.append(qubit)
                elif(self.athmoshpere.IsSecond()==1):
                    self.SecondBaseQubits.append(qubit)
            else:
                if(self.athmoshpere.IsSecond()==0):
                    del self.FirstBaseBases[-1]
                    del self.FirstBaseBits[-1]
                elif(self.athmoshpere.IsSecond()==1):
                    del self.SecondBaseBases[-1]
                    del self.SecondBaseBits[-1]
        return remaining
            
    def SendXORedKey(self):
        xored=[]
        if(len(self.FirstCorrectBits)>=256 and len(self.SecondCorrectBits)>=256):
            for i in range(255):
                xored.append(self.FirstCorrectBits[i] ^ self.SecondCorrectBits[i])
            message=[]
            message.append("xoredkey")
            message.append(xored)
            self.sendRadioBroadcast(message)
        else:
            print("nincs elég rendelkezésre álló bit a titkos kulcs létrehozásához")
            

    def printInfo(self):
        sourcefile=open(self.name+".txt", 'w')
        print("------------------------------")
        print(self.name)
        if(self.athmoshpere.IsSecond()==0):
            print("generált bitek: ", self.FirstBaseBits)
            print("használt bázisok: ", self.FirstBaseBases)
            print("tényleges kulcs: ", self.FirstCorrectBits)
            print("kulcs mérete: ", len(self.FirstCorrectBits))
            print("összesen elküldött qubitek száma: ", self.FirstAllSentQubits)
            
        else:
            print("generált bitek: ", self.SecondBaseBits)
            print("használt bázisok: ", self.SecondBaseBases)
            print("tényleges kulcs: ", self.SecondCorrectBits)
            print("kulcs mérete: ", len(self.SecondCorrectBits))
            print("összesen elküldött qubitek száma: ", self.SecondAllSentQubits)
        print("Qber: ", self.Qber)
        sourcefile.close()


class Air:
    def __init__(self, name, IsEve=0, season="summer", weather="clear"):
        self.transmittancy=float(1)
        self.gs=""
        self.sat=""
        self.IsEve=IsEve
        self.name=name
        self.season=season
        self.weather=weather
    
    def SetSatellite(self, s):
        self.sat=s

    def SetGroundStation(self, gs):
        self.gs=gs

    def SetTransmittancy(self):
        weather=0
        season=0
        if(self.season=="summer"):
            season=5
        elif(self.season=="winter"):
            season=8
        
        if(self.weather=="clear"):
            weather=11
        elif(self.weather=="hazy"):
            weather=14
        self.transmittancy=1-atm.allLoss(self.gs.zenit, self.sat.height, season, weather)
    
    def SendQubit(self, photon):
        f=random.random()
        if(f<=self.transmittancy):
            if(self.IsEve==0):
                succes=self.gs.RecieveQubit(photon)
                return succes
            else:
                base=random.randint(0,1)
                gotvalue=photon.Measure(base)
                fakephoton=Photon(base, gotvalue)
                succes=self.gs.RecieveQubit(fakephoton)
                return succes
        else:
            succes=self.gs.RecieveQubit("qubit lost")
            return succes

    def BroadcastSatelliteToGround(self, message):
        """print("\n")
        print("Satellite->Groundstation")
        print("     ", message)
        print("\n")"""
        self.gs.recieveRadioBroadcast(message)

    def BroadcastGroundToSatellite(self, message):
        """print("\n")
        print("Groundstation->Satellite")
        print("     ", message)
        print("\n")"""
        self.sat.recieveRadioBroadcast(message)

    def IsSecond(self):
        return self.gs.isSecond()



class Photon:
    def __init__(self, base, value):
        self.base=base
        self.value=value

    def Measure(self, base):
        if(base==self.base):
            return self.value
        else:
            return random.randint(0,1)
        pass


"""groundstation=GroundStation(lat=0.1, lon=0.1, zenit=30, IsSecond=0)
satellite=Satellite(lat=0, lon=1, height=500, speed=1000)
air=Air(IsEve=1)

groundstation.AddAir(air)
satellite.AddAir(air)
air.SetGroundStation(groundstation)
air.SetSatellite(satellite)
satellite.SendQubit(100)
groundstation.SendMeasuredBases()
satellite.SendMatchingBases()
groundstation.PrintInfo()
satellite.printInfo()"""


false 