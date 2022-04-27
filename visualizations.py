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

def getTypeRatingData(db_filename):
    # This function takes in a database filename and restaurant type as its input. It then creates a connection and cursor to the database,
    # and selects several values to calculate the average rating for each restaurant type in the database. It then outputs this 
    # information in a dictionary with the types as the key, and the ratings as the values. 

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    type_average = {}
    count = {}
    entry = {}

    cur.execute('SELECT Restaurants.OpenTable_Rating, Restaurants.Type FROM Restaurants JOIN Types ON Restaurants.Type_ID = Types.Type_ID')
    for row in cur:
        type = row[-1]
        rating = row[0]

        if count.get(type, None) == None:
            count[type] = rating
            entry[type] = 1
        else:
            count[type] += rating
            entry[type] += 1

        for key in count.keys():
            avg = count[key]/entry[key]
            type_average[key] = avg
    print(type_average)
    return type_average

# Visualization #1
def barchart_restaurant_ratings(restaurant_dict1, name):
    # This function takes in a dictionary which contains restaurant types as the keys and average ratings as the values. It also takes 
    # in the preferred filename of the graph which will be returned. The function uses the dictionary to create and decorate a bar chart, 
    # which will compare the average ratings across restaurant types. The function will output a jpeg file, with the preferred name 
    # that was passed into the function.

    restaurant_types = restaurant_dict1.keys()
    restaurant_average_ratings = restaurant_dict1.values()
    
    first_font = {'family':'serif','color':'black','size':15}
    second_font = {'family':'serif','color':'black','size':12}
    
    plt.figure(figsize=(10,12))
    plt.bar(restaurant_types, restaurant_average_ratings, color=['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'pink', 'orange', 'grey', 'purple', 'black', 'brown', 'olive', 'tomato', 'gold', 'wheat', 'aqua', 'coral', 'tan', 'fuchsia', 'lime', 'plum', 'navy', 'orchid', 'crimson', 'teal'])
    plt.xlabel('Restaurant Type', fontdict=second_font)
    plt.ylabel('Restaurant Average Ratings', fontdict=second_font)
    plt.title('Average Rating per Restaurant Type', fontdict=first_font)
    plt.xticks(rotation=90)
    plt.show()
    plt.savefig(name)

def getTypePriceData(db_filename):
    # This function takes in a database filename and restaurant type as its input. It then creates a connection and cursor to the database,
    # and selects several values to calculate the average price for each restaurant type in the database. It then outputs this 
    # information in a dictionary with the types as the key, and the ratings as the values. 

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    type_average = {}
    count = {}
    entry = {}

    # here we would change to Types.Type*
    cur.execute('SELECT Restaurants.OpenTable_Price, Restaurants.Type FROM Restaurants JOIN Types ON Restaurants.Type_ID = Types.Type_ID')
    for row in cur:
        type = row[-1]
        if row[0] == "$":
            price = 1
        elif row[0] == "$$":
            price = 2
        elif row[0] == "$$$":
            price = 3
        elif row[0] == "$$$$":
            price = 4
        
        
        if count.get(type, None) == None:
            count[type] = price
            entry[type] = 1
        else:
            count[type] += price
            entry[type] += 1

        for key in count.keys():
            avg = count[key]/entry[key]
            type_average[key] = avg
    print(type_average)
    return type_average

# Visualization #2
def barchart_restaurant_prices(restaurant_dict2, name):
    # This function takes in a dictionary which contains restaurant types as the keys and locations as the values. It also takes 
    # in the preferred filename of the graph which will be returned. The function uses the dictionary to create and decorate a bar chart, 
    # which will compare the prices across restaurant types. The function will output a jpeg file, with the preferred name
    # that was passed into the function.

    restaurant_types = restaurant_dict2.keys()
    restaurant_average_prices = restaurant_dict2.values()
    
    first_font = {'family':'serif','color':'black','size':15}
    second_font = {'family':'serif','color':'black','size':12}

    plt.figure(figsize=(10,12))
    plt.bar(restaurant_types, restaurant_average_prices, color=['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'pink', 'orange', 'grey', 'purple', 'black', 'brown', 'olive', 'tomato', 'gold', 'wheat', 'aqua', 'coral', 'tan', 'fuchsia', 'lime', 'plum', 'navy', 'orchid', 'crimson', 'teal'])
    plt.xlabel('Restaurant Type', fontdict=second_font)
    plt.ylabel('Restaurant Prices', fontdict=second_font)
    plt.title('Most Common Restaurant Prices per Restaurant Type', fontdict=first_font)
    plt.xticks(rotation=90)
    plt.show()
    plt.savefig(name)

# Visualization #3
def piechart_restaurant_types():
    # Description
    # Description

    dbName ='restaurantData.db'
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    chart_font = {'family':'serif','color':'black','size':15}

    cursor.execute("SELECT * FROM Restaurants")
    AfghanNumber = 0
    AmericanNumber = 0
    ContemporaryAmericanNumber = 0
    ContemporaryFrenchNumber = 0
    ContemporarySouthernNumber = 0
    CroatianNumber = 0
    FarmtotableNumber = 0
    FishNumber = 0
    FrenchAmericanNumber = 0
    FrenchNumber = 0
    FusionNumber = 0
    GreekNumber = 0
    ItalianNumber = 0
    MediterraneanNumber = 0
    MexicanNumber = 0
    PeruvianNumber = 0
    SeafoodNumber = 0
    SouthwestNumber = 0
    SpeakeasyNumber = 0
    SteakNumber = 0
    SteakhouseNumber = 0
    SushiNumber = 0
    TapasSmallPlatesNumber = 0
    TraditionalFrenchNumber = 0
    VietnameseNumber = 0
    WineryNumber = 0
    for row in cursor:
        if row[2] == 'Afghan':
            AfghanNumber += 1
        elif row[2] == 'American':
            AmericanNumber += 1
        elif row[2] == 'Contemporary American':
            ContemporaryAmericanNumber += 1
        elif row[2] == 'Contemporary French':
            ContemporaryFrenchNumber += 1
        elif row[2] == 'Contemporary Southern':
            ContemporarySouthernNumber += 1
        elif row[2] == 'Croatian':
            CroatianNumber+= 1
        elif row[2] == 'Farm-to-table':
            FarmtotableNumber += 1
        elif row[2] == 'Fish':
            FishNumber+= 1
        elif row[2] == 'French American':
            FrenchAmericanNumber+= 1
        elif row[2] == 'French':
            FrenchNumber += 1
        elif row[2] == 'Fusion':
            FusionNumber += 1
        elif row[2] == 'Greek':
            GreekNumber += 1
        elif row[2] == 'Italian':
            ItalianNumber += 1
        elif row[2] == 'Mediterranean':
            MediterraneanNumber += 1
        elif row[2] == 'Mexican':
            MexicanNumber += 1
        elif row[2] == 'Peruvian':
            PeruvianNumber += 1
        elif row[2] == 'Seafood':
            SeafoodNumber += 1
        elif row[2] == 'Southwest':
            SouthwestNumber += 1
        elif row[2] == 'Speakeasy':
            SpeakeasyNumber += 1
        elif row[2] == 'Steak':
            SteakNumber += 1
        elif row[2] == 'Steakhouse':
            SteakhouseNumber += 1
        elif row[2] == 'Sushi':
            SushiNumber += 1
        elif row[2] == 'Tapas / Small Plates':
            TapasSmallPlatesNumber += 1
        elif row[2] == 'Traditional French':
            TraditionalFrenchNumber += 1
        elif row[2] == 'Vietnamese':
            VietnameseNumber += 1
        elif row[2] == 'Winery':
            WineryNumber += 1
    
    names = ['Afghan', 'American', 'Contemporary American', 'Contemporary French', 'Contemporary Southern', 'Croatian', 'Farm-to-table', 'Fish', 'French American', 'French', 'Fusion / Eclectic', 'Greek', 'Italian', 'Mediterranean', 'Mexican', 'Peruvian', 'Seafood', 'Southwest', 'Speakeasy', 'Steak', 'Steakhouse', 'Sushi', 'Tapas / Small Plates', 'Traditional French', 'Vietnamese', 'Winery']
    size_of_groups=[AfghanNumber, AmericanNumber, ContemporaryAmericanNumber, ContemporaryFrenchNumber, ContemporarySouthernNumber, CroatianNumber, FarmtotableNumber, FishNumber, FrenchAmericanNumber, FrenchNumber, FusionNumber, GreekNumber, ItalianNumber, MediterraneanNumber, MexicanNumber, PeruvianNumber, SeafoodNumber, SouthwestNumber, SpeakeasyNumber, SteakNumber,SteakhouseNumber, SushiNumber, TapasSmallPlatesNumber, TraditionalFrenchNumber, VietnameseNumber, WineryNumber]
    colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'pink', 'orange', 'grey', 'purple', 'black', 'brown', 'olive', 'tomato', 'gold', 'wheat', 'aqua', 'coral', 'tan', 'fuchsia', 'lime', 'plum', 'navy', 'orchid', 'crimson', 'teal']
    patches, texts = plt.pie(size_of_groups, colors=colors, startangle=90, autopct=lambda x: f'{x:.1f}%\n({(x/100)*sum(size_of_groups):.0f})')
    plt.legend(patches, names, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.pie(size_of_groups)
    fig = plt.gcf()
    fig.set_size_inches(8,15)
    plt.title('Percentage of Types in List of Restaurants', fontdict=chart_font)
    plt.show()
  
    # plt.pie(size_of_groups, labels=names, labeldistance=1.15)
    # plt.title('Percentage of Types in OpenTable Website', fontdict=first_font)
    # plt.show()

# Visualization #4
def piechart_restaurant_prices():
    # Description
    # Description

    dbName ='restaurantData.db'
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    chart_font = {'family':'serif','color':'black','size':15}

    cursor.execute("SELECT * FROM Restaurants")
    Price1Number = 0
    Price2Number = 0
    Price3Number = 0
    Price4Number = 0
    for row in cursor:
        if row[6] == '$':
            Price1Number += 1
        elif row[6] == '$$':
            Price2Number += 1
        elif row[6] == '$$$':
            Price3Number += 1
        elif row[6] == '$$$$':
            Price4Number += 1
    
    names = ['Least Expensive', 'Second Least Expensive', 'Second Most Expensive', 'Most Expensive']
    size_of_groups=[Price1Number, Price2Number, Price3Number, Price4Number]
    colors = ['red', 'orange', 'green', 'blue']
    patches, texts = plt.pie(size_of_groups, colors=colors, startangle=90)
    plt.legend(patches, names, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.pie(size_of_groups)
    fig = plt.gcf()
    fig.set_size_inches(6,8)
    plt.title('Percentage of Prices in List of Restaurants', fontdict=chart_font)
    plt.show()

getTypeRatingData('restaurantData.db')
barchart_restaurant_ratings(getTypeRatingData('restaurantData.db'), "Restaurant Ratings Per Type.jpeg")
barchart_restaurant_prices(getTypePriceData('restaurantData.db'), "Restaurants Prices Per Type.jpeg")
piechart_restaurant_types()
piechart_restaurant_prices()
