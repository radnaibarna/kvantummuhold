import random
import math
import communication as comm


class Realizator:
    def __init__(self, satellite, g1, g2):
        self.satellite=satellite
        self.g1=g1
        self.g2=g2
        self.route=""
    def SetRoute(self): # az útvonal inicializálása 2 földi állomás között
        self.route=Route()
        self.route.Calculate(self.g1, self.g2, self.satellite) # az útvonal létrehozása
        pass
    def BB84_firststation(self): #BB84 a műhold és az első földi állomás között
        pass
    def BB84_secondstation(self): #BB84 a műhold és a második földi állomás között
        pass
    def Simulate(self): # a teljes útvonal szimulálása
        pass
    

class Route:
    def __init__(self): 
        self.length=0
        self.sector1=Sector()
        self.sector1.setname("Szektor 1")
        self.sector2=Sector()
        self.sector2.setname("Szektor 2")
        self.sector3=Sector()
        self.sector3.setname("Szektor 3")
        self.sector4=Sector()
        self.sector4.setname("Szektor 4")
        self.fulltime=0
    def Calculate(self, g1, g2, s): #úthossz kiszámítása, szektorok kijelölése
        distance_of_stations=CalculateDistance(g1.GetLat(), g2.GetLat(), g1.GetLon(), g2.GetLon(), s.getHeight())
        
        distatnce_of_satellite_firststation=CalculateDistance(s.GetLat(), g1.GetLat(), s.GetLon(), g1.GetLon(), s.getHeight())
        g1_zenitpoints=GetVisibleZone(g1, distatnce_of_satellite_firststation, s.getHeight())
        g2_zenitpoints=GetVisibleZone(g2, distance_of_stations+distatnce_of_satellite_firststation, s.getHeight())
        self.length=distance_of_stations+distatnce_of_satellite_firststation
        self.sector1.setstartpoint(0)
        self.sector1.setendpoint(g1_zenitpoints[0])
        self.sector2.setstartpoint(g1_zenitpoints[0])
        self.sector2.setendpoint(g1_zenitpoints[1])
        self.sector3.setstartpoint(g1_zenitpoints[1])
        self.sector3.setendpoint(g2_zenitpoints[0])
        self.sector4.setstartpoint(g2_zenitpoints[0])
        self.sector4.setendpoint(g2_zenitpoints[1])

    def Simulate(self, satellite, ground_1, ground_2, air_1, air_2):
        #1.szektor
        sector_1_time=self.sector1.getlenght()/satellite.speed
        self.sector1.settime(sector_1_time)
        print(sector_1_time)
        self.fulltime+=sector_1_time
        #2.szektor
        ground_1.AddAir(air_1) 
        satellite.AddAir(air_1)
        air_1.SetGroundStation(ground_1)
        air_1.SetSatellite(satellite)
        air_1.SetTransmittancy()
        satellite.AddSector(self.sector2)
        ground_1.AddSector(self.sector2)
        self.BB84(satellite, ground_1)
        #3.szektor
        sector_3_time=self.sector3.getlenght()/satellite.speed
        self.sector3.settime(sector_3_time)
        self.fulltime+=sector_3_time
        print(sector_3_time)
        #4.szektor
        ground_2.AddAir(air_2)
        satellite.AddAir(air_2)
        air_2.SetGroundStation(ground_2)
        air_2.SetSatellite(satellite)
        air_2.SetTransmittancy()
        satellite.AddSector(self.sector4)
        ground_2.AddSector(self.sector4)
        self.BB84(satellite, ground_2)
        satellite.SendXORedKey()
        
        #satellite.printInfo()
        ground_1.PrintInfo()
        ground_2.PrintInfo()
        print("\n\n")
        print("-------------------")
        self.sector1.PrintInfo()
        self.sector2.PrintInfo()
        self.sector3.PrintInfo()
        self.sector4.PrintInfo()



    def BB84(self, satellite, groundstation):
        satellite.SendQubit(700)
        groundstation.SendMeasuredBases()
        satellite.SendMatchingBases()
        groundstation.PrintInfo()
        satellite.printInfo()
        self.Reconcilation(satellite, groundstation)


    def Reconcilation(self, satellite, groundstation):
        groundstation.Reconcilation()

    


class Sector:
    def __init__(self):
        self.available_time="infinite"
        self.startpoint=0
        self.endpoint=0
        self.name=""
        self.passed_time=0
    def gettime(self):
        return self.passed_time
    def getlenght(self):
        return self.endpoint-self.startpoint
    def getstartpoint(self):
        return self.startpoint
    def getendpoint(self):
        return self.endpoint
    def getname(self):
        return self.name
    def settime(self, time):
        self.available_time=time
    def setstartpoint(self, sp):
        self.startpoint=sp
    def setendpoint(self, ep):
        self.endpoint=ep
    def setname(self, name):
        self.name=name
    def Addtime(self, dt):
        self.passed_time+=dt
    def PrintInfo(self):
        print(self.name)
        print("------------------")
        print("szakasz hossza: ", self.getlenght())
    






    


#segédfügggvények

def CalculateDistance(lat1, lat2, lon1, lon2, satelliteheight): #két földi állomás közötti távolság kiszámítása a műhold magasságát figyelembe véve
    lat1=math.radians(lat1)
    lat2=math.radians(lat2)
    lon1=math.radians(lon1)
    lon2=math.radians(lon2)
    dlon=lon1-lon2
    dlat=lat1-lat2
    a=math.sin(dlat/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c=2*math.asin(math.sqrt(a))
    r=6371+satelliteheight
    return (c*r)

    #source: https://www.geeksforgeeks.org/program-distance-two-points-earth/

def GetVisibleZone(g1, distance_from_startpoint, height_of_satellite): #visszaadja a földi állomás látható zónájának kezdő- és végpontját
    alpha=(360-g1.zenit)/2
    alpha=math.radians(alpha)
    a=6371+height_of_satellite
    f=6371
    b=math.sin(alpha)
    c=b*float(f)/float(a)
    beta=math.asin(c)
    
    beta=beta*180/3.141
    gamma=360-2*(alpha*180/3.141+beta)
    l=(gamma/float(360))*2*a*3.141
    points=[]
    points.append(distance_from_startpoint-(l/2))
    points.append(distance_from_startpoint+(l/2))
    return points



lat1=47.497913
lon1=19.040236
lat2=40.712345
lon2=-74.005531
sh=500




groundstation_1=comm.GroundStation(lat=lat1, lon=lon1, zenit=45, IsSecond=0)
groundstation_2=comm.GroundStation(lat=lat2, lon=lon2, zenit=45, IsSecond=1)
satellite=comm.Satellite(lat=0.0, lon=0.1, height=500, speed=8)
groundstation_1.AddName("New York")
groundstation_2.AddName("Budapest")
satellite.AddName("Satellite-1")
air_1=comm.Air(name="New York Air", IsEve=0, season="summer", weather="hazy")
air_2=comm.Air(name="Budapest Air", IsEve=0, season="summer", weather="hazy")


route=Route()
route.Calculate(groundstation_1, groundstation_2, satellite)
route.Simulate(satellite, groundstation_1, groundstation_2, air_1, air_2)