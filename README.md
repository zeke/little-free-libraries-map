# Little Free Libraries Map

An interactive map of Little Free Libraries in the Berkeley area.

## Features

- **Interactive Map**: Browse 1,100+ Little Free Library locations
- **Multiple Map Styles**: Choose from 9 different map styles including light, dark, and specialized themes
- **User Location**: Shows your current location on the map
- **Persistent Settings**: Remembers your preferred map style, position, and zoom level
- **Mobile Friendly**: Responsive design works on all devices

## View the Map

Visit the live site: [https://zeke.github.io/little-free-libraries-map/](https://zeke.github.io/little-free-libraries-map/)

## Data Source

Map data is generously provided and maintained by [Berkeley Little Free Libraries](https://berkeleylfl.wordpress.com).

The data is sourced from their [Google My Maps](https://www.google.com/maps/d/viewer?mid=1JXOsEi7Fhjretm6aXQEHMxdrHCk).

## Development

### Updating Map Data

To fetch the latest data:

```bash
./script/fetch-latest-map-data
```

This downloads the KMZ file, extracts the KML, and saves it as `libraries.kml`.

### Candidate Library Review Process

New library candidates can be photographed in the field and analyzed for addition to the map.

#### 1. Add Candidate Photos

Place photos (with GPS EXIF data) in the `candidates/` directory.

#### 2. Analyze Candidates

Run the analysis script to extract GPS coordinates, geocode addresses, and detect duplicates:

```bash
./script/analyze-candidates
```

This script:
- Extracts GPS coordinates from image EXIF data using `exiftool`
- Reverse geocodes coordinates to street addresses via the Nominatim API
- Detects potential duplicates within 20 meters of existing libraries
- Generates `candidates/analysis-report.json` with all metadata

#### 3. Review Candidates

Open `candidates/index.html` in a browser to view an interactive gallery showing:
- Each library photo with its address and coordinates
- Links to Google Maps and Street View
- Duplicate warnings for libraries already in the dataset
- Filter to view new libraries vs. potential duplicates

#### 4. Optimize Images (Optional)

Before committing images to the repository, optimize them to reduce file size:

```bash
./script/optimize-images
```

This resizes images to under 1MB while preserving GPS EXIF data.

### Local Development

Simply open `index.html` in your browser. No build process required.

### Deployment

The site automatically deploys to GitHub Pages on every push to the `main` branch via GitHub Actions.

## Tech Stack

- [Leaflet](https://leafletjs.com/) - Interactive map library
- [Leaflet Omnivore](https://github.com/mapbox/leaflet-omnivore) - KML parsing
- Vanilla JavaScript - No frameworks needed
- GitHub Pages - Hosting

## Map Styles

The map includes free tile providers:
- OpenStreetMap & OSM Humanitarian
- CartoDB Positron, Dark Matter, and Voyager (with label/no-label variants)

## Acknowledgments

Special thanks to the maintainer of [Berkeley Little Free Libraries](https://berkeleylfl.wordpress.com) for their dedicated work documenting and sharing these community resources.
