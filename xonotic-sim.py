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
import time

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
        # To print on the same line
        print("Players registation progress: ", str(round(playerCount/players*100))+"%", end="\r")

    conn.commit()
    print("Total number of players registered", playerCount)
    print()

def startGame(players):
    conn = connectDB()
    cursor = conn.cursor()
    totalPlayers = random.randrange(16, players)

    stmtGame = "INSERT INTO game(game_name, total_players) VALUES(%s, %s)"
    strValues = (strGenerator().title(), totalPlayers)
    cursor.execute(stmtGame, strValues)

    #Fetch the last Game_ID inserted
    stmtGameID = "SELECT LAST_INSERT_ID() as GameID"
    cursor.execute(stmtGameID)
    dfGameID = pd.DataFrame(cursor.fetchall())

    #Assign the column header as "Game_ID" to the Dataframe
    dfGameID.columns = [[ 'game_id' ]]

    #Read the Game_ID from the Dataframe
    iGameID = 0
    if len(dfGameID) > 0:
        iGameID = dfGameID.loc[0]['game_id']
    
    conn.commit()

    stmtPrimaryCursor = "SELECT id FROM profile ORDER BY RAND() LIMIT " + str(totalPlayers)
    cursor.execute(stmtPrimaryCursor)
    dfPlayers = pd.DataFrame(cursor.fetchall())
    dfPlayers.columns = [[ 'id' ]]

    stmtCreateLeaderBoard = "INSERT INTO gameplayer(game_id, player_id, start_time) VALUES"
    strValues = ""

    # Itrate the players list selected from the profile table for this game
    # Insert them with the game_id with some defaults
    for profileRecord in range(len(dfPlayers)):
        strValues +=  "(" + str(iGameID) + ", " + str(dfPlayers.iloc[profileRecord]['id']) + ", current_timestamp(6)), "

    # Close the final string values
    strValues = strValues[:-2]
    stmtCreateLeaderBoard += strValues

    cursor.execute(stmtCreateLeaderBoard)
    conn.commit()

    #Start Game until 1000 total kills
    battleOn(conn, dfPlayers, iGameID)

#Simulate random game play and kills
def battleOn(conn, playerList, gameID):
    cursor = conn.cursor()
    maxKills = random.randrange(500, 10000)

    for totalEvents in range(1, maxKills):
        # Get a random player ID as the RIP dude from the from the Player Dataframe
        randomPlayerID = playerList.iloc[random.randrange(0, len(playerList)-1)]['id']
        # Get a random player ID as the killer from the from the Player Dataframe
        randomKillerID = playerList.iloc[random.randrange(0, len(playerList)-1)]['id']

        stmtKill = "INSERT INTO leaderboard(game_id, player_id, killed_by, killed_time) VALUES(" + \
                        str(gameID) + ", " + str(randomPlayerID) + ", " + str(randomKillerID) + ", current_timestamp(6))"

        cursor.execute(stmtKill)
        time.sleep(random.randrange(0, 1))
        print("Game Progress: ", str(round(totalEvents/maxKills*100))+"%", end="\r")
        conn.commit()

    print("Total global kills in current game", totalEvents)

    # End Game and Update the end time for the particular game
    endGame(conn, gameID)

def endGame(conn, GameID):
    cursor = conn.cursor()
    stmtEnd = "UPDATE game SET end_time = current_timestamp(6)"
    cursor.execute(stmtEnd)
    conn.commit()

if __name__ == "__main__":
    # If only one argument is proviced and it's a number greater than ZERO hen proceed
    if len(sys.argv) == 2 and (sys.argv[1]).isdigit() and sys.argv[1] > "0":
        createPlayers(int(sys.argv[1]))
        startGame(int(sys.argv[1]))
    else:
        print("\nERROR: Invalid command line argument count, player count must be greater than ZERO")
        print("\n   Usage:")
        print("   python3 xonotic-sim.py <Player Count>")
        print("   shell> python3 xonotic-sim.py 256")
        print("\nThe above will generate 256 user profiles\n")
