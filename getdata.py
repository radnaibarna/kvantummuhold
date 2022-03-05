import requests
import city as city
from datetime import datetime

api_key = "78J68A-UYA26V-9CBFRR-4RZ5"
observer_lat = "47.506129300000005"
observer_lng = "19.0611209"
observer_alt = '110.0'

file = open("noradids.txt", "r")




noraids = file.read().splitlines()

city_1_name = 'Vienna'
city_2_name = 'Budapest'

citydata = city.getcitydata(city_1_name, city_2_name)
print(citydata)

def getsatellinteinfo(api_key, observer_lat, observer_lng, observer_alt, noraids):
    for i in noraids:
        url = 'https://api.n2yo.com/rest/v1/satellite/radiopasses/' + i + '/' + observer_lat + '/' + observer_lng + '/' + observer_alt + '/' + '1' + '/' + '45' + '/' + '&apiKey=' + api_key
        print(url)

        r = requests.get(url)
        return r.json()


city_1_datas = getsatellinteinfo(api_key, citydata[0]['lat'], citydata[0]['lon'], citydata[0]['elev'], noraids)
print(city_1_datas)
city_2_datas = getsatellinteinfo(api_key, citydata[1]['lat'], citydata[1]['lon'], citydata[1]['elev'], noraids)
print(city_2_datas)

city_1_first_pass = city_1_datas['passes'][0]
city_2_first_pass = city_2_datas['passes'][0]

if(city_1_first_pass['startUTC'] > city_2_first_pass['startUTC']):
    common_time = city_1_first_pass['endUTC']-city_2_first_pass['startUTC']
    first_zone_time = city_1_first_pass['startUTC'] - city_2_first_pass['startUTC']
    third_zone_time = city_1_first_pass['endUTC'] - city_2_first_pass['endUTC']
    print('1. város: ', city_2_name)
    print('2. város: ', city_1_name)
    print("csak ", city_2_name, ": ", datetime.utcfromtimestamp(first_zone_time).strftime('%Y-%m-%d %H:%M:%S'))
    print("közös metszet: " + datetime.utcfromtimestamp(common_time).strftime('%Y-%m-%d %H:%M:%S'))
    print("csak ", city_1_name, ": ", datetime.utcfromtimestamp(third_zone_time).strftime('%Y-%m-%d %H:%M:%S'))

elif(city_1_first_pass['startUTC'] < city_2_first_pass['startUTC']):
    common_time = city_2_first_pass['endUTC']-city_1_first_pass['startUTC']
    first_zone_time = city_2_first_pass['startUTC'] - city_1_first_pass['startUTC']
    third_zone_time = city_2_first_pass['endUTC'] - city_1_first_pass['endUTC']
    print('1. város: ', city_1_name)
    print('2. város: ', city_2_name)
    print("csak ", city_1_name, ": ", datetime.utcfromtimestamp(first_zone_time).strftime('%Y-%m-%d %H:%M:%S'))
    print("közös metszet: " + datetime.utcfromtimestamp(common_time).strftime('%Y-%m-%d %H:%M:%S'))
    print("csak ", city_2_name, ": ", datetime.utcfromtimestamp(third_zone_time).strftime('%Y-%m-%d %H:%M:%S'))

"""url = 'https://api.n2yo.com/rest/v1/satellite/above/' + observer_lat + '/' + observer_lng + '/' + observer_alt + '/' + '45' + '/' + '32' + '/' + '&apiKey=' + api_key
r = requests.get(url)
above = r.json()['above']
for i in above:
    print(i)"""
    



