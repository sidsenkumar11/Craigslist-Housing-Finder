from craigslist import CraigslistHousing
from collections import namedtuple
import db_handler
from config import *
import time

# Define geotag tuples
Point = namedtuple('Point', ['lat', 'long'])
Box = namedtuple('Box', ['upper_left', 'bottom_right'])

# Define bounding boxes for acceptable house locations
upper_left = Point(lat=34.429806, long=-119.885178)
bottom_right = Point(lat=34.407634, long=-119.843107)
main_box = Box(upper_left, bottom_right)
BOXES = {
    main_box: 'IV + Goleta'
}

def in_box(coords, box):
    return box.bottom_right.lat < coords.lat < box.upper_left.lat and box.upper_left.long < coords.long < box.bottom_right.long

def search(site):
    results = site.get_results(sort_by='newest', geotagged=True, limit=20)
    for result in results:
        geotag = Point(result["geotag"][0], result["geotag"][1])
        area = ""
        for coords, a in BOXES.items():
            if in_box(geotag, coords):
                area = a

                # Insert result into DB
                db_handler.insert(result)

def main():
    # Create 3 searches for housing
    apartments = CraigslistHousing(site='santabarbara', category='apa', filters={'max_price': 1200, 'min_price': 700})
    rooms      = CraigslistHousing(site='santabarbara', category='roo', filters={'max_price': 1200, 'min_price': 700})
    sublets    = CraigslistHousing(site='santabarbara', category='sub', filters={'max_price': 1200, 'min_price': 700})
    sites      = [apartments, rooms, sublets]

    while True:
        for site in sites:
            search(site)
        time.sleep(10)

if __name__ == '__main__':
    main()
