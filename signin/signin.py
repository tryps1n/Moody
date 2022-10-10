from pathlib import Path
from threading import Thread
from tkinter import Canvas, Entry, Text, Button, PhotoImage, Tk
import pickle
from googleapiclient.discovery import build
import os
from google_auth_oauthlib.flow import InstalledAppFlow


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("800x600")
window.configure(bg = "#FFFFFF")
window.title('Sign In')
window.iconbitmap('assets/icon.ico')

def fetchTokens():
    flow = InstalledAppFlow.from_client_secrets_file(
            'assets/client_secrets.json',
            scopes=[
                'https://www.googleapis.com/auth/youtube',
            ]
        )
    flow.run_local_server(port=8080, prompt='consent',
                            authorization_prompt_message='')
    credentials = flow.credentials

    with open('assets/token.pickle', 'wb') as f:
        print('Saving Credentials for Future Use...')
        pickle.dump(credentials, f)
    
    window.destroy()

def signin():
    t1 = Thread(target=fetchTokens, args=())
    t1.start()

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 600,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    400.0,
    300.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=signin,
    relief="flat"
)
button_1.place(
    x=261.0,
    y=439.0,
    width=277.0,
    height=58.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    398.0,
    123.0,
    image=image_image_2
)
window.resizable(False, False)
window.mainloop()

os.system('python guimain/guimain.py')
