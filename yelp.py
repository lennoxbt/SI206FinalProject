# Winter 2022 Final Project
# SI 206
# Name: Lennox Thomas & Nicole Surcel

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
    # This function gathers data from the Yelp API, 20 items at a time. It accesses the restaurant names in the restaurant.csv file in order to 
    # pull multiple restaurant metrics from the api. This pulled data is then placed into the tables of the restaurantData.db 
    # database.

    api_key = 'OP7cfO8hvRHG4xM1GUusN1i3VLGPR49ih-GAizx_L_K6bK4cuIVz6gVeksghyZR_23E1mOJuLT3hPijs1IDAhpSG956IaPh6cpUxsDT1Hi4Rbh6vzftOEdrfjghoYnYx'
    ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
    rest_rows = []
    my_file = 'count.txt'
    my_file = open(my_file, "r")
    count = my_file.readlines()
    my_file.close()
    with open('restaurant.csv', 'r') as file:
        reader = csv.reader(file)
    
        # AYMAN'S ADDITION
        #==================
        print(count)
        count = int(count[0])
        ind = count%4
        reader1=[row for idx, row in enumerate(reader) if idx in range(25*ind+1,25*(ind+1)+1)]
        #==================
        # END OF AYMAN'S ADDITION
        dbName ='restaurantData.db'
        conn = sqlite3.connect(dbName)
        cursor = conn.cursor()
        #next(reader)

        objects = []
        for row in reader1:
            # if count > 20:
            #     print('got 20, restart for more')
            #     break
            # count += 1
            # print(row)
            restaurantName = row[0]
            restaurantType = row[1]
            restaurantLocation = row[2]
            # restaurantYelpRating = row[3]
            id = 0
            
            parameters = {'term': restaurantName, 'location': restaurantLocation, 'categories': 'restaurants', 'limit': 1}
            HEADERS = {'Authorization': 'bearer %s' % api_key}
            print(restaurantName)
            response_obj = requests.get(url = ENDPOINT, params = parameters, headers = HEADERS)
            data = response_obj.json()
            # print(data['businesses'][0])
            # print(data.keys())
            # print(type(data.keys()))

            if 'businesses' in data.keys():
                # print(json.dumps(data, indent = 3))
                if data['businesses'] != []:
                    # print(json.dumps(data['businesses'][0]['price'], indent = 3))
                    yelp_Rating = (data['businesses'][0]['rating'])
                    if 'price' in data['businesses'][0]:
                        yelp_Price = data['businesses'][0]['price']
                    else:
                        yelp_Price = 'N/A'
                else:
                    yelp_Rating = 0

                # print(yelp_Rating)
            
            #cursor.execute('UPDATE Restaurants SET Type_ID=(select Type_ID from Types WHERE Types.Type=Restaurants.Type)')
            #'UPDATE Restaurants SET type_id=(select type_id from Types WHERE Types.type=Restaurants.type)'
            #conn.commit()
            cursor.execute("UPDATE Restaurants SET Yelp_Rating = ? WHERE Name = ?", (yelp_Rating, restaurantName))
            conn.commit()
            cursor.execute("UPDATE Restaurants SET Yelp_Price = ? WHERE Name = ?", (yelp_Price, restaurantName))
            conn.commit()
            
            count += 1

            # cursor.execute("SELECT * FROM Restaurants")
            # for row in cursor:
            #     id = row[0]
            #     #print(row)
        my_file = open("count.txt", "w")
        my_file.write(str(count))
        my_file.close()
        # conn.commit()
        # if rest_rows:
        #     with open('restaurant.csv', 'w') as file:    
        #         writer = csv.writer(file)
        #         writer.writerows(rest_rows)

def yelp_csv(filename):
    # This function takes in a csv filename as input, and selects data from the joined tables, Restaurants and Types. 
    # This data is then used to calculate the average of the OpenTable and Yelp ratings for each restaurant.
    # This calculation is then output into the yelp.csv file along with the restaurant name, average rating btwn yelp and open table

    header = ('Restaurant Name', 'Restaurant Average Rating')

    dbName ='restaurantData.db'
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    
    cursor.execute('SELECT Restaurants.Name, Restaurants.OpenTable_Rating, Restaurants.Yelp_Rating FROM Restaurants JOIN Types ON Restaurants.Type_ID = Types.Type_ID WHERE OpenTable_Rating != ? AND Yelp_Rating != ?', (0,0))
    with open(filename, 'w', newline ='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for row in cursor:
            print(row)
            opentable_rating = row[1]
            yelp_rating = row[2]
            #print(row)
            # print(opentable_rating,yelp_rating)
            score = (float(opentable_rating) + float(yelp_rating))
            avg = score/2
            ro = [row[0], avg]
            print(ro)
            writer.writerow(ro)

def main():
    # This function calls the above functions, getYelpRatings and yelp_csv. In order to gather enough data from 
    # the Yelp API, getYelpRatings is called within a for loop, multiple times.
    
    # The for loop below allows for the "Yelp" API data to be collected and placed within the database 25 items at a time, with one execution/run
    # for i in range(1,5):
    #     time.sleep(1)
    #     getYelpRatings()
    #     hm = (i*25)
    #     print(str(hm) + ' Items Collected')

    getYelpRatings()  
    yelp_csv('yelp.csv')

main()
