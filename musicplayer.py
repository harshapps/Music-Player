import os
from tkinter.filedialog import askdirectory

import pygame
from mutagen.id3 import ID3
from tkinter import *
import time
import socket
# from thread import *
from threading import Thread


def accept_conn():
    while True:
        global client_socket, client_address
        client_socket, client_address = server_socket.accept()  # Socket accepts any connection request
        thread2 = Thread(target=receivedData)
        thread2.start()
        thread2.join()
        # start_new_thread(clientthread,(client_socket,client_address),)     #Forking a new thread for the newly connected client


def receivedData():
    global client_socket, client_address
    print("In Receive")
    while True:
        msg = client_socket.recv(1024).decode("utf-8")
        print(msg)
        if str(msg).endswith("change") == True:
            playpausesong()
        if str(msg).endswith("next") == True:
            nextsong()
        if str(msg).endswith("previous") == True:
            prevsong()


client_socket = ""
client_address = ""
root = Tk()
root.minsize(350, 350)
playflag = False
volume = ''

listofsongs = []
realnames = []

v = StringVar()
songlabel = Label(root, textvariable=v, width=35)

no_of_musicfiles = 0

def directorychooser():
    directory = askdirectory()
    os.chdir(directory)

    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            audio = ID3(realdir)
            realnames.append(audio['TIT2'].text[0])

            listofsongs.append(files)

    no_of_musicfiles = len(listofsongs)
    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    # pygame.mixer.music.play()


index = 0
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
    global no_of_musicfiles

    index += 1
    try:
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        updatelabel()
    except:
        print("No next song available")

def prevsong(event):
    global index
    global no_of_musicfiles
    index -= 1

    # if abs(index) <= no_of_musicfiles:
    try:
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        updatelabel()
    except:
        print("No previous song available")


def stopsong(event):
    pygame.mixer.music.stop()
    v.set("")
    # return songname


def playpausesong():
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
    # time.sleep(10)
    # pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
    v.set("")
    # return songname


def decreasevolume(event):
    global volume
    pygame.mixer.music.pause()
    volume = pygame.mixer.music.get_volume()
    print('volume current', volume)
    pygame.mixer.music.set_volume(volume - 0.1)
    pygame.mixer.music.unpause()
    print('volume is', volume)
    v.set("")


def increasevolume(event):
    global volume
    print('volume current', volume)
    pygame.mixer.music.pause()
    volume = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(volume + 0.1)
    pygame.mixer.music.unpause()
    print('volume is', volume)
    v.set("")

    # for volume_index in range(9):
    #     print('volume is ', volume)
    #     pygame.mixer.music.load(listofsongs[index])
    #     time.sleep(10)
    #     pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
    #     volume = pygame.mixer.music.get_volume()
    #     pygame.mixer.music.play()
    #     volume_index = volume_index+1
    # v.set("")


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

# playpausesong_btn = Button(root, text='Play/Pause Music')
# playpausesong_btn.pack()

decreasevolume_btn = Button(root, text='Decrease Volume')
decreasevolume_btn.pack()

increasevolume_btn = Button(root, text='Increase Volume')
increasevolume_btn.pack()

nextbutton.bind("<Button-1>", nextsong)
previousbutton.bind("<Button-1>", prevsong)
stopbutton.bind("<Button-1>", stopsong)
decreasevolume_btn.bind("<Button-1>", decreasevolume)
increasevolume_btn.bind("<Button-1>", increasevolume)
# decreasevolume_btn.bind("<Button-1>", decreasevolume)

# playpausesong_btn.bind("<Button-1>", playpausesong)

songlabel.pack()

server_address = ('0.0.0.0', 1234)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(500)
thread = Thread(target=accept_conn)
thread.start()

root.mainloop()