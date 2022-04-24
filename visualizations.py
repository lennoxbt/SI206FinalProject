# Winter 2022 Final Project
# SI 206
# Name: Lennox Thomas & Nicole Surcel

from sqlite3.dbapi2 import Row
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import average
import requests
import re
import csv
import os
import sqlite3

def getTypeRatingData(db_filename, label):
    # This function takes in a database fiilename and restaurant type as its input. It then creates a connection and cursor to the database,
    # and selects several values to calculate the average rating for each restaurant type in the database. It then outputs this 
    # information in a dictionary with the types as the key, and the ratings as the values. 

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    # typeavg = {}
    # count = {}
    # entry = {}

    # typeavgb = {}
    # countb = {}
    # entryb = {}

    # cur.execute('SELECT rating, type FROM Restaurants JOIN Types ON Restaurants.typeid = Types.id WHERE label='+str(label),)
    # for row in cur:
    #     typ = row[-1]
    #     rating = row[0]

    #     if count.get(typ,None) == None:
    #         count[typ] = rating
    #         entry[typ] = 1
    #     else:
    #         count[typ] += rating
    #         entry[typ] += 1

    #     for key in count.keys():
    #         avg = count[key]//entry[key]
    #         typeavg[key] = avg
    # return typeavg
    pass

def barchart_restaurants(restaurant_dict, name):
    # This function takes in a dictionary which contains restaurant types as the keys and average ratings as the values. It also takes 
    # in the preferred filename of the graph which will be returned. The function uses the dictionary to create and decorate a bar chart, 
    # which will compare the average ratings across restaurant types. The function will output a jpeg file, with the preferred name 
    # which was passed into the function.

    restaurant_types = restaurant_dict.keys()
    restaurant_average_ratings = restaurant_dict.values()
    
    first_font = {'family':'serif','color':'black','size':15}
    second_font = {'family':'serif','color':'black','size':12}
    
    plt.figure(figsize = (10,12))
    plt.bar(restaurant_types, restaurant_average_ratings, color = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'pink', 'orange', 'grey', 'purple', 'black', 'brown', 'olive', 'tomato', 'gold', 'wheat', 'aqua', 'coral', 'tan', 'fuchsia', 'lime', 'plum', 'navy', 'orchid', 'crimson'])
    plt.xlabel('Restaurant Type Category', fontdict = second_font)
    plt.ylabel('Restaurant Average Ratings', fontdict = second_font)
    plt.title('Average Rating per Restaurant Type Category', fontdict = first_font)
    plt.xticks(rotation = 90)
    plt.show()
    plt.savefig(name)

def scatter_restaurants():
    # This function takes no input, as it is designed to iterate through the ratings.csv file to create two dictionaries which contain 
    # both the average critic rating and price for each restaurant. These dictionaries are then used to create a scatter plot which compares 
    # the average critic ratings and price for each restaurant, across both restaurant types.

    # path = os.path.dirname(os.path.abspath(__file__))
    # conn = sqlite3.connect(path+'/movieData.db')
    # cur = conn.cursor()

    # restaurant1 = {}
    # restaurant2 = {}

    # with open('ratings.csv', 'r') as file:
    #     reader = csv.reader(file)
    #     next(reader)
    #     for row in reader:
    #         title = row[0]
    #         rating = row[2]
    #         type = row[-1]
    #         price = row[-2]
    #         if int(type) == 0:
    #             restaurant1[title] = [rating,price]
    #         else:
    #             restaurant2[title] = [rating,price]
    # sortedm1 = sorted(restaurant1.values(), key = lambda x: x[0])
    # sortedm2 = sorted(restaurant2.values(), key = lambda x: x[0])
    # #print(sortedm1)
    # wratings = []
    # wprice = []
    # for key in sortedm1:
    #     rating = key[0]
    #     price = key[1]
    #     wratings.append(rating)
    #     wprice.append(price)
    # bratings = []
    # bprice = []
    # for key in sortedm2:
    #     rating = key[0]
    #     price = key[1]
    #     bratings.append(rating)
    #     bprice.append(price)
    
    # #print(wgross,wratings)
    # plt.figure(figsize=(11,6))

    # plt.scatter(bratings,bprice, color='blue',marker='x',s=25,label='Black Restaurants',edgecolor='black')
    # plt.scatter(wratings,wprice, color='green',marker='o',s=25,label='White Restaurans',edgecolor='black')
    # plt.xticks(np.arange(len(bratings)),bratings, rotation=90)
    
    # font1 = {'family':'serif','color':'black','size':20}
    # font2 = {'family':'serif','color':'black','size':15}
    # plt.yscale('log')
    # plt.xlabel('Average Rating',fontdict = font2)
    # plt.ylabel('Price ($)',fontdict = font2)
    # plt.title('Price vs Average Rating',fontdict = font1)
    # plt.legend(loc="upper left")
    
    # plt.savefig('ScatterGraph.jpeg')
    # plt.tight_layout()
    # plt.show()
    pass

def main():
    # This function calls the above functions, getTypeRatingData, barchart_restaurants, and scatter_restaurants to create the visuals needed 
    # to compare and analyze the collected data.

    barchart_restaurants()
    # whitem = getTypeRatingData('restaurantData.db',0)
    # blackm = getTypeRatingData('restaurantData.db',1)
    # barchart_restaurants(blackm,'BarChartBlackRestaurants.jpeg')
    # barchart_restaurants(whitem,'BarChartWhiteRestaurants.jpeg')
    # scatter_restaurants()
    #barchart_restaurants(dictionaries)
    #scatter_restaurants(dictionaries)
    pass

main()
