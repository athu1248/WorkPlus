import datetime
import json
import random
import datetime

# generates a random question from a large trivia dataset 
class Quiz():
    def __init__(self, *args, **kwargs):
        with open('fitness/triviadata/WWTBAM JSON File.json', "r") as f:
            self.data = json.load(f)
            self.index = datetime.datetime.today().day
            self.question = self.data[self.index]["question"]
            self.A = self.data[self.index]["A"]
            self.B = self.data[self.index]["B"]
            self.C = self.data[self.index]["C"]
            self.D = self.data[self.index]["D"]
            self.answer = self.data[self.index]["answer"]
            self.option = self.data[self.index][self.answer]

            self.CHOICES = [
                ("A", self.A),
                ("B", self.B),
                ("C", self.C),
                ("D", self.D),
            ]
