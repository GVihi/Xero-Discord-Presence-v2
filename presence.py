from pypresence import Presence
import time
from bs4 import BeautifulSoup
import requests
import json
import credentials
import datetime

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
        print(getTime() + info + "Attempting to connect to Discord...")
        global RPC
        RPC = Presence(credentials.app_id)
        RPC.connect()
        connected = "true"
        print(getTime() + info + "Connection successful!\n")
    except:
        time.sleep(1)
        print(getTime() + err + "Failed to connect to Discord!")
        print(getTime() + info + "Make sure Discord is running! \n")
        time.sleep(1)
        print(getTime() + info + "Exiting application...")
        time.sleep(1)
        quit()

#Stop presence and disconnect from Discord
def discordDisconnect():
    print(getTime() + info + "Disconnecting from Discord")
    RPC.clear()

def main():
    print(getTime() + info + "Starting Rich Presence for Xero...")
    print(getTime() + info + "Waiting for user to appear online...\n")

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

    largeImg = ""
    
    smallImg = ""
    smallImg_tooltip = ""

    statusSwitchCounter = 0
    isTDorDM = "false"
    isTDorDM_andPlaying = "false"

    isBRorChaser = "false"
    isBRorChaser_andPlaying = "false"

    status2 = "Placeholder text"

    idle_timer = 0
    idle = "false"
    idle_start = 0

    largeImageLobbyCounter = 0


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
                print(getTime() + info + "Attempting to get data in 5 seconds!")
                gotData = "false"
                time.sleep(5)

            if gotData == "true":
                #If player is Online, connect to Discord
                if data['game']['online'] == True:
                    #Had trouble with KeyError 'game' due to trying to compare boolean True to string "true"
                    #print(getTime() + debug + str(data['game']['online']))
                    if connected == "false":
                        print(getTime() + info + data['info']['name'] + " is online! \n")
                        discordConnect()
                        start_time = int(time.time())

                    #Get player name, level and xp data
                    pName = data['info']['name']
                    pLevel = data['info']['progression']['level']['value']
                    pRankPercentage = data['info']['progression']['level']['progress']['percentage']

                    largeImageLobbyCounter+=1

                    largeImg = "image"
                    smallImg = "checkmark"
                    smallImg_tooltip = pName + " is online"

                    if largeImageLobbyCounter < 5:
                        largeImg = data['info']['progression']['level']['image']

                    if largeImageLobbyCounter == 10:
                        largeImageLobbyCounter = 0
    
                    #Set rich presence "details" parameter to values above ^
                    detail = pName + ", Rank " + str(pLevel) + " (" + str(pRankPercentage) + "%)"

                    #Check if player is in a room
                    try:
                        if data['game']['room'] == None:
                            status = data['game']['channel']['name']
                            if idle == "false":
                                idle_start = int(time.time())
                                idle = "true"
                            
                            idle_timer = int(time.time()) - idle_start

                            #If player is in channel select or room browser for 90 seconds, set small_image and small_text to "Idle" status
                            if idle_timer > 90:
                                status = status + ", Idle (" + str(datetime.timedelta(seconds=idle_timer)) + ")"
                                smallImg = "idle"
                                smallImg_tooltip = pName + " is idle"
                        else:
                            idle = "false"
                            idle_timer = 0
                            isTDorDM_andPlaying = "false"
                            isTDorDM = "false"
                            isBRorChaser = "false"
                            isBRorChaser_andPlaying = "false"
                            pRoomId = data['game']['room']['id']
                            pGameMode = data['game']['room']['mode']['name']
                            if pGameMode == "Touchdown": 
                                pGameMode = "TD"
                                isTDorDM = "true"
                                #print(getTime() + debug + "TD or DM: " + isTDorDM)
                            if pGameMode == "Deathmatch": 
                                pGameMode = "DM"
                                isTDorDM = "true"
                            if pGameMode == "Battle Royal": 
                                pGameMode = "BR"
                                isBRorChaser = "true"
                            if pGameMode == "Chaser":
                                isBRorChaser = "true"
                            pChannel = data['game']['channel']['name']

                            #When player is in a room, check gameState
                            if data['game']['room']['match']['gameState']['name'] == "Playing":
                                pGameState = data['game']['room']['match']['gameTimeState']['name']
                                if pGameState == "FirstHalf": pGameState = "First Half"
                                if pGameState == "SecondHalf": pGameState = "Second Half"

                                if isTDorDM == "true":
                                    isTDorDM_andPlaying = "true"
                                    #print(getTime() + debug + "Getting match score and calculating time remaining")
                                    pTimeLimit = data['game']['room']['timeLimit']
                                    pRoundTime = data['game']['room']['match']['roundTime']

                                    pMap = data['game']['room']['map']['name']
                                    largeImg = data['game']['room']['map']['image']

                                    timeRemaining = (pTimeLimit / 2) - pRoundTime
                                    timeRemaining = datetime.timedelta(seconds=timeRemaining)

                                    status2 = pMap + " | " + str(timeRemaining)

                                    #Joining an ongion match and waiting in room lobby throws NoneType error, because you can't
                                    #view the score, hence the necessary check
                                    if data['game']['room']['match']['modeData'] != None:
                                        pScoreAlpha = data['game']['room']['match']['modeData']['score']['alpha']
                                        pScoreBeta = data['game']['room']['match']['modeData']['score']['beta']
                                        status2 = pMap + " | " + str(pScoreAlpha) + "-" + str(pScoreBeta) + " | " + str(timeRemaining)
                                    
                                if pGameState == "HalfTime":
                                    isTDorDM_andPlaying = "false"
                                    pGameState = "Half Time"

                                if isBRorChaser == "true":
                                    isBRorChaser_andPlaying = "true"
                                    pTimeLimit = data['game']['room']['timeLimit']
                                    pRoundTime = data['game']['room']['match']['roundTime']
                                    pMap = data['game']['room']['map']['name']
                                    largeImg = data['game']['room']['map']['image']

                                    timeRemaining = pTimeLimit - pRoundTime
                                    timeRemaining = datetime.timedelta(seconds=timeRemaining)

                                    status2 = pMap + " | " + str(timeRemaining)


                            else:
                                pGameState = data['game']['room']['match']['gameState']['name']
                            
                            status = pChannel + " #" + str(pRoomId) + ", " + pGameMode + ", " + pGameState

                            if pGameState == "None":
                                status = pChannel +  " #" + str(pRoomId) + ", " + pGameMode

                            if isTDorDM == "true" and isTDorDM_andPlaying == "true" and statusSwitchCounter < 10:
                                #print(getTime() + debug + "statusSwitchCounter: " + str(statusSwitchCounter) + "\n")
                                if statusSwitchCounter < 5:
                                    status = status2
                                
                                statusSwitchCounter+= 1
                                
                                if statusSwitchCounter == 10:
                                    statusSwitchCounter = 0

                            if isBRorChaser == "true" and isBRorChaser_andPlaying == "true" and statusSwitchCounter < 10:
                                if statusSwitchCounter < 5:
                                    status = status2
                                
                                statusSwitchCounter+= 1
                                
                                if statusSwitchCounter == 10:
                                    statusSwitchCounter = 0

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

                    try:
                        RPC.update(
                            start=start_time,
                            details=detail,
                            state=status,
                            large_image=largeImg,
                            small_image=smallImg,
                            small_text=smallImg_tooltip,
                            buttons=[{"label":"View Profile","url":pLink}]
                        )
                    except Exception as e:
                        print(getTime() + err + "An error occured while communicating with Discord.")
                        print(getTime() + err + "Unable to update rich presence.")
                        print(getTime() + debug + str(e))
                        print(getTime() + info + "Retrying... \n")
                        connected = "false"

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