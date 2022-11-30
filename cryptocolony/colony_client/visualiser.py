import requests
from tkinter import *
from cryptocolony.colony_client.core_controller import CoreController


class VisualiserWindow:
    def __init__(self, coreController):
        self.coreController = coreController
        self.currentIndex = 0
        self.frameUpdateIteration = 0
        self.firstIteration = True
        self.isUpdated = False
        self.bots = []
        self.root = Tk()
        self.root.title("Colony Visualiser")
        self.root.geometry("500x500")

        self.canvas = Canvas(self.root, bg="white")
        self.canvas.pack()

        self.colonyName = Entry(self.root, width=20, bg="white", fg="black")
        self.colonyButton = Button(self.root, text="Submit", command=self.submitColonyName)
        self.botColony = Entry(self.root, width=20, bg="white", fg="black")
        self.botButton = Button(self.root, text="Submit", command=self.submitBotColony)

        self.colonyLabel = Label(self.root, text="Colony Name")
        self.colonyLabel.pack()

        self.colonyName.pack()
        self.colonyButton.pack()

        self.botLabel = Label(self.root, text="Bot Name")
        self.botLabel.pack()

        self.botColony.pack()
        self.botButton.pack()

        self.virtualCore = VisualCoreController(self.canvas)

    def renderText(self, message: str, posX, posY):

        renderFill = "black"
        renderFont = "Times 7"

        try:
            self.canvas.create_text(posX, posY, fill=renderFill, font=renderFont, text=message)
        except Exception as e:
            print(e)

    def addBot(self):
        self.bots.append(VisualBot(self.root, self.canvas, self.currentIndex))
        self.currentIndex += 1

    def updateBotData(self, colonyName: str):
        url = "http://65.108.214.180/api/v1/colony/%s" % colonyName
        try:
            response = requests.get(url)
        except Exception as e:
            response = None
            print(e)

        json = response.json()

        self.frameUpdateIteration += 1
        print("Iteration:", self.frameUpdateIteration)
        print("JSON Bots:", len(json["bots"]))
        print("Local Bots:", len(self.bots))

        while len(json["bots"]) > len(self.bots):
            self.isUpdated = True
            self.bots.append(self.addBot())
            print("Added a VisualBot")

        if self.isUpdated:
            for bot in self.bots:
                if bot:
                    try:
                        rawData = json["bots"][self.bots.index(bot)]
                        processedData = "Bot %s has %s %s" % (rawData["id"], rawData["coinAmount"], rawData["coinName"])
                        self.renderText(processedData, bot.x1 + 100, bot.y1 + 10)
                    except Exception as e:
                        print(e)
            self.root.update()
            self.isUpdated = False

    def submitColonyName(self):
        if self.colonyName.get():
            print("Colony:", self.colonyName.get())
        else:
            return

    def submitBotColony(self):
        if self.botColony.get():
            botCoinValue = str(self.botColony.get())
            self.coreController.createBot(botCoinValue)
            print("Tried to add bot:", botCoinValue)
        else:
            return

    def redrawBots(self):
        self.updateBotData(self.coreController.identifier)
        self.renderText(self.coreController.identifier, self.virtualCore.x1 + 15, self.virtualCore.y1 + 40)
        self.bots = list(filter(lambda iterBot: iterBot is not None, self.bots))

        self.virtualCore.draw()
        for bot in self.bots:
            bot.draw()

        self.root.after(5000, self.redrawBots)

    def run(self):
        if self.firstIteration:
            self.virtualCore.draw()
            for bot in self.bots:
                bot.draw
            self.firstIteration = False
        self.redrawBots()
        self.root.mainloop()


class VisualBot:
    def __init__(self, root, canvas, index):
        self.index = index  # Identifier with the visualiser
        self.x1 = 30
        self.y1 = (20 + (50 * self.index))
        self.color = "red"
        self.size = (20, 20)
        self.root = root
        self.canvas = canvas
        self.icon = PhotoImage(file="sprites/boticon.png")
        self.icon = self.icon.zoom(25)
        self.icon = self.icon.subsample(200)
    def draw(self):
        self.canvas.create_image(self.x1, self.y1, image=self.icon, anchor=NW)


class VisualCoreController:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x1 = 320
        self.y1 = 210
        self.x2 = 350
        self.y2 = 240

    def draw(self):
        self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill="lightblue")


def initialiseDemo():
    testCoreController = CoreController("demo")
    testCoreController.createBot("demoCoin1")
    testCoreController.createBot("demoCoin2")
    myVisualiser = VisualiserWindow(testCoreController)

    myVisualiser.run()

