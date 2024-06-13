import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures

# to get factorylinks if they change, goto: https://r.jakumo.org/factories_profit.php
# and run this in the console: JSON.stringify(Array.from(document.querySelectorAll('body > div > div > div > table > tbody > tr > td:nth-child(1) > span > a')).map(a => ({ access: false, name: a.innerText, link: a.href })))
factoryLinks = [
    {"access": True, "name": "Brick factory", "link": "https://r.jakumo.org/factory_details.php?id=25"},
    {"access": True, "name": "Concrete factory", "link": "https://r.jakumo.org/factory_details.php?id=6"},
    {"access": True, "name": "Fertilizer factory", "link": "https://r.jakumo.org/factory_details.php?id=23"},
    {"access": True, "name": "Ironworks", "link": "https://r.jakumo.org/factory_details.php?id=31"},
    {"access": True, "name": "Oil refinery", "link": "https://r.jakumo.org/factory_details.php?id=39"},
    {"access": True, "name": "Glazier's shop", "link": "https://r.jakumo.org/factory_details.php?id=61"},
    {"access": True, "name": "Copper refinery", "link": "https://r.jakumo.org/factory_details.php?id=37"},
    {"access": True, "name": "Insecticide factory", "link": "https://r.jakumo.org/factory_details.php?id=29"},
    {"access": True, "name": "Aluminium factory", "link": "https://r.jakumo.org/factory_details.php?id=33"},
    {"access": True, "name": "Plastic factory", "link": "https://r.jakumo.org/factory_details.php?id=63"},
    {"access": True, "name": "Lithium refinery", "link": "https://r.jakumo.org/factory_details.php?id=91"},
    {"access": True, "name": "Battery factory", "link": "https://r.jakumo.org/factory_details.php?id=95"},
    {"access": True, "name": "Arms factory", "link": "https://r.jakumo.org/factory_details.php?id=101"},
    {"access": True, "name": "Silicon refinery", "link": "https://r.jakumo.org/factory_details.php?id=68"},
    {"access": False, "name": "Electronics factory", "link": "https://r.jakumo.org/factory_details.php?id=69"},
    {"access": False, "name": "Titanium refinery", "link": "https://r.jakumo.org/factory_details.php?id=52"},
    {"access": False, "name": "Medical technology Inc.", "link": "https://r.jakumo.org/factory_details.php?id=76"},
    {"access": False, "name": "Silver refinery", "link": "https://r.jakumo.org/factory_details.php?id=34"},
    {"access": False, "name": "Gold refinery", "link": "https://r.jakumo.org/factory_details.php?id=80"},
    {"access": False, "name": "Goldsmith", "link": "https://r.jakumo.org/factory_details.php?id=85"},
    {"access": False, "name": "Drone shipyard", "link": "https://r.jakumo.org/factory_details.php?id=118"},
    {"access": False, "name": "Truck plant", "link": "https://r.jakumo.org/factory_details.php?id=125"},
]

currentFactoryLevels = [
    {"name": "Brick factory",           "lvl": 23},
    {"name": "Concrete factory",        "lvl": 15},
    {"name": "Fertilizer factory",      "lvl": 2},
    {"name": "Ironworks",               "lvl": 3},
    {"name": "Oil refinery",            "lvl": 3},
    {"name": "Glazier's shop",          "lvl": 3},
    {"name": "Copper refinery",         "lvl": 3},
    {"name": "Insecticide factory",     "lvl": 1},
    {"name": "Aluminium factory",       "lvl": 3},
    {"name": "Plastic factory",         "lvl": 2},
    {"name": "Lithium refinery",        "lvl": 1},
    {"name": "Battery factory",         "lvl": 1},
    {"name": "Arms factory",            "lvl": 1},
    {"name": "Silicon refinery",        "lvl": 0},
    {"name": "Electronics factory",     "lvl": 0},
    {"name": "Titanium refinery",       "lvl": 0},
    {"name": "Medical technology Inc.", "lvl": 0},
    {"name": "Silver refinery",         "lvl": 0},
    {"name": "Gold refinery",           "lvl": 0},
    {"name": "Goldsmith",               "lvl": 0},
    {"name": "Drone shipyard",          "lvl": 0},
    {"name": "Truck plant",             "lvl": 0},
]

def format_number(num):
    num = float(num)
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.1f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

def getEarnBackTime(factory):
    factoryLevel = list(filter(lambda f: f['name'] == factory['name'], currentFactoryLevels))[0]['lvl']

    link = f'{factory["link"]}&s={factoryLevel}&e={factoryLevel + 1}'

    # Send a GET request to the URL
    response = requests.get(link)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'lxml')

    earnbackTimeElement = soup.select_one('script[type="text/javascript"]')

    pattern = r'Return time: \d+\.?\d* days'
    match = re.search(pattern, earnbackTimeElement.text)
    if (not match):
        return {
        'name': factory['name'],
        'days': 'not found',
        'toLvl': factoryLevel + 1
    }
    extracted_string = match.group()
    days = re.sub('[a-zA-Z :]+', '', extracted_string)

    # get the total upgrade price
    upgrade_price_element = soup.select_one('td:has(> small#profit)')
    upgrade_price = int(re.sub('\xa0', '', upgrade_price_element.text)) # \xa0 is &nbsp

    return {
        'name': factory['name'],
        'days': days,
        'toLvl': factoryLevel + 1,
        'price': format_number(upgrade_price)
    }

def pretty_print_dicts(dicts):
    # Get all keys
    keys = list(dicts[0].keys())

    # Determine the maximum length of each field
    max_lengths = {key: max(len(str(d[key])) for d in dicts) for key in keys}

    # Update max_lengths if any key is longer than the max length of the data in its field
    for key in keys:
        if len(key) > max_lengths[key]:
            max_lengths[key] = len(key)

    # Print headers
    print(' '.join(f"{key:<{max_lengths[key]}}" for key in keys))

    # Print each dictionary line by line
    for d in dicts:
        print(' '.join(f"{str(d[key]):<{max_lengths[key]}}" for key in keys))

if __name__ == '__main__':
    # List of accessible factories
    accessible_factory_links = filter(lambda f: f['access'], factoryLinks)
    input = accessible_factory_links

    # List to hold the results
    earn_back_times = []

    # Use ThreadPoolExecutor to parallelize the function calls
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the function to the factories and execute in parallel
        results = executor.map(getEarnBackTime, input)
        earn_back_times = list(results)

    sorted_earn_back_times = sorted(earn_back_times, key=lambda t: float(t['days']), reverse=False)

    pretty_print_dicts(sorted_earn_back_times)