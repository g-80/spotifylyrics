import spotify_client
import threading
import requests
import lxml
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import ttk

### Connect to Spotify API

sp = spotify_client.SpotifyClient()

if sp.refresh_token == " ":
    sp.get_authentication_code()
    sp.get_access_token()


def auto_refresh_access_token():
    threading.Timer(3500, auto_refresh_access_token).start()
    sp.refresh_access_token()
    print ("Access token was refreshed")

auto_refresh_access_token()


### Get the artist and track name

def get_currently_playing_data():
    data = sp.get_currently_playing()
    if data == None:
        print ("No music is currently playing")
    return data
     
current_playing_data = get_currently_playing_data()
print (current_playing_data)


### Scrape Genius' lyrics page

def get_lyrics(data):
    genius_artist = data["artist"]
    genius_track = data["track"]

    # String processing for genius 
    if "(" in genius_track:
        indx = genius_track.find("(")
        genius_track = genius_track[:indx-1]
    if "-" in genius_track:
        indx = genius_track.find("-")
        genius_track = genius_track[:indx-1]
    print (genius_artist,genius_track)    
    genius_artist = genius_artist.replace(" ", "-").replace("/", "-").replace("'", "").replace("&", "and")
    genius_track = genius_track.replace(" ","-").replace("/", "-").replace("'", "").replace(",","").replace("&", "and")

    res = requests.get(f"https://genius.com/{genius_artist}-{genius_track}-lyrics")
    if res.status_code not in range(200,299):
            raise Exception("Could not get lyrics")
            pass
    soup = BeautifulSoup(res.text,"lxml")
    page_text = soup.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
    text_with_spaces = ""
    for part in page_text:
        text_with_spaces = text_with_spaces + part.prettify()

    def remove_html_tags(text):

        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    
    lyrics = remove_html_tags(text_with_spaces)
    return lyrics


lyrics = get_lyrics(current_playing_data)


### Display lyrics with tkinter

def display_lyrics(lyrics):

    root = tk.Tk()
    root.title("Lyrics")
    root.geometry("500x300")

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=1)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side="left", fill="both", expand= 1)

    scrollbar = ttk.Scrollbar(main_frame, orient= "vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    second_frame = tk.Frame(canvas)

    canvas.create_window((0,0), window=second_frame, anchor="nw")

    def refresh_lyrics():
        refreshed_data = get_currently_playing_data()
        new_lyrics = get_lyrics(refreshed_data)
        str_var.set(new_lyrics)
    
    button = tk.Button(second_frame, text="Refresh lyrics", command=refresh_lyrics).pack()
    
    str_var = tk.StringVar()
    str_var.set(lyrics)

    label = tk.Label(second_frame, textvariable=str_var).pack(padx=60)
            
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/70)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    root.mainloop()
 
display_lyrics(lyrics)
