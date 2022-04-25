# Winter 2022 Final Project
# SI 206
# Name: Lennox Thomas & Nicole Surcel

from bs4 import BeautifulSoup
import requests
import re
import csv
import os
import sqlite3

def restaurantlst(url):
  # This function takes in a url from the "Open Table" website, and creates a BeautifulSoup Object to parse through 
  # the site's HTML. The function returns a list of tuples which include the restaurant name as well as the restaurant's location.
    
    restaurant_Name = []
    restaurant_Location = []
    restaurant_Type = []
    restaurant_Rating = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')

    spans = soup.find_all(class_='CCbGHaorgGHXgJqoOaXl')

    for item in spans:
      restaurantName = item.find('h2', class_='H5kqSXUFObkmV6wfAw7p').text
      restaurantLocation =  item.find('div', class_='GwGPDuPdTZpMt7oIzo4A YQ2SmR3lcmrtTcxuktZA').text
      restaurantType =  item.find('div', class_= 'UNOIq8wcqctrC7s3wHAW YQ2SmR3lcmrtTcxuktZA').text
      restaurantRating = item.find('div', class_ = 'vJWFYZLiWZbHIB0Hwa83')['aria-label'][:3]
      if restaurantRating[0] == 5:
        print("hooray")
        #restaurantRating == 5.0
      # else:
      #   restaurantRating = float(restaurantRating)
      
      restaurant_Name.append(restaurantName)
      restaurant_Type.append(restaurantType)
      restaurant_Location.append(restaurantLocation)
      restaurant_Rating.append(restaurantRating)
    
    #print(restaurant_location)
    #print(restaurant_names)
    #print(list(zip(restaurant_names, restaurant_location)))
    restaurantlst = list(zip(restaurant_Name, restaurant_Type, restaurant_Location, restaurant_Rating))
    #print(restaurantlst)
    return restaurantlst

def setUpDatabase(db_name):
  # This function simply takes in a string as input which contains the preferred database file name, and 
  # returns the cursor and connection to the created database.

   path = os.path.dirname(os.path.abspath(__file__))
   conn = sqlite3.connect(path+'/'+db_name)
   cur = conn.cursor()

   return cur, conn

# Create Restaurants table if does not exist
def setUpRestaurantsTable(cur, conn, restaurantlst, x = 0):
  # This takes a database cursor and conneciton, list of restaurant names, restaurant type, and optional 
  # argument which specifies the starting position of the database id. The function creates a table, Restaurants, 
  # within the passed database and inserts each restaurant in restaurantlist, along with its corresponding id, location, and type.
  
  cur.execute("CREATE TABLE IF NOT EXISTS Restaurants (id INTEGER PRIMARY KEY, Name TEXT, Type TEXT, Type_ID TEXT, Location TEXT, OpenTable_Rating FLOAT, Yelp_Rating FLOAT)")
  for num in range(len(restaurantlst)):
    id = num + x
    cur.execute("INSERT OR IGNORE INTO Restaurants (id, Name, Type, Location, OpenTable_Rating) VALUES (?,?,?,?,?)", (id, restaurantlst[num][0], restaurantlst[num][1], restaurantlst[num][2], restaurantlst[num][3][:3]))
  conn.commit()

# Create Types table is not exists
def setUpTypesTable(cur, conn, typelst):
    # This function takes in a databse cursor and connection, as well as a list of restaurant type. It then creates
    # a table, Types, within the database, along with its corresponding id number.

    cur.execute("CREATE TABLE IF NOT EXISTS Types (id INTEGER PRIMARY KEY, type TEXT)")
    for i in range(len(typelst)):
        cur.execute("INSERT OR IGNORE INTO Types (id, type) VALUES (?,?)", (i, typelst[i]))
    conn.commit()

# Write restaurant list into a CSV file
def write_csv(data, filename):
  # This file takes in a list of tuples and csv filename as input. It then iterates through the list of tuples 
  # to write multiple rows within the csv, outputting a csv file containing each restaurant name and restaurant location.
  
  header = ('Restaurant Name', 'Restaurant Type', 'Restaurant Location', 'Restaurant OpenHouse Rating')

  with open(filename, 'w', newline='') as f:
         writer = csv.writer(f)
         writer.writerow(header)
         for item in data:
             writer.writerow(item)
  
# Setup database file
def main():

  restaurant_tuple_lst = restaurantlst('https://www.opentable.com/lists/top-100-2021')
  types = ['Afghan', 'American', 'Contemporary American', 'Contemporary French', 'Contemporary Southern', 'Croatian', 'Farm-to-table', 'Fish', 'French', 'Fusion / Eclectic', 'Greek', 'Italian', 'Mediterranean', 'Mexican', 'Peruvian', 'Seafood', 'Southwest', 'Speakeasy', 'Steak', 'Steakhouse', 'Sushi', 'Tapas / Small Plates', 'Traditional French', 'Vietnamese', 'Winery']
  
  write_csv(restaurant_tuple_lst, 'restaurant.csv')

  cur, conn = setUpDatabase('restaurantData.db')
  setUpRestaurantsTable(cur, conn, restaurant_tuple_lst, x = 0)
  setUpTypesTable(cur, conn, types)

main()
