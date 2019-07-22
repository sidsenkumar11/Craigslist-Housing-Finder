from sqlalchemy import create_engine, MetaData, Table, Column, BigInteger, String, Boolean
from sqlalchemy.dialects.mysql import insert as upsert
from config import *
import time

# Create DB engine and database
engine = None
while not engine:
    try: # Keep trying until sql server finishes init
        engine = create_engine(f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}', echo=True)
    except Exception as e:
        print('Failed to connect')
        print(str(e))
        time.sleep(5)

while True:
    try:
        engine.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
        break
    except Exception as e:
        print('Failed to run command')
        print(str(e))
        time.sleep(20)
engine.execute(f'USE {DB_NAME}')

# Create table
metadata = MetaData(engine)
listings = Table('listings', metadata,
    Column('id', BigInteger(), primary_key=True, unique=True),
    Column('name', String(100)),
    Column('url', String(200)),
    Column('price', String(20)),
    Column('datetime', String(25)),
    Column('has_image', Boolean()),
    Column('geotag', String(30)),
    Column('where', String(100)),

    # Not as important
    Column('bedrooms', String(2)),
    Column('area', String(50)),
    Column('has_map', Boolean()),
    Column('repost_of', String(100)),
)
metadata.create_all()

def insert(result):

    real = {
        'id'         : result['id'],
        'name'       : result['name'],
        'url'        : result['url'],
        'price'      : result['price'] if result['price'] else 'No price given',
        'datetime'   : result['datetime'],
        'has_image'  : result['has_image'],
        'geotag'     : str(result['geotag']) if result['geotag'] else '(0,0)',
        'where'      : result['where'] if result['where'] else 'No location given',

        # Not as important
        'bedrooms'   : result['bedrooms'] if result['bedrooms'] else '-1',
        'area'       : result['area'] if result['area'] else 'No area given',
        'has_map'    : result['has_map'],
        'repost_of'  : result['repost_of'] if result['repost_of'] else 'No repost_of given',
    }

    ins = upsert(listings).values(
        id         = real['id'],
        name       = real['name'],
        url        = real['url'],
        price      = real['price'],
        datetime   = real['datetime'],
        has_image  = real['has_image'],
        geotag     = real['geotag'],
        where      = real['where'],

        # Not as important
        bedrooms   = real['bedrooms'],
        area       = real['area'],
        has_map    = real['has_map'],
        repost_of  = real['repost_of'],
    )
    on_duplicate_key_ins = ins.on_duplicate_key_update(
        id         = real['id'],
        name       = real['name'],
        url        = real['url'],
        price      = real['price'],
        datetime   = real['datetime'],
        has_image  = real['has_image'],
        geotag     = real['geotag'],
        where      = real['where'],

        # Not as important
        bedrooms   = real['bedrooms'],
        area       = real['area'],
        has_map    = real['has_map'],
        repost_of  = real['repost_of'],
    )
    conn = engine.connect()
    conn.execute(on_duplicate_key_ins)
    conn.close()

def get_all():
    conn = engine.connect()
    raw = conn.execute(listings.select())
    conn.close()

    results = {}
    for res in raw:
        print(type(res))
        data = {
            'id'         : res[0],
            'name'       : res[1],
            'url'        : res[2],
            'price'      : res[3],
            'datetime'   : res[4],
            'has_image'  : res[5],
            'geotag'     : res[6],
            'where'      : res[7],

            # Not as important
            'bedrooms'   : res[8],
            'area'       : res[9],
            'has_map'    : res[10],
            'repost_of'  : res[11],
        }
        results[data['id']] = data
    return results
