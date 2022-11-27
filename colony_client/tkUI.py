from tkinter import *

root = Tk()

"""Functions to call on click of the button"""


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
colonyName.pack()

myButton = Button(root, text="Submit", command=submitColonyName)
myButton.pack()

botColony = Entry(root, width=20, bg="white", fg="black")
botColony.pack()

myButton = Button(root, text="Submit", command=submitBotColony)
myButton.pack()


root.mainloop()
