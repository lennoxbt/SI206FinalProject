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
    
    restaurant_names =[]
    restaurant_location =[]
    restaurant_Type = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')

    spans = soup.find_all(class_='CCbGHaorgGHXgJqoOaXl')

    for item in spans:
      restaurantName = item.find('h2', class_='H5kqSXUFObkmV6wfAw7p').text
      restaurantLocation =  item.find('div', class_='GwGPDuPdTZpMt7oIzo4A YQ2SmR3lcmrtTcxuktZA').text
      restaurantType =  item.find('div', class_= 'UNOIq8wcqctrC7s3wHAW YQ2SmR3lcmrtTcxuktZA').text
      restaurant_names.append(restaurantName)
      restaurant_Type.append(restaurantType)
      restaurant_location.append(restaurantLocation)

    #print(restaurant_location)
    #print(restaurant_names)
    #print(list(zip(restaurant_names, restaurant_location)))
    restaurantlst = list(zip(restaurant_names, restaurant_Type, restaurant_location))
    print(restaurantlst)
    return restaurantlst


def setUpDatabase(db_name):
  # This function simply takes in a string as input which contains the preferred database file name, and 
  # returns the cursor and connection to the created database.

   path = os.path.dirname(os.path.abspath(__file__))
   conn = sqlite3.connect(path+'/'+db_name)
   cur = conn.cursor()

   return cur, conn
  

  #Create restaurant table if not exists 

def setUpRestaurantTable(cur, conn, restaurantlst, x = 0):
  # This takes a database cursor and conneciton, list of restaurant names, restaurant type, and optional 
  # argument which specifies the starting position of the database id. The function creates a table, Restaurants, 
  # within the passed database and inserts each restaurant in restaurantlist, along with its corresponding id, location, and type.
  cur.execute("CREATE TABLE IF NOT EXISTS Restaurants (id INTEGER PRIMARY KEY,Name TEXT,Type TEXT,Location TEXT, opentable_rating FLOAT, YELP1 INTEGER, YELP2 FLOAT, YELP3 FLOAT, YELP4 FLOAT)")
  for num in range(len(restaurantlst)):
    id = num + x
    cur.execute("INSERT INTO Restaurants (id,Name,Type,Location) VALUES (?,?,?,?)",(id,restaurantlst[num][0],restaurantlst[num][1],restaurantlst[num][2]))
  conn.commit()

  
  # Create Type table is not exists

# def setUpTypeTable(cur, conn, typelst):
#     # This function takes in a databse cursor and connection, as well as a list of movie genres. It then creates
#     # a table, Types, within the database, along with its corresponding id number.
#     cur.execute("CREATE TABLE IF NOT EXISTS Genres (id INTEGER PRIMARY KEY, genre TEXT)")
#     for i in range(len(restaurantlst)):
#         cur.execute("INSERT OR IGNORE INTO Genres (id, genre) VALUES (?,?)", (i, restaurantlst[i]))
#     conn.commit()
#     pass

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



restaurantlst('https://www.opentable.com/lists/top-100-2021')

def main():

  restaurant_tuple_lst = restaurantlst('https://www.opentable.com/lists/top-100-2021')
  
  cur, conn = setUpDatabase('restaurantData.db')
  setUpRestaurantTable(cur, conn, restaurant_tuple_lst, x = 0)



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
