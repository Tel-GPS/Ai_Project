import overpy

def get_city_bounding_box(city_name):
    # You can use the Nominatim geocoding service to get the city's bounding box
    # For simplicity, we'll use hardcoded bounding boxes for New York and Washington

    bounding_boxes = {
        "New York": (40.4774, -74.2590, 40.9176, -73.7004),
        "Washington": (38.7722, -77.2639, 39.0564, -76.8350)
    }

    return bounding_boxes.get(city_name, None)

def fetch_osm_data(city_name):
    bounding_box = get_city_bounding_box(city_name)

    if not bounding_box:
        print(f"No bounding box found for {city_name}")
        return

    api = overpy.Overpass()

    # Fetch ways (linear features like roads, paths, and tracks) within the bounding box
    query = f"""
    [out:json];
    way["highway"]({bounding_box[0]}, {bounding_box[1]}, {bounding_box[2]}, {bounding_box[3]});
    out body;
    >;
    out skel qt;
    """

    result = api.query(query)
    return result

if __name__ == "__main__":
    cities = ["New York", "Washington"]

    for city in cities:
        print(f"Fetching OSM data for {city}:")
        data = fetch_osm_data(city)
        # Process or save the data as needed
