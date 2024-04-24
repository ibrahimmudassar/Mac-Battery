import os
import pygsheets
import requests
import re
from datetime import datetime
from discord_webhook import DiscordEmbed, DiscordWebhook  # Connect to discord
from environs import Env  # For environment variables
import math


# Setting up environment variables
env = Env()
env.read_env()  # read .env file, if it exists


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great circle distance between two points on the earth (specified in decimal degrees).
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in meters
    return c * r


r = requests.get("http://ip-api.com/json/").json()

gc = pygsheets.authorize(
    service_file="/Users/ibrahimmudassar/downloads/macbattery/client_secret.json")
raw_battery_data = os.popen("pmset -g batt").read()
formatted_battery_data = re.search(
    r"\s(\d+)\%\;.(.+)\;.(.+).present", raw_battery_data)

# Open GoogleSheet
sh = gc.open_by_key(env('SHEET_KEY'))
wks = sh.sheet1

# retrieve all rows of the worksheet
cells = wks.get_all_values(
    include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')

# extract all non empty rows
nonEmptyRows = []
for i in cells:
    if i != []:
        nonEmptyRows.append(i)
percentage, battery_status, battery_estimate = formatted_battery_data.groups()
row = [percentage, battery_status, battery_estimate, r['lat'], r['lon'],
       datetime.now().isoformat()]

# here wks is the worksheet object
wks.insert_rows(len(nonEmptyRows), values=row, inherit=True)

distance_from_house = calculate_distance(
    float(env("LAT")), float(env("LON")), r['lat'], r['lon'])

if distance_from_house <= 1 and int(percentage) < 60 and battery_status == 'discharging':
    embed = DiscordEmbed(title='Mac Battery Low')

    embed.add_embed_field(
        name="Data", value=f"Percentage:\t{percentage}", inline=False)

    # set footer
    embed.set_footer(text='Made By Ibrahim Mudassar',
                     icon_url='https://avatars.githubusercontent.com/u/22484328?v=4')

    # add embed object to webhook(s)
    # Webhooks to send to
    for webhook_url in env.list("WEBHOOKS"):
        webhook = DiscordWebhook(url=webhook_url)

        webhook.add_embed(embed)
        webhook.execute()
