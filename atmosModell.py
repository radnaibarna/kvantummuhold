import math as Math

#__all__ = ["allLossallLoss"]

def waveLengthToWaveNumber(waveLength):
    ret = (2 * Math.pi) / (waveLength * Math.pow(10, -9))
    return ret


def turbulenceStrength(heightAboveSeaLevel,windspeed):
    aParameter = 1.7 * Math.pow(10, -14)
    ret = 0
    ret = 0.00594 * Math.pow((windspeed / 27), 2) * Math.pow((heightAboveSeaLevel * Math.pow(10, -5)), 10) * Math.exp((heightAboveSeaLevel / 1000) * (-1)) + (2.7 * Math.pow(10, -16)) * Math.exp((heightAboveSeaLevel / 1500) * (-1)) + aParameter * Math.exp((heightAboveSeaLevel / 100) * (-1))

    return ret

def beamWideningGroundToSpace( waveLength, heightBlocks, channelLength, windSpeed, zenithAngle, height):
    ret = 0
    sum = 0 
    channelLength = channelLength * 1000
    Wavenumber = waveLengthToWaveNumber(waveLength)
    for i in range(len(heightBlocks)-2):
        turb1 = turbulenceStrength(heightBlocks[i], windSpeed)
        tort1 = Math.pow(1 - heightBlocks[i] / (channelLength * Math.cos(zenithAngle * (Math.pi / 180))), 5/3)
        turb2 = turbulenceStrength(heightBlocks[i + 1], windSpeed)
        #print(f"za = {zenithAngle}, ch = {channelLength}") 
        tort2 = Math.pow(1 - heightBlocks[i + 1] / (channelLength * Math.cos(zenithAngle * (Math.pi / 180))), 5 / 3)
        tort3 = (turb1 * tort1 + turb2 * tort2) / 2
        tort4 = abs((heightBlocks[i + 1] - heightBlocks[i]) / Math.cos(zenithAngle * (Math.pi / 180)))
        tort5 = tort3 * tort4
        sum = sum + tort5

    ret = (1.46 * Math.pow(Wavenumber, 2) * sum) 
    
    if ret < 0:
        ret *=-1
        ret = Math.pow(ret, -0.6)
        ret *=-1
    else:
        ret = Math.pow(ret,-0.6)

    return ret

def beamWideningSpaceToGround(waveLength, heightBlocks, channelLength, windSpeed, zenithAngle, height):
    ret = 0
    sum = 0

    channelLength = channelLength * 1000
    Wavenumber = waveLengthToWaveNumber(waveLength);ret = 0
    sum = 0

    channelLength = channelLength * 1000
    Wavenumber = waveLengthToWaveNumber(waveLength)
    for i in range(len(heightBlocks)-2):
        turb1 = turbulenceStrength(heightBlocks[i], windSpeed)
        tort1 = Math.pow(1 - ((channelLength - (heightBlocks[i] /  Math.cos(zenithAngle * (Math.pi / 180)))) / channelLength), 5 / 3)
        turb2 = turbulenceStrength(heightBlocks[i + 1], windSpeed)
        tort2 = Math.pow(1 - ((channelLength - (heightBlocks[i + 1] / Math.cos(zenithAngle * (Math.pi / 180)))) / channelLength), 5 / 3)
        tort3 = (turb1 * tort1 + turb2 * tort2) / 2
        tort4 = abs((heightBlocks[i + 1] - heightBlocks[i]) / Math.cos(zenithAngle * (Math.pi / 180)))
        tort5 = tort3 * tort4
        sum = sum + tort5

    ret = 1.46 * Math.pow(Wavenumber, 2) * sum
    ret = Math.pow(ret, -0.6)

    return ret

def beamWideningInAtmosphere(channelLength, waveLength, coherenceLength, apertureDiameter):
    ret = 0
    channelLength = channelLength * 1000
    WaveNumber = waveLengthToWaveNumber(waveLength)
    ret = Math.sqrt(4.0 * Math.pow(channelLength, 2.0) / (Math.pow(WaveNumber, 2.0) * Math.pow(apertureDiameter, 2.0)) + Math.pow(apertureDiameter, 2.0) / 4.0 + 4.0 * Math.pow(channelLength, 2.0) /Math.pow(WaveNumber * coherenceLength, 2.0) * Math.pow(Math.pow(1.0 - 0.62 * Math.pow(coherenceLength / apertureDiameter, 0.3333), 6.0), 0.0))
    #ret = Math.sqrt((4 * Math.pow(channelLength, 2)) / (Math.pow(WaveNumber, 2) * Math.pow(apertureDiameter, 2)) + Math.pow(apertureDiameter, 2) / 4 +            ((4 * Math.pow(channelLength, 2)) / Math.pow((WaveNumber * coherenceLength), 2)) * Math.pow(Math.pow((1 - 0.62 * Math.pow((coherenceLength / apertureDiameter), 0.3333)), 6), 1/5))

    return ret 


def totalScattering(beamRadius, targetingError):
    ret = 0
    ret = Math.sqrt(Math.pow(beamRadius, 2) + Math.pow(targetingError, 2))
    return ret


def targetingError(angularError, channelLength):
    ret = 0

    channelLength = channelLength * 1000
    ret = channelLength * angularError
    ret = ret * Math.pow(10, -6)
    return ret


def dynamicLoss(totalScattering, mirrorRadius):
    ret = 0
    ret =  1 - Math.exp(((-1) * Math.pow(mirrorRadius, 2)) / (2 * Math.pow(totalScattering, 2)))

    return ret

def staticLoss( molecularScattering,  molecularAbsorption,  aerosolScattering,  aerosolAbsorption,  layers,  zenithAngle):
    scattering = []
    absorption = []
    ret = 0
    sum = 0

    for i in range(len(molecularScattering)):
        scattering.append( molecularScattering[i] + aerosolScattering[i])
                

    for i in range(len(molecularScattering)):
        absorption.append( molecularAbsorption[i] + aerosolAbsorption[i])
    
    for i in range(len(layers)-1):
        sum = sum + (((scattering[i] + scattering[i + 1]) / 2) + ((absorption[i] + absorption[i + 1]) / 2)) * ((layers[i + 1] - layers[i]) / Math.cos(zenithAngle * (Math.pi / 180)))
    ret = Math.exp(-1 * sum)
    return ret


def beamWideningInVacum(channelLength,waveLength,apertureDiameter):
    channelLength*=1000.0
    Wavenumber = waveLengthToWaveNumber(waveLength)
    ret = Math.sqrt(4.0*pow(channelLength,2.0)/(pow(Wavenumber,2.0)*pow(apertureDiameter,2.0)) + pow(apertureDiameter,2.0)/4.0)
    return ret


def setOpticalDistance(heightAboveSeaLevel = 500, zenithAngle=30):
    opticalDistanceStages = {} 
    opticalDistanceStages[0] = 0.0
    for i in range(1,45):#this was used in QuantumProtocol
        if (opticalDistanceStages[i - 1] < 1000.0):
            opticalDistanceStages[i] = opticalDistanceStages[i - 1] + 200.0
    
        if (opticalDistanceStages[i - 1] >= 1000.0 and opticalDistanceStages[i - 1] < 30000.0):
            opticalDistanceStages[i] = opticalDistanceStages[i - 1] + 1000.0
            
        if (opticalDistanceStages[i - 1] >= 30000.0 and opticalDistanceStages[i - 1] < 60000.0):
            opticalDistanceStages[i] = opticalDistanceStages[i - 1] + 5000.0
            
        if (opticalDistanceStages[i - 1] >= 60000.0):
            opticalDistanceStages[i] = opticalDistanceStages[i - 1] + 10000.0
    return opticalDistanceStages         
        
    



#isDown 0 fel; 1 ur; 2 le 
def allLoss( zenithAngle=30, satelliteheight=500, season=5, weather=11):
    import csv
    molecularScattering = [] 
    molecularAbsorption = [] 
    aerosolScattering = [] 
    aerosolAbsorption = [] 
    layers = [] 
    isDown=2

    molcular_index = season #SUMMER 5 Winter 8
    aerosol_index = weather #CLEAR 11 Hazy 14
    
    with open('asv_860.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter = ';')
        cnt = 1
        for row in reader:
            if cnt > 7:
                layers.append(float(row[0]))
                molecularAbsorption.append(float(row[molcular_index]))
                molecularScattering.append(float(row[molcular_index+1]))
                aerosolAbsorption.append(float(row[aerosol_index]))
                aerosolScattering.append(float(row[aerosol_index+1]))

            cnt +=1 
    heightAboveSeaLevel = satelliteheight
    opticalDistance = Math.sqrt(Math.pow(6371.0, 2.0) * Math.pow(Math.cos(zenithAngle * 0.017453292519943295), 2.0) + 12742.0 * heightAboveSeaLevel + Math.pow(heightAboveSeaLevel, 2.0)) - 6371.0 * Math.cos(zenithAngle * 0.017453292519943295)
    opticalDistanceStages = setOpticalDistance(heightAboveSeaLevel,zenithAngle)
    
    #konstansok
    mirrorDiameter = 1 # m
    apertureDiameter = 0.2 #m
    targetingAngularError = 0.5 #qrad
    waveLength = 860 #nm
    windSpeed = 21 # m/s
    heightAboveSeaLevel = 500 #ez konstans mivel starlink ott megy
    
    totalNoise = 2.0E-7
    prob_of_polarization_measurment_error = 1.0E-4
    meanPhotonNumberOfSignal = 0.1
    quantumEfficiencyOfDetector = 0.7
    #print(opticalDistance)
    #print(layers)
    #print(molecularAbsorption)
    #print(molecularScattering)
    #print(aerosolAbsorption)
    #print(aerosolScattering)
    """if isDown == 0:
        sl = staticLoss(molecularScattering, molecularAbsorption, aerosolScattering, aerosolAbsorption, layers, zenithAngle)
        coherenceLength = beamWideningGroundToSpace(waveLength, opticalDistanceStages , opticalDistance, windSpeed, zenithAngle, heightAboveSeaLevel) #optical distanceStages lecserelve layersre 
        beamWidening = beamWideningInAtmosphere( opticalDistance, waveLength, coherenceLength, apertureDiameter ) 
        TE = targetingError(targetingAngularError, opticalDistance)
        TS = totalScattering(beamWidening, TE)
        DL = dynamicLoss(TS, mirrorDiameter / 2)
    if isDown == 1:
        sl = 1
        beamWidening = beamWideningInVacum(spaceChannelLength,waveLength,apertureDiameter)
        TE = targetingError(targetingAngularError,spaceChannelLength)
        TS = totalScattering(beamWidening,TE)
        DL = dynamicLoss(TS,mirrorDiameter/2)"""
    if isDown==2:
         sl = staticLoss(molecularScattering, molecularAbsorption, aerosolScattering, aerosolAbsorption, layers, zenithAngle)
         coherenceLength = beamWideningSpaceToGround(waveLength,opticalDistanceStages, opticalDistance, windSpeed, zenithAngle, heightAboveSeaLevel) #optical distanceStages lecserelve layersre
         beamWidening = beamWideningInAtmosphere( opticalDistance, waveLength, coherenceLength, apertureDiameter )
         TE = targetingError(targetingAngularError, opticalDistance)
         TS = totalScattering(beamWidening, TE)
         DL = dynamicLoss(TS, mirrorDiameter / 2)
    """
    print(zenithAngle)
    print("---")
    print(f"targetingError: {TE}")
    print(f"totalScattering {TS}")
    print(f"dyn loss : {DL}")
    print (f"beamWideningInAtmosphere : {beamWidening}")
    #print(f"coherenceLength {coherenceLength}")
    print(f"staticLoss : {sl}")
    """
    t = sl * DL
    prob = prob_of_polarization_measurment_error +  totalNoise * 4 /(meanPhotonNumberOfSignal *quantumEfficiencyOfDetector *2* t)
    #print(prob)
    return prob 


print(allLoss(45, 500))
#allLoss(30,1,577)

