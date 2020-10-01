import requests
import base64
import datetime
import creds
import webbrowser

class SpotifyClient():
    
    def __init__(self):
        self.client_id = creds.client_id
        self.client_secret = creds.client_secret
        self.redirect_uri = creds.redirect_uri
        self.auth_code = None
        self.token_url = "https://accounts.spotify.com/api/token"
        self.refresh_token = creds.refresh_token

    def get_authentication_code(self):
        auth_url = (f"https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code"
        f"&redirect_uri={self.redirect_uri}&scope=user-read-currently-playing")
        webbrowser.open(auth_url)
        self.auth_code= input("Log in to your account and enter the authorization code from the redirect uri \n")
        if len(self.auth_code) == 211:
            self.is_authenticated = True
            print ("Successfully authenticated")

    def get_client_credentials(self):
        if self.client_id== " " or self.client_secret == " ":
            raise Exception("You must set your client ID and client secret in the creds.py file")
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_access_token(self):
        client_creds = self.get_client_credentials()
        res = requests.post(self.token_url,
            data={"grant_type": "authorization_code", "code": self.auth_code, "redirect_uri": self.redirect_uri},
            headers={"Authorization": f"Basic {client_creds}"})
        if res.status_code not in range(200,299):
            raise Exception("Could not authenticate client")
        data = res.json()
        access_token = data['access_token']
        refresh_token = data["refresh_token"]
        self.access_token = access_token
        self.refresh_token = refresh_token
        print (f"This is your refresh token. Save it to creds.py \n{refresh_token}")
        
    def refresh_access_token(self):
        client_creds = self.get_client_credentials()
        res= requests.post(self.token_url,
            data={"grant_type": "refresh_token", "refresh_token": self.refresh_token}, 
            headers={"Authorization": f"Basic {client_creds}"})
        data = res.json()
        access_token = data['access_token']
        self.access_token = access_token
                                        
    def get_currently_playing(self):
        r = requests.get("https://api.spotify.com/v1/me/player/currently-playing",
        headers={"Authorization": f"Bearer {self.access_token}"})
        data = r.json()
        artist_name = data["item"]["artists"][0]["name"]
        track_name = data["item"]["name"]
        return {"artist":artist_name, "track":track_name}         




