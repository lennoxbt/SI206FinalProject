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
    restaurant_location = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')

    spans = soup.find_all(class_='CCbGHaorgGHXgJqoOaXl')

    for item in spans:
      resturantName = item.find(class_='H5kqSXUFObkmV6wfAw7p').text
      resturantLocation =  item.find(class_='GwGPDuPdTZpMt7oIzo4A YQ2SmR3lcmrtTcxuktZA').text
      restaurant_names.append(resturantName)
      restaurant_location.append(resturantLocation)

    #print(restaurant_location)
    #print(restaurant_names)
    #print(list(zip(restaurant_names, restaurant_location)))
    restaurantlst = list(zip(restaurant_names, restaurant_location))
    return restaurantlst



# Write restuaurant list into a CSV file
def write_csv(data, filename):
  # This file takes in a list of tuples and csv filename as input. It then iterates through the list of tuples 
  # to write multiple rows within the csv, outputting a csv file containing each restaurant name and restaurant location.
  
  header = ('Restaurant Name', 'Restaurant Location') #, 'Rating')

  with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for item in data:
      writer.writerow(item)
  
  # Setup database file

def setUpDatabase(db_name):
  # This function simply takes in a string as input which contains the preferred database file name, and 
  # returns the cursor and connection to the created database.
  
  path = os.path.dirname(os.path.abspath(__file__))
  conn = sqlite3.connect(path+'/'+db_name)
  cur = conn.cursor()
  
  return cur, conn
  
  # Create restaurant table if not exists

def setUpRestaurantTable(cur, conn, restaurantlst,type, x = 0):
  # This file takes a database cursor and conneciton, list of restaurant names, restaurant type, and optional 
  # argument which specifies the starting position of the database id. The function creates a table, Restaurants, 
  # within the passed database and inserts each restaurant in restaurantlist, along with its corresponding id, location, and type.

  # cur.execute("CREATE TABLE IF NOT EXISTS Restaurants (id INTEGER PRIMARY KEY, name TEXT, location TEXT, typeid TEXT, openhouse_rating FLOAT, yelp_rating FLOAT, label INTEGER)") # "CREATE TABLE IF NOT EXISTS Restaurants (id INTEGER PRIMARY KEY, name TEXT, location TEXT, typeid TEXT, openhouse_rating FLOAT, awards INTEGER, yelp_rating FLOAT, metascore FLOAT, rotten_tomatoes FLOAT, label INTEGER)")
  # for num in range(len(restaurantlst)):
  #   id = num + x
  #   cur.execute("INSERT INTO Restaurants (id,name,location,label) VALUES (?,?,?,?)",(id,restaurantlst[num][0],restaurantlst[num][1],type))
  # conn.commit()
  pass
  
  # Create Type table is not exists

def setUpTypeTable(cur, conn, typelst):
  # This function takes in a databse cursor and connection, as well as a list of restaurant types. It then creates
  # a table, Types, within the database, along with its corresponding id number.
  
  # cur.execute("CREATE TABLE IF NOT EXISTS Types (id INTEGER PRIMARY KEY, type TEXT)")
  # for i in range(len(restaurantlst)):
  #   cur.execute("INSERT OR IGNORE INTO Types (id, type) VALUES (?,?)", (i, restaurantlst[i]))
  # conn.commit()
  pass

def main():

  restaurant_tuple_lst = restaurantlst('https://www.opentable.com/lists/top-100-2021')
  write_csv(restaurant_tuple_lst,'restaurant.csv')
  cur, conn = setUpDatabase('restaurantData.db')
  setUpRestaurantTable(cur, conn, restaurantlst,type, x = 0)

main()

# def main():
#     # This function calls all the above functions, setting up the database, defining the restaurant types, 
#     # grabbing the lists of restaurants, writing the csv, and setting up the database tables.
    
#     cur, conn = setUpDatabase('restaurantData.db')

#     genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']
#     m1 = movielst('https://www.imdb.com/list/ls008939186/') 
#     m2 = movielst('https://www.imdb.com/list/ls054431555/')
#     movies = m1 + m2

#     write_csv(movies,'movies.csv')

#     setUpGenreTable( cur, conn, genres)
#     setUpMovieTable( cur, conn, m1,0)
#     setUpMovieTable( cur, conn, m2,1,100)
#     pass
