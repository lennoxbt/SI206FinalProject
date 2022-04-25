import requests
import re
import csv
import json
import sqlite3
import time

#Business Search      URL -- 'https://api.yelp.com/v3/businesses/search'

# Define a business ID
# business_id = '4AErMBEoNzbk7Q8g45kKaQ'

def getYelpRatings():
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
                    Yelp_Rating = (data['businesses'][0]['rating'])
                else:
                    Yelp_Rating = 0
            #print(Yelp_Rating)

            cursor.execute("SELECT * FROM Types")
            for row in cursor:
                #print(row)
                if type == row[1]:
                    id = row[0]
            
            cursor.execute("UPDATE Restaurants SET Type_ID = ? WHERE Name = ?", (id, restaurantName))
            cursor.execute("UPDATE Restaurants SET Yelp_Rating = ? WHERE Name = ?", (id, restaurantName))

def yelp_csv(filename):
    # This function takes in a csv filename as input, and selects data from the joined tables, Restaurants and Types. 
    # This data is then used to calculate the average of the OpenTable and Yelp ratings for each restaurant.
    # This calculation is then output into the yelp.csv file along with the restaurant name, gross, release date, and movie type.

    header = ('Restaurant Name', 'Restaurant OpenHouse Rating', 'Restaurant Yelp Rating')

    dbName ='restaurantData.db'
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Restaurants JOIN Types ON Restaurants.typeid = Types.id WHERE OpenHouse_Rating != ? AND Yelp_Rating != ?', (0))
    with open(filename, 'w', newline ='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for row in cursor:
            opentable = row[-6]* 10
            yelp = row[-5]
            # print(row)
            # print(opentable,yelp)

            score = (float(opentable) + float(yelp))
            avg = score//2
            #print(avg,score)
            ro = list(row)
            #print(avgscore)
            r = [ro[1],ro[2],avg]
            #print(r)
            writer.writerow(r)

def main():
    # This function calls the above functions, getYelpRatings and yelp_csv. In order to gather enough data from 
    # the Yelp API, getYelpRatings is called within a for loop, multiple times.

    # for i in range(1,11):
    #     time.sleep(1)
    #     getYelpRatings()
    #     hm = (i*20)
    #     print(str(hm) + ' Items Collected')
    
    # yelp_csv('yelp.csv')
    pass

main()
