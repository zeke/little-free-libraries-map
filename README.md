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

The data is sourced from two Google My Maps:
- [Berkeley area map](https://www.google.com/maps/d/viewer?mid=1JXOsEi7Fhjretm6aXQEHMxdrHCk)
- [California-wide map](https://www.google.com/maps/d/viewer?mid=108krRpy3BwV0mDPKC9OtZXUnmkw)

## Development

### Updating Map Data

To fetch and merge the latest data from both sources:

```bash
./script/fetch-latest-map-data
```

This downloads both KMZ files, extracts the KML, merges them, and saves the result as `libraries.kml`.

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
