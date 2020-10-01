# spotifylyrics

Displays the lyrics from genius.com of the song currently playing on user's Spotify. 

Before I started I know that are a lot better existing programs and software but I wanted to make something on my own. This is my first big project. It took me around a month. I tried to automate and not hardcode this as much as I could. I stopped so many times and had to rethink and google things but I also learned so much from doing this.

External modules required to be installed:
  requests, bs4, lxml, tkinter
  
To use: 

1- Set up spotify api from developers.spotify.com

2- Create an app.

3- Add redirect uri to your app from app settings.

4- Copy client ID, client secret and redirect uri to creds.py

5- After running the script for the first time, copy your refresh_token to creds.py

6- (Optional) create a desktop shortcut and in the properties modify the target so it becomes: PATH TO PYTHON.EXE "PATH TO RUN.PY"


Limitations:

1- Tkinter is so clunky sometimes it just doesn't load properly for no reason.

2- Only track names with english alphabet are supported.

3- Sometimes when there are two artists for one track spotify only gives one which results in problems in getting the genius lyrics page.
