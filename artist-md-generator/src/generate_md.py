import yaml
import os
import urllib.parse

def generate_markdown(artist, images):
    name = artist['name']
    genre = artist.get('genre', 'Unknown')
    biography = artist.get('biography', '')
    paintings = artist.get('paintings', [])
    contact = artist.get('contact', {})
    slug = artist.get('slug', name.replace(' ', '_').lower())

    md_content = f"# {name}\n\n"
    md_content += f"**Genre:** {genre}\n\n"
    md_content += f"**Biography:**\n{biography}\n\n"

    if images:
        md_content += "## Showcase\n"
        md_content += '<div style="display: flex; flex-wrap: wrap; gap: 16px;">\n'
        for img in images:
            img_url = f"/assets/artists/{slug}/{urllib.parse.quote(img)}"
            md_content += f'<img src="{img_url}" alt="{name}" style="width:200px; height:auto; object-fit:cover; border-radius:8px;" />\n'
        md_content += '</div>\n\n'

    if paintings:
        md_content += "## Paintings\n"
        for painting in paintings:
            md_content += f"- {painting}\n"
        md_content += "\n"

    if contact:
        md_content += "## Contact Information\n"
        for key, value in contact.items():
            md_content += f"- **{key.capitalize()}**: {value}\n"
        md_content += "\n"

    return md_content


def main():
    # Path to YAML and output directory
    yaml_path = os.path.join(os.path.dirname(__file__), '../artists.yaml')
    output_dir = os.path.join(os.path.dirname(__file__), '../../docs/artists')
    assets_dir = os.path.join(os.path.dirname(__file__), '../../docs/assets/artists')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

    print(f"Reading artists from: {yaml_path}")
    print(f"Markdown output directory: {output_dir}")
    print(f"Assets directory: {assets_dir}\n")

    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
        artists = data.get('artists', [])

    for artist in artists:
        slug = artist.get('slug', artist['name'].replace(' ', '_').lower())
        artist_dir = os.path.join(assets_dir, slug)
        images = []
        if os.path.isdir(artist_dir):
            images = [f for f in os.listdir(artist_dir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))]
        print(f"Generating markdown for: {artist['name']} (slug: {slug})")
        print(f"  Found {len(images)} images in {artist_dir}")
        md_content = generate_markdown(artist, images)
        filename = f"{slug}.md"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w') as md_file:
            md_file.write(md_content)
        print(f"  Markdown written to: {output_path}\n")

if __name__ == "__main__":
    main()