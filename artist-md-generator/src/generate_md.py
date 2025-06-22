import yaml
import os
import urllib.parse
import random
import re
import requests
from jinja2 import Environment, FileSystemLoader

def load_city_coords():
    coords_path = os.path.join(os.path.dirname(__file__), '..', 'city_coords.yaml')
    if os.path.exists(coords_path):
        with open(coords_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

def fetch_instagram_profile_image(username):
    try:
        url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            # Instagram's public API changes often; this works as of 2024
            if 'graphql' in data and 'user' in data['graphql']:
                return data['graphql']['user'].get('profile_pic_url_hd')
        return None
    except Exception:
        return None

def fetch_facebook_profile_image(url):
    # Extract username or ID from the Facebook URL
    match = re.search(r"facebook.com/([A-Za-z0-9_.]+)/?", url)
    if not match:
        return None
    username = match.group(1)
    # Facebook Graph API for profile picture (public)
    return f"https://graph.facebook.com/{username}/picture?type=large"

def extract_instagram_username(url):
    if not url:
        return None
    match = re.search(r"instagram.com/([A-Za-z0-9_.]+)/?", url)
    if match:
        return match.group(1)
    return None

def extract_instagram_profile(url):
    if not url:
        return None
    match = re.search(r"instagram.com/([A-Za-z0-9_.]+)/?", url)
    if match:
        return f"https://instagram.com/{match.group(1)}"
    return None

def load_allowed_image_tags():
    tags_path = os.path.join(os.path.dirname(__file__), '..', 'image_tags.yaml')
    if os.path.exists(tags_path):
        with open(tags_path, 'r') as f:
            data = yaml.safe_load(f)
            return set(data.get('allowed_tags', []))
    return set()

def generate_markdown(artist, template, allowed_tags):
    instagram_url = None
    contact = artist.get('contact', {})
    
    # Validate image tags
    images = []
    for img in artist.get('images', []):
        tags = img.get('tags', [])
        valid_tags = [tag for tag in tags if tag in allowed_tags]
        img = dict(img)
        img['tags'] = valid_tags
        images.append(img)
    # Set base_url for all pages to '/localart'
    data = {
        'name': artist['name'],
        'genre': artist.get('genre', 'Unknown'),
        'city': artist.get('city', ''),
        'biography': artist.get('biography', ''),
        'paintings': artist.get('paintings', []),
        'contact': contact,
        'slug': artist.get('slug', artist['name'].replace(' ', '_').lower()),
        'images': images,
        'instagram_url': instagram_url,
        'base_url': '/localart',
    }
    return template.render(**data)

def generate_index_md(artists, output_path, env, city_coords):
    # Collect (artist, image, city, area, lat, lon, tags) pairs
    showcase = []
    cities = set()
    areas = set()
    map_points = []
    allowed_tags = load_allowed_image_tags()
    for artist in artists:
        slug = artist.get('slug', artist['name'].replace(' ', '_').lower())
        images = artist.get('images', [])
        city = artist.get('city', '')
        area = artist.get('area', '')
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
            tags = [tag for tag in img.get('tags', []) if tag in allowed_tags]
            showcase.append({
                'artist_name': artist['name'],
                'slug': slug,
                'img_file': img['file'],
                'img_title': img.get('title', ''),
                'img_tags': tags,
                'img_price': img.get('price'),
                'img_sold': img.get('sold', False),
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
        f.write(template.render(showcase=showcase, cities=sorted(cities), areas=sorted(areas), map_points=map_points, base_url='/localart', allowed_tags=sorted(allowed_tags)))


def generate_image_detail_pages(artists, env):
    image_template = env.get_template('image_detail_template.md.j2')
    for artist in artists:
        slug = artist.get('slug', artist['name'].replace(' ', '_').lower())
        artist_name = artist['name']
        images = artist.get('images', [])
        for img in images:
            img_dir = os.path.join(os.path.dirname(__file__), '../../docs/artists', slug, 'image')
            os.makedirs(img_dir, exist_ok=True)
            img_filename = os.path.splitext(img['file'])[0] + '.md'
            img_path = os.path.join(img_dir, img_filename)
            md = image_template.render(
                img=img,
                slug=slug,
                artist_name=artist_name,
                base_url='/localart'
            )
            with open(img_path, 'w') as f:
                f.write(md)

def generate_tag_pages(artists, env):
    # Collect all artworks by tag
    tag_to_artworks = {}
    for artist in artists:
        artist_name = artist['name']
        artist_slug = artist.get('slug', artist_name.replace(' ', '_').lower())
        artist_page = f"../artists/{artist_slug}.md"
        for img in artist.get('images', []):
            image_title = img.get('title', img.get('file'))
            image_file = img.get('file')
            image_slug = os.path.splitext(image_file)[0]
            image_page = f"../artists/{artist_slug}/image/{image_slug}.md"
            image_tags = img.get('tags', [])
            image_price = img.get('price')
            image_sold = img.get('sold', False)
            for tag in image_tags:
                tag_to_artworks.setdefault(tag, []).append({
                    'artist_name': artist_name,
                    'artist_slug': artist_slug,
                    'artist_page': artist_page,
                    'image_file': image_file,
                    'image_title': image_title,
                    'image_slug': image_slug,
                    'image_page': image_page,
                    'image_tags': image_tags,
                    'image_price': image_price,
                    'image_sold': image_sold
                })
    tag_template = env.get_template('tag_page_template.md.j2')
    tags_dir = os.path.join(os.path.dirname(__file__), '../../docs/tags')
    os.makedirs(tags_dir, exist_ok=True)
    for tag, artworks in tag_to_artworks.items():
        tag_md_path = os.path.join(tags_dir, f"{tag}.md")
        with open(tag_md_path, 'w') as f:
            f.write(tag_template.render(tag=tag, artworks=artworks, base_url='/localart'))
    return sorted(tag_to_artworks.keys())

def generate_mkdocs_yml(artists, tags):
    template_dir = os.path.dirname(__file__)
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('mkdocs_template.yml.j2')
    mkdocs_content = template.render(artists=artists, tags=tags)
    mkdocs_path = os.path.join(os.path.dirname(__file__), '../../mkdocs.yml')
    with open(mkdocs_path, 'w') as f:
        f.write(mkdocs_content)
    print(f"mkdocs.yml generated at: {mkdocs_path}")

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
    allowed_tags = load_allowed_image_tags()

    for artist in artists:
        print(f"Generating markdown for: {artist['name']} (slug: {artist.get('slug', artist['name'].replace(' ', '_').lower())})")
        md_content = generate_markdown(artist, template, allowed_tags)
        filename = f"{artist.get('slug', artist['name'].replace(' ', '_').lower())}.md"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w') as md_file:
            md_file.write(md_content)
        print(f"  Markdown written to: {output_path}\n")
    
    index_output_path = os.path.join(os.path.dirname(__file__), '../../docs/index.md')
    generate_index_md(artists, index_output_path, env, city_coords)
    print(f"  Homepage index written to: {index_output_path}\n")
    generate_image_detail_pages(artists, env)
    print(f"  Image detail pages generated.\n")
    tags = generate_tag_pages(artists, env)
    generate_mkdocs_yml(artists, tags)

if __name__ == "__main__":
    main()