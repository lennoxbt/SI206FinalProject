import requests
import re
import csv
import json
import sqlite3
import time

#Business Search      URL -- 'https://api.yelp.com/v3/businesses/search'

def GetYelpRatings():
    # This function gathers data from the yelp api, 20 items at a time. It accesses the movie titles in the movie.csv file in order to 
    # pull multiple movie metrics from the api. This pulled data is then places into the tables of the movieData.db 
    # database.

    api_key = 'MG1W3tSf9JH2M0wgcH8WF57_7OW8wGBb6JjTFUxQ4YoXdvZkpmuBjNcydtePtFZISQlpXxnktL7DAiBKaOi2zwv9EwXC-0xb9FG9HeHGLTaBwnnV-75rN9qU7FtmYnYx'
    ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
    rest_rows = []
    with open('restaurant.csv', 'r') as file:
        reader = csv.reader(file)
        count = 0
        dbName ='restaurantData.db'
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        next(reader)
        for row in reader:
            #count += 1
            print(row)
            restaurantName = row[0]
            restaurantType = row[1]
            id = 0

            location = row[2]
            parameters = {'term': restaurantName, 'location': location, 'categories': "restaurants", 'limit': 1}
            HEADERS = {'Authorization': 'bearer %s' % api_key}
            response_obj = requests.get(url = ENDPOINT, params = parameters, headers = HEADERS)
            data = response_obj.json()
            #print(data['businesses'][0])
            #print(data.keys())
            #print(type(data.keys()))
           # print(data)
            if 'businesses' in data.keys():
                #print(json.dumps(data, indent = 3))
                if data['businesses'] != []:
                    yelp_rating = (data['businesses'][0]['rating'])  
                else:
                    yelp_rating = 0
                #print(yelp_rating)
            cursor.execute("UPDATE Restaurants SET Yelp_rating = ? WHERE Name = ?", (yelp_rating, restaurantName))
            conn.commit()
            cursor.execute('UPDATE Restaurants SET Type_id = (SELECT b.Type_id  FROM Restaurants a left JOIN Types b on a.Type = b.Type)')

            conn.commit()
        

# get a cursor for "select type, typeid from types"
# for each row in the cursor
#     get type and type_id from the row
#     update restaurant set type_id = (type_id)
#     where restaurant.type =  (type)


        # cursor.execute("SELECT Type_id  FROM Types")
        # for row in cursor:
        #     id = row[0]
        #     print(row)

        # cursor.execute("SELECT * FROM Restaurants")
        # for row in cursor:
        #     print(row)         

# UPDATE Restaurants
# SET Type_id = (SELECT b.Type_id  FROM Restaurants a left JOIN Types b on a.Type = b.Type)
        
GetYelpRatings()
print('done')
