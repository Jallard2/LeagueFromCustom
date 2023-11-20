import json
import os
from sheets import Connection

class GatherData():
    def __init__(self):
        self.connection = Connection()
        with open("completed.json", "r") as f:
            self.completed: list[str] = json.load(f)

    def getGames(self):
        folders = ['BotGames', 'JungleGames', 'MiddleGames', 'TopGames']
        # folders = ['TopGames']

        for folder in folders:
            for file in os.listdir(folder):
                if file not in self.completed:
                    self.completed.append(file)
                    with open(f"{folder}/{file}", 'r') as f:
                        data = json.load(f)

                    data['playedFor'] = folder.removesuffix('Games')
                    self.connection.makeHeaders(file, data['playedFor'], int(int(data['gameDuration']) / 60000))
                    self.detectData(data)
                    
                    with open(f"{folder}/{file}", 'w') as f:
                        json.dump(data, f, indent=2)

        with open('completed.json', 'w') as f:
            json.dump(self.completed, f)

    def detectData(self, data: dict):
        # print(data.get('playedFor'))
        # pprint.pprint(data.get('participants'))
        maxDmg = 0
        maxGold = 0
        maxCsm = 0
        player:dict
        for player in data.get('participants'):
            ssData = []
            lane = player.get('INDIVIDUAL_POSITION')
            if lane == 'UTILITY':
                lane = 'SUPPORT'
            ssData.append(lane.title())
            ssData.append(player.get('NAME'))
            ssData.append(player.get('SKIN'))
            ssData.append(player.get('CHAMPIONS_KILLED'))
            ssData.append(player.get('NUM_DEATHS'))
            ssData.append(player.get('ASSISTS'))
            ssData.append(player.get('LEVEL'))
            ssData.append(player.get('GOLD_EARNED'))
            cs = int(player.get('MINIONS_KILLED')) + int(player.get('NEUTRAL_MINIONS_KILLED'))
            ssData.append(cs)
            ssData.append(player.get('TOTAL_DAMAGE_DEALT_TO_CHAMPIONS'))
            ssData.append(player.get('TOTAL_DAMAGE_DEALT_TO_TURRETS'))
            ssData.append(player.get('TOTAL_DAMAGE_SELF_MITIGATED'))
            ssData.append(player.get('VISION_SCORE'))
            ssData.append(player.get('WIN'))

            playerScore = int(player.get('TOTAL_DAMAGE_DEALT_TO_CHAMPIONS')) * .55 + int(player.get('GOLD_EARNED')) * .35 + (cs / int((int(data.get('gameDuration')) / 60000)) * .1)
            ssData.append("")
            ssData.append(round(int(playerScore) / 100.0, 2))

            maxDmg = max(maxDmg, int(player.get('TOTAL_DAMAGE_DEALT_TO_CHAMPIONS')))
            maxGold = max(maxGold, int(player.get('GOLD_EARNED')))
            maxCsm = max(maxCsm, (cs / int((int(data.get('gameDuration')) / 60000))))

            self.connection.makeEntry(ssData)

        
        scaleFactor = maxDmg * .55 + maxGold * .35 + maxCsm * .1
        # print(scaleFactor)
        self.connection.addScores(scaleFactor)

        self.connection.skipRow()
            


GatherData().getGames()