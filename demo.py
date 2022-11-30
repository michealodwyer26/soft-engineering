# The demo application for a core controller.
import requests
from tkinter import *
from threading import Thread

from colony_client.core_controller import CoreController
from colony_client.visualiser import Visualiser

def runTkWindow():
    root = Tk()

    def submitColonyName():
        # myLabel = Label(root, text=colonyName.get())
        # myLabel.pack()
        if colonyName.get():
            print(colonyName.get())
        else:
            return

    def submitBotColony():
        # myLabel = Label(root, text=botColony.get())
        # myLabel.pack()
        if botColony.get():
            print(botColony.get())
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



