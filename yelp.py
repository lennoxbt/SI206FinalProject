import requests
import re
import csv
import json
import sqlite3
import time

#Business Search      URL -- 'https://api.yelp.com/v3/businesses/search'

# Define a business ID
# business_id = '4AErMBEoNzbk7Q8g45kKaQ'

def GetYelpRatings():
    # This function gathers data from the yelp api, 20 items at a time. It accesses the restaurant names in the restaurant.csv file in order to 
    # pull multiple restaurant metrics from the api. This pulled data is then placed into the tables of the restaurantData.db 
    # database.

    api_key = 'HfqofispM8DGunRZH5-sweTfY7YZQ3dppTieqg1FyH9rSi8fpaYDMhcVOQuLkYOfQvYwZPGzqkkkb1iQz2I5nmR1Pj7ApLHxrDZJ0nFJEyc7Cg8N25ngbdypujZPYnYx'
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
            count += 1
            #print(row)
            restaurantName = row[0]
            # restaurantType = row[1]
            location = row[2]
            id = 0

            parameters = {'term': restaurantName, 'location': location, 'categories': "restaurants", 'limit': 1}
            HEADERS = {'Authorization': 'bearer %s' % api_key}
            response_obj = requests.get(url = ENDPOINT, params = parameters, headers = HEADERS)
            data = response_obj.json()
            #print(data['businesses'][0])
            #print(data.keys())
            #print(type(data.keys()))

            if 'businesses' in data.keys():
                #print(json.dumps(data, indent = 3))
                if data['businesses'] != []:
                    yelp_rating = (data['businesses'][0]['rating'])
                else:
                    yelp_rating = 0
               
            #print(yelp_rating)

            cursor.execute("SELECT * FROM Types")
            for row in cursor:
                #print(row)
                if type == row[1]:
                    id = row[0]
            
            cursor.execute("UPDATE Restaurants SET Type_ID = ? WHERE Name = ?", (id, restaurantName))
            cursor.execute("UPDATE Restaurants SET Yelp_Rating = ? WHERE Name = ?", (yelp_rating, restaurantName))

GetYelpRatings()
