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
            count += 1
            #print(row)
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
        


        cursor.execute("SELECT * FROM Restaurants")
        for row in cursor:
            id = row[0]
            print(row)

        # cursor.execute("UPDATE Restaurants SET Type_id = ?", ('HANNNN')) 
        # cursor.execute("SELECT * FROM Restaurants")
        # for row in cursor:
        #     print(row)         

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
            
    GetYelpRatings()
    print('done')

    # for i in range(1,11):
    #     time.sleep(1)
    #     getYelpRatings()
    #     hm = (i*20)
    #     print(str(hm) + ' Items Collected')
    
    # yelp_csv('yelp.csv')
    pass

main()
