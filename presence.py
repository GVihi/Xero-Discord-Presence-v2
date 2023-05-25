from pypresence import Presence
import time
from bs4 import BeautifulSoup
import requests
import json
import credentials

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

info =  bcolors.OKGREEN + "[INFO:] " + bcolors.ENDC
debug = bcolors.WARNING + "[DEBUG:] " + bcolors.ENDC
err =   bcolors.FAIL + "[ERROR:] " + bcolors.ENDC

def getTime():
    return bcolors.OKBLUE + "[" + time.strftime("%H:%M:%S", time.gmtime(time.time())) +"] " + bcolors.ENDC

#Attempt to connect to Discord
def discordConnect():
    global connected
    try:
        print(getTime() + info + "Attempting to connect to Discord!")
        global RPC
        RPC = Presence(credentials.app_id)
        RPC.connect()
        connected = "true"
        print(getTime() + info + "Connection successful!\n")
    except:
        time.sleep(1)
        print(getTime() + err + "Failed to connect to Discord!")
        time.sleep(1)
        print(getTime() + info + "Exiting application...")
        time.sleep(1)
        quit()

#Stop presence and disconnect from Discord
def discordDisconnect():
    print(getTime() + info + "Disconnecting from Discord")
    RPC.clear()

def main():
    print(getTime() + info + "Starting Rich Presence for Xero...\n")

    global connected
    connected = "false"

    #Rich presence variables
    detail = ""
    status = ""

    #p - player
    pName = ""
    pLevel = ""
    pRankPercentage = ""

    pRoomId = ""
    pGameState = ""
    pGameMode = ""
    pChannel = ""

    smallImg = ""
    smallImg_tooltip = ""


    try:
        while True:
            #Loop every second
            time.sleep(1)
            gotData = "false"
            #Attempt to get game data from Xero API
            try:
                r = requests.get("https://xero.gg/api/self/status/", headers={"x-api-access-key-id" : credentials.id, "x-api-secret-access-key": credentials.secret})
                doc = BeautifulSoup(r.text, "html.parser")
                doc = str(doc)
                data = json.loads(doc)
                data = json.dumps(data, indent=4)
                #print(data)
                data = json.loads(data)
                gotData = "true"
            except:
                print(getTime() + err + "Unable to access Xero API!")
                print(getTime() + info + "Attempting to get data in 15 seconds!")
                gotData = "false"
                time.sleep(15)

            if gotData == "true":
                #If player is Online, connect to Discord
                if data['game']['online'] == True:
                    #Had trouble with KeyError 'game' due to trying to compare boolean True to string "true"
                    #print(getTime() + debug + str(data['game']['online']))
                    if connected == "false":
                        print(getTime() + info + data['info']['name'] + " is online!")
                        discordConnect()
                        start_time = int(time.time())

                    #Get player name, level and xp data
                    pName = data['info']['name']
                    pLevel = data['info']['progression']['level']['value']
                    pRankPercentage = data['info']['progression']['level']['progress']['percentage']

                    smallImg = "checkmark"
                    smallImg_tooltip = pName + " is online"
    
                    #Set rich presence "details" parameter to values above ^
                    detail = pName + ", Rank " + str(pLevel) + " (" + str(pRankPercentage) + "%)"

                    #Check if player is in a room
                    try:
                        if data['game']['room'] == None:
                            status = data['game']['channel']['name']
                        else:
                            pRoomId = data['game']['room']['id']
                            pGameMode = data['game']['room']['mode']['name']
                            if pGameMode == "Touchdown": pGameMode = "TD"
                            if pGameMode == "Deathmatch": pGameMode = "DM"
                            if pGameMode == "Battle Royal": pGameMode = "BR"
                            pChannel = data['game']['channel']['name']

                            #When player is in a room, check gameState
                            if data['game']['room']['match']['gameState']['name'] == "Playing":
                                pGameState = data['game']['room']['match']['gameTimeState']['name']
                                if pGameState == "FirstHalf": pGameState = "First Half"
                                if pGameState == "SecondHalf": pGameState = "Second Half"
                            else:
                                pGameState = data['game']['room']['match']['gameState']['name']
                            
                            status = pChannel + " #" + str(pRoomId) + ", " + pGameMode + ", " + pGameState

                            if pGameState == "None":
                                status = pChannel +  " #" + str(pRoomId) + ", " + pGameMode

                            if data['game']['room']['isPasswordProtected'] == True:
                                smallImg = "locked"
                                smallImg_tooltip = "Room #" + str(pRoomId) + " is locked"
                            else:
                                smallImg = "unlocked"
                                smallImg_tooltip = "Room #" + str(pRoomId) + " is unlocked"
                                    
                    except Exception as e:
                        print(getTime() + err + "Something went wrong while getting room data.")
                        print(getTime() + debug + str(e))
                        print(getTime() + info + "Retrying... \n")
                
                    pLink = "https://xero.gg/player/" + pName

                    RPC.update(
                        start=start_time,
                        details=detail,
                        state=status,
                        large_image="image",
                        small_image=smallImg,
                        small_text=smallImg_tooltip,
                        buttons=[{"label":"View Profile","url":pLink}]
                    )

                else:
                    if connected == "true":
                        print(getTime() + info + data['info']['name'] + " went offline!")
                        discordDisconnect()
                        connected = "false"
                            

            

            
    except KeyboardInterrupt:
        pass

    print(getTime() + info + "Exiting application...")
    if connected == "true":
        discordDisconnect()




if __name__ == "__main__":
    main()