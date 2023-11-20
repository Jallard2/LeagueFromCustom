import pygsheets
import pandas as pd
import json

class Connection(object):
    def __init__(self):
        self.gc = pygsheets.authorize(service_file = 'client_secret.json')
        self.sh = self.gc.open('Meatballers Customs Data')
        self.wks = self.sh[0]
        with open('completed.json', 'r') as f:
            data = json.load(f)

        # print(data)

        games = len(data)
        if games == 0:
            self.row = 1
        else:
            self.row = games * 9 + 1
        self.headers = [
            'PlaceHolder',
            'Name',
            'Champion',
            'Kills',
            'Deaths',
            'Assists',
            'Level',
            'Gold Earned',
            'CS',
            'Dmg Champs',
            'Dmg Turrets',
            'Dmg Mitigated',
            'Vision Score',
            'Win',
            'Game Duration',
            'PlayedFor',
        ]

        self.currentSheet = self.sh.worksheet_by_title('Games')

    def makeHeaders(self, matchId:str, lane:str, duration:int):
        matchId = matchId.removesuffix(".json")
        self.headers[0] = matchId
        self.headers[len(self.headers) - 1] = lane
        self.headers[len(self.headers) - 2] = f"{duration} Minutes"
        dataRange = pygsheets.DataRange(start=f'A{self.row}', end=f'P{self.row}', worksheet=self.wks)
        model_cell = self.wks.cell((1,1))
        model_cell.set_text_format('bold', True).set_horizontal_alignment(pygsheets.custom_types.HorizontalAlignment.CENTER)
        dataRange.apply_format(model_cell)
        self.currentSheet.update_values(f"A{self.row}", [self.headers])
        # self.currentSheet.format(f"{self.row}", {'textFormat': {'bold': True}})
        self.row += 1

    def makeEntry(self, data: dict):
        # self.currentSheet.append_table(data)
        self.currentSheet.update_values(f"A{self.row}", [data])
        self.row += 1

    def skipRow(self):
        self.row += 3

    def addScores(self, scaleFactor):
        for i in range(5, 0, -1):
            current = float(self.currentSheet.get_value(f"P{self.row - i}"))
            # print(current)
            self.currentSheet.update_value(f"P{self.row - i}", round(current / (scaleFactor / 100), 2) * 100)

