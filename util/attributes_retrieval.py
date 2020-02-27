from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import requests
import datetime
import json
import os

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def get_max_page_for_letter(letter):
    url = "https://www.world-airport-codes.com/alphabetical/airport-name/{}.html?page=1".format(letter)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all('a', attrs={"class":"page-numbers"})
    max_page = 1
    for e in results:
        try:
            if max_page < int(e.string):
                max_page = int(e.string)
        except ValueError:
            pass
    return max_page

def get_geo_coord(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find('div', attrs={"data-location":True})
    if result is None:
        return None
    coord = result["data-location"]
    return coord

def get_zip_code_by_geopy(coord):
    geolocator = Nominatim(user_agent="get_zip_code")
    location = geolocator.reverse(coord)
    try:
        zip_code = location.raw['address']['postcode']
    except KeyError:
        zip_code = None
    return zip_code

def get_zip_code(coord):
    API_KEY = os.getenv('API_KEY')
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={}&key={}".format(coord, API_KEY)
    response = requests.get(url)
    response = json.loads(response.text)
    zip_code = None
    if response['status'] != 'ZERO_RESULTS':
        for d in response['results'][0]['address_components']:
            if d['types'] == ['postal_code']:
                zip_code = d['long_name']
                break
    if zip_code is None:
        zip_code = get_zip_code_by_geopy(coord)
    return zip_code

def get_attrs(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all('tr')
    results_new = []
    for re in results:
        if re.find('a', href=True) is not None:
            results_new.append(re)
    results = results_new

    values = []

    for r in results:
        url = r.find('a')["href"]
        url = "https://www.world-airport-codes.com{}".format(url)
        name = r.find('a').string

        coord = get_geo_coord(url)
        if coord is not None:
            zip_code = get_zip_code(coord)
        else:
            zip_code = None

        city = None
        country = None
        for e in r.find_all('td'):
            if e.find('span', string="City: ") is not None:
                city = list(e)[1]
            if e.find('span', string="Country: ") is not None:
                country = list(e)[1]
        values.append([name, city, country, zip_code])
        print(datetime.datetime.now(), [name, city, country, zip_code])
    return values
