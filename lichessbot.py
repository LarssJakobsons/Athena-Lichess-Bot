version = '1.0.0'


import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

auth_token = os.environ['AUTH_TOKEN_PERSONAL']
print(auth_token)
auth = {'Authorization': f'Bearer {auth_token}'}

get_acc = 'https://lichess.org/api/account'
acc_info = requests.get(get_acc, headers=auth)

get_team = 'https://lichess.org/api/team/athena_bot-dev-playground'
team_info = requests.get(get_team, headers=auth)

print(json.dumps(team_info.json(), indent=4))

create_swiss = 'https://lichess.org/api/swiss/new/athena_bot-dev-playground'
tournament_data ={
    "name": "Athena Bot Swiss",
    "rated": "false",
    "clock.limit": "120",
    "clock.increment": "5",
    "nbRounds": "3",
    "variant": "standard",
}
swiss_info = requests.post(create_swiss, headers=auth, data=tournament_data)

print(json.dumps(swiss_info.json(), indent=4))