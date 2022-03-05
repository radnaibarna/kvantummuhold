





def getcitydata(city_1, city_2):
    cities=[
        {
            'name' : 'Vienna',
            'lat' : "48.12",
            'lon' : "16.22",
            'elev' :"110"
        },
        {
            'name' : 'Budapest',
            'lat' : "47.50",
            'lon' : "19.06",
            'elev' :"102"
        },
        {
            'name' : 'Helsinki',
            'lat' : '60.2',
            'lon' : '24.95',
            'elev' : '7'
        },
        {
            'name' : 'Stockholm',
            'lat' : '59.33',
            'lon' : '18.06',
            'elev' : '40'
        }

        
    ]

    data_to_return = []

    for i in range(len(cities)):
        if(cities[i]["name"] == city_1):
            data_to_return.append(cities[i])
        if(cities[i]["name"] == city_2):
            data_to_return.append(cities[i])

    return data_to_return