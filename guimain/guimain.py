from pathlib import Path
import os
from telnetlib import SE
from threading import Thread
import pickle
from googleapiclient.discovery import build
from pathlib import Path
from tkinter import CENTER, DISABLED, E, N, SW, Canvas, Tk, Entry, Text, Button, PhotoImage, END, Label, messagebox
import webbrowser
import time

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()


window.geometry("1280x720")
window.configure(bg = "#FFFFFF")
window.iconbitmap('assets/icon.ico')
window.title('Moody - Song Recommender')

if os.path.exists('assets/token.pickle'):
    print('Loading Credentials From File...')
    with open('assets/token.pickle', 'rb') as token:
        creds = pickle.load(token)

youtube = build('youtube', 'v3', credentials=creds)
request = youtube.channels().list(
        part = 'snippet',
        mine = True,

    )

response = request.execute()
username = response['items'][0]['snippet']['title']

present = False
playurl = ''

def clock():
    string = time.strftime('%A \n %d-%m-%y \n %I:%M:%S %p')
    lbl.config(text = string)
    lbl.after(1000, clock)

def mooddetfunc(mood, entry_1):
    entry_1.delete('0', END)
    entry_1.insert(END, 'Detecting mood, please wait...')
    os.system('python mooddetmain/mooddetmain.py')
    f = open('assets/mood.txt', 'r')
    mood = f.read()
    f.close()
    
    entry_1.delete('0', END)
    if ' ' not in mood and len(mood) > 1: 
        
        entry_1.insert(END, "Detected Mood: " + mood + ". Click 'Detect Mood' again if the detection was wrong.")
        messagebox.showinfo(f"Mood Detected: {mood.upper()}", "Detected Mood: " + mood.upper() + ". \nClick 'Detect Mood' again if the detection was wrong.")
        button_2.place(
            x=470.0,
            y=557.0,
            width=340.0,
            height=61.0
        )

    elif mood == 'x':
        entry_1.insert(END, "Camera was crossed out. Please try again.")
    else: 
        entry_1.insert(END, "No face was detected. Please try again.")
        messagebox.showerror('error', 'no face was detected, please try again.')
    f.close()

def ytPlaylist(text, entry_1):
    entry_1.delete('0', END)
    text = 'generating playlist, please wait...'
    entry_1.insert(END, text)
    f = open('assets/mood.txt', 'r')
    url = f.read()
    f.close()
    print(url)
    if url == '': 
        entry_1.delete('0', END)
        text = 'You need to detect your mood first.'
        entry_1.insert(END, text)
        messagebox.showerror('Error', 'You need to detect your mood first.')
    elif url == 'err':
        entry_1.delete('0', END)
        entry_1.insert(END, 'internal error occured. pls try again.')
    else:
        os.system('python playlist-generation/playlist-generation.py')
        time.sleep(0.6)
        f = open('assets/mood.txt')
        url0 = f.read()
        print("This thing " + url0)
        print('url is ' + url0)
        f.close()
        f = open('assets/mood.txt', 'w')
        if url0 == 'err':
            entry_1.delete('0', END)
            entry_1.insert(END, 'internal error occured. pls try again.')
            messagebox.showerror('Error', 'Internal Error Occurred.')
            
        elif url0 == 'quota':
            entry_1.delete('0', END)
            entry_1.insert(END, 'ran out of required quota.')
            messagebox.showerror('Error', 'ran out of required quota.')
        else: 
            entry_1.delete('0', END)
            entry_1.insert(END, f'playlist generated. url -> {url0}')
            webbrowser.open(f'{url0}')
            playurl = url0
        f.close()
        button_3.place(
            x=18.0,
            y=618.0,
            width=254.0,
            height=45.0
        )
        
def CreatePlayButton():
    t1 = Thread(target=ytPlaylist, args=(mood, entry_1))
    t1.start()

def moodFunc():
    t1 = Thread(target=mooddetfunc, args=(mood, entry_1))
    t1.start()

def signout():
    with open('assets/token.pickle', 'wb') as f:
        pickle.dump('signedout', f)
    window.destroy()
    os.system('python signin/signin.py')

def delPlaylist():
    response = youtube.playlistItems().list(
         part = 'contentDetails', 
         playlistId = playurl.replace('https://www.youtube.com/playlist?list=', ''), 
         maxResults = 10,    
    ).execute()
    playlistitems = response['items']
    for item in playlistitems: 
        print('deleting item')
        youtube.playlistItems().delete(id=item['id']).execute()
    print('process complete.')
mood = 'Click the "Detect Mood" Button to get started.'

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    643.0,
    340.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    643.0,
    700.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    highlightthickness=0
)
entry_1.place(
    x=0.0,
    y=680.0,
    width=1286.0,
    height=38.0
)

canvas.create_text(
    554.0,
    283.0,
    anchor="nw",
    text=username,
    justify=CENTER,
    fill="#FFFFFF",
    font=("Inter ExtraLight", 45 * -1)
)

canvas.create_text(
    1079.0,
    514.0,
    anchor="nw",
    text="Logged in as:",
    fill="#FFFFFF",
    font=("RobotoRoman Light", 23 * -1)
)

canvas.create_text(
    1079.0,
    545.0,
    anchor="nw",
    text=username,
    fill="#FFFFFF",
    font=("RobotoRoman Light", 21 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=moodFunc,
    relief="flat"
)
button_1.place(
    x=470.0,
    y=472.0,
    width=339.9999694824219,
    height=63.26776123046875
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=CreatePlayButton,
    relief="flat"
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=delPlaylist,
    relief="flat"
)

canvas.create_text(
    1079.0,
    587.0,
    anchor="nw",
    text="Not you?",
    fill="#FFFFFF",
    font=("RobotoRoman Light", 23 * -1)
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=signout,
    relief="flat"
)
button_4.place(
    x=1079.0,
    y=616.0,
    width=183.0,
    height=36.350067138671875
)

lbl = Label(window, font = ('RobotoRoman Light', 29),
            background = '#2b5b71',
            foreground = 'white'
)
entry_1.insert(END, mood)
lbl.pack(anchor=E)
clock()

# window.wm_attributes('-transparentcolor', '#2b5b71')

window.resizable(False, False)
window.mainloop()

f = open('assets/mood.txt','w')
f.write('')