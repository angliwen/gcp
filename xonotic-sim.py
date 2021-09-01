#####################################################
# Author: Faisal Saeed
# Team: 6m11 Team1
# Date 2021-09-02, post midnignt and very tired
#####################################################

from datetime import datetime
import numpy as np
import pandas as pd
import mysql.connector
import sys
import string
import random

# Returns a randomized string
def strGenerator(chars=string.ascii_uppercase):
    size = random.randrange(4, 15)
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(size))

#Creates a connection to the CloudSQL database instance
def connectDB():
    conn = mysql.connector.connect(
        user="game_user",
        password="password",
        host='10.29.182.2',
        db="xonoticdb"
    )
    return conn

# Reads data from leaderboard table
def readData():
    conn = connectDB()
    # Execute a query
    cursor = conn.cursor()
    cursor.execute("SELECT * from leaderboard")

    # Fetch the results
    result = cursor.fetchall()

    # Do something with the results
    for row in result:
        print(row)

# Creates player profiles using randomized strings
def createPlayers(players):
    conn = connectDB()
    cursor = conn.cursor()

    for playerCount in range(players+1):
        # Generate Random Values
        strName = strGenerator().title() + " " + strGenerator().title()
        strEmail = strGenerator().lower() + "@" + strGenerator().lower() + ".com"

        strInventory = '{'
        # Randon Inventory size from 1 to 10
        for i in range(1, random.randrange(2,10)):
            strInventory += '"item-' + str(i) + '":"' + strGenerator().lower() + '", '

        # Remove the last ", " from the string and close the JSON string with "}"
        strInventory = strInventory[:-2] + '}'

        iLevel = random.randrange(1, 100)

        # Generate SQL
        strStatement = ("INSERT INTO xonoticdb.profile(user_name, user_email, user_inventory, user_level) "
                        "VALUES(%s, %s, %s, %s)")
        strValues = (strName, strEmail, strInventory, iLevel)

        #print(strValues)
        cursor.execute(strStatement, strValues)
        conn.commit()
        # To print on the same line
        print("Players registation progress: ", str(round(playerCount/players*100))+"%", end="\r")

    print()
    print("Total number of players registered", playerCount)

def startGame(players):
    conn = connectDB()

if __name__ == "__main__":
    # If only one argument is proviced and it's a number greater than ZERO hen proceed
    if len(sys.argv) == 2 and (sys.argv[1]).isdigit() and sys.argv[1] > "0":
        createPlayers(int(sys.argv[1]))
    else:
        print("\nERROR: Invalid command line argument count, player count must be greater than ZERO")
        print("\n   Usage:")
        print("   python3 xonotic-sim.py <Player Count>")
        print("   shell> python3 xonotic-sim.py 256")
        print("\nThe above will generate 256 user profiles\n")
