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

    restaurant_names = []
    restaurant_locations = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')

    spans = soup.find_all(class_='CCbGHaorgGHXgJqoOaXl')

    for item in spans:
      restaurantNameInfo = soup.find_all(class_='H5kqSXUFObkmV6wfAw7p')
      for restaurantName in restaurantNameInfo:
        restaurant_names.append(restaurantName.text)

      restaurantLocationInfo = soup.find_all(class_='GwGPDuPdTZpMt7oIzo4A YQ2SmR3lcmrtTcxuktZA')
      for restaurantLocation in restaurantLocationInfo:
        restaurant_names.append(restaurantLocation.text)
     
    print(restaurant_names)
    print(restaurant_locations)

  # Write restuaurant list into a CSV file

def write_csv(data, filename):
  # This file takes in a list of tuples and csv filename as input. It then iterates through the list of tuples 
  # to write multiple rows within the csv, outputting a csv file containing each restaurant name and restaurant location.
  
  header = ('Restaurant Name', 'Restaurant Location', 'Rating')

  with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item in data:
            writer.writerow(item)
  pass

  # Setup database file

def setUpDatabase(db_name):
  # This function simply takes in a string as input which contains the preferred database file name, and 
  # returns the cursor and connection to the created database.

  path = os.path.dirname(os.path.abspath(__file__))
  conn = sqlite3.connect(path+'/'+db_name)
  cur = conn.cursor()
  return cur, conn
  pass

  # Create restaurant table if not exists

def setUpRestaurantTable(cur, conn, restaurantlst, type, x = 0):
  # This file takes a database cursor and conneciton, list of restaurant names, restaurant type, and optional 
  # argument which specifies the starting position of the database id. The function creates a table, Restaurants, 
  # within the passed database and inserts each restaurant in restaurantlist, along with its corresponding id, location, and type.
  
  cur.execute("CREATE TABLE IF NOT EXISTS Restaurants (id INTEGER PRIMARY KEY, title TEXT, location TEXT, typeid TEXT, openhouse_rating FLOAT, label INTEGER)")
  # cur.execute("CREATE TABLE IF NOT EXISTS Restaurants (id INTEGER PRIMARY KEY, title TEXT, location TEXT, typeid TEXT, openhouse_rating FLOAT, awards INTEGER, imdb_rating FLOAT, metascore FLOAT, rotten_tomatoes FLOAT, label INTEGER)")

  for num in range(len(restaurantlst)):
    id = num + x
    cur.execute("INSERT INTO Movies (id,title,date,label) VALUES (?,?,?,?)",(id,restaurantlst[num][0], restaurantlst[num][1],type))
  conn.commit()
  pass
  
  # Create genre table is not exists

def setUpTypeTable(cur, conn, typelst):
    # This function takes in a databse cursor and connection, as well as a list of restaurant types. It then creates
    # a table, Types, within the database, along with its corresponding id number.

    cur.execute("CREATE TABLE IF NOT EXISTS Types (id INTEGER PRIMARY KEY, genre TEXT)")
    for i in range(len(typelst)):
        cur.execute("INSERT OR IGNORE INTO Types (id, type) VALUES (?,?)", (i, typelst[i]))
    conn.commit()
    pass

def main():
    # This function calls all the above functions, setting up the database, defining the restaurant types, 
    # grabbing the lists of restaurants, writing the csv, and setting up the database tables.
    
    cur, conn = setUpDatabase('restaurantData.db')

    types = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']
    r1 = restaurantlst('https://www.imdb.com/list/ls008939186/') 
    r2 = restaurantlst('https://www.imdb.com/list/ls054431555/')
    restaurants = r1 + r2

    write_csv(restaurants,'restaurants.csv')

    setUpTypeTable( cur, conn, types)
    setUpRestaurantTable( cur, conn, r1,0)
    setUpRestaurantTable( cur, conn, r2,1,100)
    pass

#main()

restaurantlst('https://www.opentable.com/lists/top-100-2021')
