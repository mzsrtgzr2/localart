import yaml
import requests
import time

# Load artist YAML
with open('artist-md-generator/artists.yaml', 'r') as f:
    data = yaml.safe_load(f)

artists = data.get('artists', [])
city_set = set()
for artist in artists:
    city = artist.get('city')
    if city:
        city_set.add(city)

locations = {}
for city in city_set:
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'city': city, 'country': 'Israel', 'format': 'json'}
    print(f"Fetching coordinates for {city}...")
    resp = requests.get(url, params=params, headers={'User-Agent': 'localart/1.0'})
    if resp.status_code == 200 and resp.json():
        lat = float(resp.json()[0]['lat'])
        lon = float(resp.json()[0]['lon'])
        locations[city] = {'lat': lat, 'lon': lon}
        print(f"  {city}: {lat}, {lon}")
    else:
        print(f"  {city}: Not found!")
    time.sleep(1)  # Be polite to the API

# Print YAML for locations section
print('\nlocations:')
for city, coords in locations.items():
    print(f"  {city}:")
    print(f"    lat: {coords['lat']}")
    print(f"    lon: {coords['lon']}")
