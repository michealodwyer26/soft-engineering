# The demo application for a core controller.
import requests
from tkinter import *
from threading import Thread

from cryptocolony.colony_client.core_controller import CoreController
from visualiser import Visualiser


class WindowManager:

    def __init__(self):
        self.colonyNameData = None
        self.botColonyData = None
        self.coreController = CoreController("demo")
        self.vis = Visualiser(self.coreController)

    def runTkWindow(self):

        root = Tk()

        def submitColonyName():
            if colonyName.get():
                self.colonyNameData = colonyName.get()
            else:
                return

        def submitBotColony():
            if botColony.get():
                self.botColonyData = botColony.get()
                try:
                    self.coreController.createBot(self.botColonyData)
                    print("Created a core controller bot: %s" % self.botColonyData)
                except Exception as e:
                    print(e)
            else:
                return

        colonyName = Entry(root, width=20, bg="white", fg="black")
        colonyButton = Button(root, text="Submit", command=submitColonyName)
        botColony = Entry(root, width=20, bg="white", fg="black")
        botButton = Button(root, text="Submit", command=submitBotColony)

        botColony.pack()
        botButton.pack()
        colonyName.pack()
        colonyButton.pack()
        root.mainloop()

    def runPygameWindow(self):

        response = requests.get("http://65.108.214.180/api/v1/colony/demo")
        json = response.json()
        print(json)

        for i in json['bots']:
            self.vis.addBot()

        self.vis.run()

    def runWindows(self):

        # Threads
        Thread(target=self.runTkWindow).start()
        Thread(target=self.runPygameWindow).start()


mainWindows = WindowManager()
mainWindows.runWindows()
