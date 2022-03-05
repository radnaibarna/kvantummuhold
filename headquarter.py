from os import name
import city as city
import communication as comm
import requests


class HeadQuarter:
    def __init__(self) -> None:
        self.api_key = "78J68A-UYA26V-9CBFRR-4RZ5"
        self.satellite_schedules = {}  
        self.satellites = ["27848", "27844", "29252"]
        self.cities_by_satellites={} # egyes városokra azok az adatok, hogy az egyes műholdakat mikor kezdi el látni és mikor lép ki a látómezejükből
        self.mode = 1 
        self.sectors = {}
        self.city_modes_by_satellites = {}
        self.photon_time = 0.1
        self.city_names = []
        self.city_pairs = {}

        pass
        
    def get_satellite_data(self, cities_):
        self.cities_ = cities_

        for i in cities_:
            self.city_names.append(i[0])
            self.city_names.append(i[1])
            self.city_pairs[i[0]] = i[1]
            self.city_pairs[i[1]] = i[0]
            for j in self.satellites:
                city_datas = city.getcitydata(i[0], i[1])
                city_1_datas = self.getsatellinteinfo(self.api_key, city_datas[0]["lat"], city_datas[0]["lon"], city_datas[0]["elev"], j)
                city_2_datas = self.getsatellinteinfo(self.api_key, city_datas[1]["lat"], city_datas[1]["lon"], city_datas[0]["elev"], j)
                """print(city_1_datas)
                print(city_2_datas)"""
                if(city_datas[0]["name"] not in self.cities_by_satellites):
                    self.cities_by_satellites[city_datas[0]["name"]] = {
                                                                            j : {
                                                                                    "start_time" : city_1_datas["passes"][0]["startUTC"],
                                                                                    "end_time" : city_1_datas["passes"][0]["endUTC"]
                                                                            }
                                                                        }
                else:
                    if(j not in self.cities_by_satellites[city_datas[0]["name"]]):
                        self.cities_by_satellites[city_datas[0]["name"]][j] = {
                                                                                    "start_time" : city_1_datas["passes"][0]["startUTC"],
                                                                                    "end_time" : city_1_datas["passes"][0]["endUTC"]
                                                                            }
                if(city_datas[1]["name"] not in self.cities_by_satellites):
                    self.cities_by_satellites[city_datas[1]["name"]] = {
                                                                            j : {
                                                                                    "start_time" : city_2_datas["passes"][0]["startUTC"],
                                                                                    "end_time" : city_2_datas["passes"][0]["endUTC"]
                                                                            }
                                                                        }
                else:
                    if(j not in self.cities_by_satellites[city_datas[1]["name"]]):
                        self.cities_by_satellites[city_datas[1]["name"]][j] = {
                                                                                    "start_time" : city_2_datas["passes"][0]["startUTC"],
                                                                                    "end_time" : city_2_datas["passes"][0]["endUTC"]
                                                                            }

        #calculate whitch city is first, which is second
        print(self.cities_by_satellites)

    def calculate_schedule_of_satellites(self):
        self.satellite_datas = {}
        for i in self.satellites:
            satellite_data = {}
            for j in self.cities_by_satellites:
                """print(j)"""
                if(i in self.cities_by_satellites[j]):

                    satellite_data[j] = {
                            "start_time" : self.cities_by_satellites[j][i]["start_time"],
                            "end_time" : self.cities_by_satellites[j][i]["end_time"]
                        }

            self.satellite_datas[i] = satellite_data



        print(self.satellite_datas)

    def calculate_sectors(self):
        self.sectors_by_satellite = {}
        for i in self.satellites:
            self.city_modes_by_satellites[i] = {}
        for i in self.satellite_datas:
            start_times = []
            end_times = []
            all_times = []
            for j in self.satellite_datas[i]:
                start_times.append(self.satellite_datas[i][j]["start_time"])
                end_times.append(self.satellite_datas[i][j]["end_time"])
                all_times.append(self.satellite_datas[i][j]["start_time"])
                all_times.append(self.satellite_datas[i][j]["end_time"])
            
            
            all_times.sort()
            sectors_of_satellite = {}
            for j in range(len(all_times)-1):
                current_sector = []
                for k in self.satellite_datas[i]:
                    """print(all_times[j])"""
                    if((self.satellite_datas[i][k]["start_time"]+1 >= all_times[j] and self.satellite_datas[i][k]["start_time"]+1 <= all_times[j+1]) or (self.satellite_datas[i][k]["end_time"]-1 >= all_times[j] and self.satellite_datas[i][k]["end_time"]-1 <= all_times[j+1])):
                        current_sector.append(k)
                name_of_sector = "sector" + str(j)
                sectors_of_satellite[name_of_sector] = {
                    "start_time" : all_times[j],
                    "end_time" : all_times[j+1],
                    "participants" : current_sector,
                    "available_time" : all_times[j+1]-all_times[j]
                }
            self.sectors_by_satellite[i] = sectors_of_satellite


        """print(print(sectors_of_satellite))"""


    def calculate_most_needed_city(self, needed_amounts, part_cities):
            most_needed = part_cities[0]
            for i in part_cities:
                if(needed_amounts[part_cities] > needed_amounts[most_needed]):
                    most_needed = needed_amounts[part_cities]
            return most_needed

    def calculate_communication(self):
        for i in self.satellites:
            self.satellite_schedules[i] = {}
        
        print("city_pairs")
        print(self.city_pairs)

        needed_amounts = {}

        needed_times = {}

        full_schedule = {}

        for i in self.cities_:
            if(i[2] == "AES"):
                needed_amount = 2.4*256*i[3]
                needed_time = int(needed_amount*self.photon_time)
                needed_amounts[i[0]] = int(needed_amount)
                needed_amounts[i[1]] = int(needed_amount)
                needed_times[i[0]] = needed_time
                needed_times[i[1]] = needed_time
            elif(i[2] == "OTP"):
                needed_amount = 2.4*i[3]
                needed_time = int(needed_amount*self.photon_time)
                needed_amounts[i[0]] = int(needed_amount)
                needed_amounts[i[1]] = int(needed_amount)
                needed_times[i[0]] = needed_time
                needed_times[i[1]] = needed_time
        

        print(needed_amounts)

       
        for i in self.sectors_by_satellite:
            type_ones = []
            type_twos = []
            particiated_cities = []
            n_of_sector = 0

            print(self.sectors_by_satellite)

            for j in self.sectors_by_satellite[i]:
                
                if(len(self.sectors_by_satellite[i][j]["participants"])==1):
                    if(self.sectors_by_satellite[i][j]["participants"][0] not in particiated_cities):
                        type_ones.append(self.sectors_by_satellite[i][j]["participants"][0])
                        particiated_cities.append(self.sectors_by_satellite[i][j]["participants"][0])
                        possible_key_exchange = self.sectors_by_satellite[i][j]["available_time"]/self.photon_time
                        if(needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]]-possible_key_exchange) > 0:
                            needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]] = needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]]-possible_key_exchange
                            needed_amounts[self.city_pairs[self.sectors_by_satellite[i][j]["participants"][0]]] = needed_amounts[self.city_pairs[self.sectors_by_satellite[i][j]["participants"][0]]]-possible_key_exchange
                        else:
                            needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]] = 0
                            needed_amounts[self.city_pairs[self.sectors_by_satellite[i][j]["participants"][0]]] = 0
                    else:
                        type_twos.append(self.sectors_by_satellite[i][j]["participants"][0])
                        particiated_cities.append(self.sectors_by_satellite[i][j]["participants"][0])
                        possible_key_exchange = self.sectors_by_satellite[i][j]["available_time"]/self.photon_time
                        
            
            for j in self.sectors_by_satellite[i]:
                print(len(self.sectors_by_satellite[i][j]["participants"]))
                if(len(self.sectors_by_satellite[i][j]["participants"])>1):
                    for k in self.sectors_by_satellite[i][j]["participants"]:
                        print(k)
                        if(self.sectors_by_satellite[i][j]["participants"][0] not in particiated_cities):
                            type_ones.append(self.sectors_by_satellite[i][j]["participants"][0])
                            if(self.mode== 1):
                                pass
                            if(self.mode == 2):
                                possible_key_exchange = self.sectors_by_satellite[i][j]["available_time"]/self.photon_time
                                if(needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]]-possible_key_exchange) > 0:
                                    needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]] = needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]]-possible_key_exchange
                                    needed_amounts[self.city_pairs[self.sectors_by_satellite[i][j]["participants"][0]]] = needed_amounts[self.city_pairs[self.sectors_by_satellite[i][j]["participants"][0]]]-possible_key_exchange
                                else:
                                    needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]] = 0
                                    needed_amounts[self.city_pairs[self.sectors_by_satellite[i][j]["participants"][0]]] = 0

                        elif(self.sectors_by_satellite[i][j]["participants"][0] in type_ones):
                                type_ones.append(self.sectors_by_satellite[i][j]["participants"][0])
                                if(self.mode == 1):
                                    pass
                                if(self.mode == 2):
                                    possible_key_exchange = self.sectors_by_satellite[i][j]["available_time"]/self.photon_time
                                    if(needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]]-possible_key_exchange) > 0:
                                        needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]] = needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]]-possible_key_exchange
                                        needed_amounts[self.city_pairs[self.sectors_by_satellite[i][j]["participants"][0]]] = needed_amounts[self.city_pairs[self.sectors_by_satellite[i][j]["participants"][0]]]-possible_key_exchange
                                    else:
                                        needed_amounts[self.sectors_by_satellite[i][j]["participants"][0]] = 0
                                        needed_amounts[self.city_pairs[self.sectors_by_satellite[i][j]["participants"][0]]] = 0





            print(needed_amounts)

                    

        

                    

        
         
                 
    
    def main(self, cities_):
        self.get_satellite_data(cities_)
        self.calculate_schedule_of_satellites()
        self.calculate_sectors()
        self.calculate_communication()
        


    def getsatellinteinfo(self, api_key, observer_lat, observer_lng, observer_alt, noraids):
        
        url = 'https://api.n2yo.com/rest/v1/satellite/radiopasses/' + noraids + '/' + observer_lat + '/' + observer_lng + '/' + observer_alt + '/' + '1' + '/' + '45' + '/' + '&apiKey=' + api_key
        print(url)

        r = requests.get(url)
        return r.json()





input_data = [
    ["Vienna", "Budapest", "AES", 10],
    ["Helsinki", "Stockholm", "OTP", 1024]
]


h = HeadQuarter()

h.main(input_data)