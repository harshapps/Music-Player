import os
from tkinter.filedialog import askdirectory

import pygame
from mutagen.id3 import ID3
from tkinter import *


root = Tk()
root.minsize(350, 350)
playflag = False

listofsongs = []
realnames = []

v = StringVar()
songlabel = Label(root, textvariable=v, width=35)


def directorychooser():

    directory = askdirectory()
    os.chdir(directory)

    for files in os.listdir(directory):
        if files.endswith(".mp3"):

            realdir = os.path.realpath(files)
            audio = ID3(realdir)
            realnames.append(audio['TIT2'].text[0])

            listofsongs.append(files)

    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    # pygame.mixer.music.play()


index = 1
directorychooser()
pygame.mixer.music.load(listofsongs[index])
pygame.mixer.music.play()


def updatelabel():
    global index
    global songname
    v.set(realnames[index])
    # return songname


def nextsong(event):
    global index
    index += 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()


def prevsong(event):
    global index
    index -= 1
    # print(index)
    print(len(listofsongs))
    if abs(index) <= len(listofsongs[index]):
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        updatelabel()


def stopsong(event):
    pygame.mixer.music.stop()
    v.set("")
    # return songname


def playpausesong(event):
    global playflag
    if playflag:
        pygame.mixer.music.unpause()
        playflag = False
    else:
        pygame.mixer.music.pause()
        playflag = True
    v.set("")
    # return songname


def resumesong(event):
    pygame.mixer.music.unpause()
    v.set("")


def playsong(event):
    global index
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    v.set("")
    # return songname


label = Label(root, text='Music Player')
label.pack()

listbox = Listbox(root)
listbox.pack()

# listofsongs.reverse()
realnames.reverse()

for items in realnames:
    listbox.insert(0, items)

realnames.reverse()
# listofsongs.reverse()


nextbutton = Button(root, text='Next Song')
nextbutton.pack()

previousbutton = Button(root, text='Previous Song')
previousbutton.pack()

stopbutton = Button(root, text='Stop Music')
stopbutton.pack()

playpausesong_btn = Button(root, text='Play/Pause Music')
playpausesong_btn.pack()

# playsong_btn = Button(root, text='Play Music')
# playsong_btn.pack()

nextbutton.bind("<Button-1>", nextsong)
previousbutton.bind("<Button-1>", prevsong)
stopbutton.bind("<Button-1>", stopsong)
playpausesong_btn.bind("<Button-1>", playpausesong)
# playsong_btn.bind("<Button-1>", playsong)

songlabel.pack()

root.mainloop()
