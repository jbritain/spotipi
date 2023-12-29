import serial
import time
from spotify import Spotify
import asyncio

# equivalent to setTimeout in JS
# takes in a callback and a delay in seconds, and calls the callback once that time has passed
def async_call_later(seconds, callback):
    async def schedule():
        await asyncio.sleep(seconds)

        if asyncio.iscoroutinefunction(callback):
            await callback()
        else:
            callback()

    asyncio.ensure_future(schedule())

# every hour we must get a new token
async def token_update_timer():
    spotify.token = spotify.get_token()
    async_call_later(3600, token_update_timer)

# arduino stuff
port = 'COM8'
baudrate = 115200
arduino = serial.Serial(port=port,  baudrate=baudrate, timeout=.1)

def write(x):
    arduino.write(bytes(x,  'utf-8'))

def read():
    return arduino.readline()

# spotify stuff
CLIENT_ID = "4e01751363414764a80826923907e8ac"
CLIENT_SECRET = "96c70855a11e4431beeb9f9bce744e11"
INITIAL_TOKEN = "BQAFMPbgUFP-EtsLx1nFnPTpjzCA5BhKC2quHSwAsHBCV4fLbW6iRHIWSTyDx4KgivyScuHGN1UqlkddQtdklhyljDP6mws5_DgG2RwGCvi4nXMLwskBNnVrgYkM6u4Iq5y05Wdk1A6aSzdimerOt9FJFC_nBNweMy-aCG40YQTyRLZwj3by_4M0OvBknPQZs6Bi4nKOuXXK"

spotify = Spotify(INITIAL_TOKEN, CLIENT_ID, CLIENT_SECRET)

print(spotify.get_playback_info())
last_vol = 0
vol = 0

while(True):
    
    # get current volume
    data = read().decode()
    if data != '':
        vol = int(data.split("-")[-1])
    if vol != last_vol:
        print(vol)
        spotify.set_volume(vol)
        last_vol = vol

    write(spotify.get_playback_info().to_display(int(time.time())))

