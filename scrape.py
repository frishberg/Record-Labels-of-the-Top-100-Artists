import requests
from bs4 import BeautifulSoup
import json
import time


data = {}
data["aron"] = ["jew"]

with open("labels.json", "w") as outfile :
    json.dump(data, outfile)