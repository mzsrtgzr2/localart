import yaml
import os
import urllib.parse
import random
from jinja2 import Environment, FileSystemLoader

def load_city_coords():
    coords_path = os.path.join(os.path.dirname(__file__), '..', 'city_coords.yaml')
    if os.path.exists(coords_path):
        with open(coords_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

def generate_markdown(artist, template):
    # Prepare data for template
    data = {
        'name': artist['name'],
        'genre': artist.get('genre', 'Unknown'),
        'biography': artist.get('biography', ''),
        'paintings': artist.get('paintings', []),
        'contact': artist.get('contact', {}),
        'slug': artist.get('slug', artist['name'].replace(' ', '_').lower()),
        'images': artist.get('images', [])
    }
    return template.render(**data)

def generate_index_md(artists, output_path, env, city_coords):
    # Collect (artist, image, city, area, lat, lon) pairs
    showcase = []
    cities = set()
    areas = set()
    map_points = []
    for artist in artists:
        slug = artist.get('slug', artist['name'].replace(' ', '_').lower())
        images = artist.get('images', [])
        city = artist.get('city', '')
        area = artist.get('area', '')
        # Always resolve lat/lon before using
        lat = artist.get('lat', None)
        lon = artist.get('lon', None)
        # Convert to float if possible
        try:
            lat = float(lat) if lat not in (None, 'None', '') else None
        except Exception:
            lat = None
        try:
            lon = float(lon) if lon not in (None, 'None', '') else None
        except Exception:
            lon = None
        if (lat is None or lon is None) and city and city_coords.get(city):
            lat = float(city_coords[city]['lat'])
            lon = float(city_coords[city]['lon'])
        print(f"Artist: {artist['name']} | City: {city} | lat: {lat} | lon: {lon}")
        if city:
            cities.add(city)
        if area:
            areas.add(area)
        if images:
            img = random.choice(images)
            showcase.append({
                'artist_name': artist['name'],
                'slug': slug,
                'img_file': img['file'],
                'img_title': img.get('title', ''),
                'city': city,
                'area': area,
                'lat': lat if lat is not None else '',
                'lon': lon if lon is not None else '',
            })
        # Only add to map_points if both lat and lon are valid floats
        if lat is not None and lon is not None:
            try:
                latf = float(lat)
                lonf = float(lon)
                map_points.append({
                    'artist_name': artist['name'],
                    'slug': slug,
                    'lat': latf,
                    'lon': lonf,
                    'city': city,
                    'area': area,
                })
            except Exception:
                pass
    # Render index
    template = env.get_template('index_template.md.j2')
    with open(output_path, 'w') as f:
        f.write(template.render(showcase=showcase, cities=sorted(cities), areas=sorted(areas), map_points=map_points))


def main():
    # Path to YAML and output directory
    yaml_path = os.path.join(os.path.dirname(__file__), '../artists.yaml')
    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/artists')
    template_dir = os.path.dirname(__file__)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Reading artists from: {yaml_path}")
    print(f"Markdown output directory: {output_dir}\n")

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(template_dir))
    env.filters['urlencode'] = lambda value: urllib.parse.quote(value)
    template = env.get_template('artist_template.md.j2')

    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
        artists = data.get('artists', [])

    city_coords = load_city_coords()

    for artist in artists:
        print(f"Generating markdown for: {artist['name']} (slug: {artist.get('slug', artist['name'].replace(' ', '_').lower())})")
        md_content = generate_markdown(artist, template)
        filename = f"{artist.get('slug', artist['name'].replace(' ', '_').lower())}.md"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w') as md_file:
            md_file.write(md_content)
        print(f"  Markdown written to: {output_path}\n")
    
    index_output_path = os.path.join(os.path.dirname(__file__), '../../docs/index.md')
    generate_index_md(artists, index_output_path, env, city_coords)
    print(f"  Homepage index written to: {index_output_path}\n")

if __name__ == "__main__":
    main()