# Artist Markdown Generator

This project is designed to generate Markdown files for a list of artists based on a YAML configuration file. The main components of the project include a Python script that processes the YAML file and generates individual Markdown files for each artist.

## Project Structure

```
artist-md-generator
├── src
│   ├── generate_md.py
├── artists.yaml
└── README.md
```

## Files

- **src/generate_md.py**: This script reads the `artists.yaml` file, processes the list of artists, and generates Markdown files for each artist.

- **artists.yaml**: This YAML file contains a list of artists. Each entry includes the following details:
  - `name`: The name of the artist.
  - `genre`: The genre of music the artist is associated with.
  - `biography`: A short biography of the artist.

## Usage

1. Ensure you have Python installed on your machine.
2. Install any required dependencies (if applicable).
3. Update the `artists.yaml` file with the desired artist information.
4. Run the script using the command:

   ```
   python src/generate_md.py
   ```

5. The script will generate Markdown files for each artist in the project directory.

## Example of artists.yaml

```yaml
- name: Artist One
  genre: Rock
  biography: "Artist One is a rock musician known for their energetic performances."

- name: Artist Two
  genre: Jazz
  biography: "Artist Two is a jazz artist with a unique style and sound."
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.