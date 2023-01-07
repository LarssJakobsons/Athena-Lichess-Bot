# bot created using the berserk-downstream library

bot_version = "0.1.0"

# import all the necessary libraries
import berserk as lichess
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from random import choice
import schedule

# load the token from the .env file
load_dotenv()
token = os.environ["LICHESS_API"]
team_password = os.environ["TEAM_PASSWORD"]


def join(teams, team_id, message=None, password=None):
    """Join a team.
    Temporary fix provided by Sol
    """
    path = f"/team/{team_id}/join"
    payload = {
        "message": message,
        "password": password,
    }
    return teams._r.post(path, json=payload)["ok"]


# connect to lichess and start a bot session
session = lichess.TokenSession(token)
client = lichess.Client(session=session)
print(f'{client.account.get()["username"]} has connected to lichess')

# join a team if needed
# join(client.teams, "athena_bot-dev-playground", message=None, password=team_password)

# create a swiss tournament in the team
def create_tournament():
    tournament = client.teams.create_swiss(
        teamId="athena_bot-dev-playground",  # team id
        name="Test tournament",  # tournament name
        clock={"increment": 0, "limit": 7},  # clock settings
        nb_rounds=10,  # maximum number of rounds
        startsAt=datetime.utcnow() + timedelta(days=5),  # tournament date
        roundInterval=10,  # time between rounds
        password=None,  # tournament password
        variant="standard",  # variant name
        rated=True,  # affects ratings
        conditions={"maxRating": 3000, "minRating": 0, "nbRatedGames": 0},  # conditions for joining
    )
    # send a message to Larss_J on lichess that contains the tournament link
    client.messaging.send("Larss_J", f"https://lichess.org/swiss/{tournament['id']}")


# create a tournament every saturday at 11:00 UTC using task scheduler
schedule.every().saturday.at("11:00").do(create_tournament, "test")

# run the task scheduler
while True:
    schedule.run_pending()
