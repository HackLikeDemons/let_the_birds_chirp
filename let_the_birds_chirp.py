# Author: HackLikeDemons - twitter.com/andreaswienes
# TODO: programmatically get Bearer token
# https://stackoverflow.com/questions/72482384/how-to-read-emails-from-gmail

import requests
import urllib3
from datetime import datetime
from geopy.geocoders import Nominatim
import time

urllib3.disable_warnings()

# get latitude and longitude 
loc = Nominatim(user_agent="GetLoc")
getLoc = loc.geocode("Hamburg Jungfernstieg")
latitude = str(getLoc.latitude)
longitude = str(getLoc.longitude)

TIMESTAMP = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%Z")
LOCATION = '{"timestamp":"' + TIMESTAMP + '","longitude":' + longitude + ',"latitude":'+ latitude + '}'
BIRD_AUTH_TOKEN = 'Bearer REDACTED'
BIRD_USER_AGENT ='User-Agent: Bird/4.206.1 (co.bird.Ride; build:1; iOS 15.6.1) Alamofire/5.2.2'

### !!! Be careful with these parameters !!! ###
ALARM = False
RADIUS = "1000"
WAIT_SECONDS = 2
ROUNDS = 3

def chirp(bird_id):    
    BIRD_CHIRP_URL = "https://api-bird.prod.birdapp.com/bird/chirp"
    http_headers = {
        'Location': LOCATION,
        'Authorization': BIRD_AUTH_TOKEN,
        'User-Agent': BIRD_USER_AGENT,
        'Content-Type': 'application/json'
    }    
    r = requests.put(BIRD_CHIRP_URL, headers=http_headers, 
    json={"bird_id":bird_id,"alarm":ALARM})
    # print(bird_id, r.status_code)
    

# get birds nearby
BIRD_LIST_URL = "https://api-bird.prod.birdapp.com/bird/nearby?latitude=" + latitude + "&longitude=" + longitude + " &radius=" + RADIUS

http_headers = {
    'Location': LOCATION,
    'Authorization': BIRD_AUTH_TOKEN,
    'User-Agent': BIRD_USER_AGENT
}

round = 1
while round <= ROUNDS:
    print(f'round {round} of {ROUNDS}')
    r = requests.get(BIRD_LIST_URL, headers=http_headers, verify=False)
    data = r.json()

    bird_list = data['birds']
    print(f'Found {len(bird_list)} birds nearby')
    print('... chirp chirp ...')
    
    # let the birds chirp
    for bird in bird_list[:3]:
        chirp(bird['id'])
        
    if round == ROUNDS:
        print("Hope you had some fun")        
        exit()
    else:
        round += 1
        print(f"Waiting for {WAIT_SECONDS} seconds")
        time.sleep(WAIT_SECONDS)