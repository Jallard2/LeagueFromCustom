import json
import os

class GatherData():
    def __init__(self):
        with open("completed.json", "r") as f:
            self.completed: list[str] = json.load(f)

    def getGames(self):
        folders = ['BotGames', 'JgGames', 'MidGames', 'TopGames']

        for folder in folders:
            for file in os.listdir(folder):
                if file not in self.completed:
                    # self.completed.append(file)
                    with open(f"{folder}/{file}", 'r') as f:
                        data = json.load(f)

                    data['playedFor'] = folder.removesuffix('Games')

                    self.detectData(data)
                    
                    with open(f"{folder}/{file}", 'w') as f:
                        json.dump(data, f, indent=2)

        with open('completed.json', 'w') as f:
            json.dump(self.completed, f)

    def detectData(self, data: dict):
        print(data.get('playedFor'))
        print(data.get('participants'))


GatherData().getGames()