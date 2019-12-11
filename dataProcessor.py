import spotifyCollection
import weather
import sqlite3
import os
import sys
import requests
from collections import defaultdict
import statistics

#### TO DO ####

def dataCollection():   
    usr_input = input("Do you want to collect data? [y/n]")
    if usr_input.lower() == 'y':  
        dataCollectionHandler()
    elif usr_input.lower() == 'n':
        return
    else:
        print("Invalid input. Please try again.")
        return dataCollection()

def dataCollectionHandler():
    usr_input = input("Would you like to collect track data, weather data, or both? [t/w/b]")
    if usr_input.lower() == 't':
        spotifyCollection.main()
    elif usr_input.lower() == 'w':
        weather.main()
    elif usr_input.lower() == 'b':
        spotifyCollection.main()
        weather.main()
    else:
        print("Invalid input. Please try again.")
        return dataCollectionHandler()

#############################

#### Connect to database ####

def databaseConnection(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

##############################


#### Calculations for popularity and genre ####

def popularityGenre(cur, conn):
    joined_data = []
    for row in cur.execute('SELECT Tracks.Popularity, Genres.Title FROM Tracks INNER JOIN Genres ON Tracks.genre_id=Genres.genre_id'):
        joined_data.append((row[0], row[1]))
    return joined_data

def avgGenrePopularity(data):
    genredict = defaultdict(list)
    for item in data:
        genredict[item[1]].append(item[0])
    genredict = dict(genredict)

    pop_means = []
    for pop in genredict.values():
        popavg = statistics.mean(pop)
        pop_means.append(popavg)

    genres = []
    for genre in genredict:
        genres.append(genre)

    genremeans = {}
    for i in range(len(genres)):
        genremeans[genres[i]] = pop_means[i]
    return genremeans

##############################


def cityTemps(cur, conn):
    joined_data = []
    for row in cur.execute('SELECT Weather_Data.Temp_Min, Weather_Data.Temp_Max, Cities.City FROM Weather_Data INNER JOIN Cities ON Weather_Data.City=Cities.Id'):
        joined_data.append((row[0], row[1], row[2]))
    return joined_data

def main():
    dataCollection()
    cur, conn = databaseConnection('spotifyweather.db')
    genreinfo = popularityGenre(cur, conn)
    genre_means = avgGenrePopularity(genreinfo)
    print(genre_means)

    cityTemps(cur, conn)

if __name__ == "__main__":
    main()
