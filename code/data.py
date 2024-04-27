import csv
import requests

def main():

    api_key = 'api'
    origin = 'Central Park, New York'
    destination = 'East Village, New York, État de New York, États-Unis'
    STEP_SIZE_FT = 200 # Consume quickly the api if small

    # Récupération des coordonnées le long de l'itinéraire
    route_coordinates = get_route_coordinates(api_key, origin, destination, STEP_SIZE_FT)
    if route_coordinates:
        print("Coordonnées le long de l'itinéraire :")
        for i, coord in enumerate(route_coordinates, start=1):
            print(f"Étape {i}: Latitude = {coord[0]}, Longitude = {coord[1]}")

        # Écrire les coordonnées dans un fichier CSV
        write_to_csv('coordinates.csv', route_coordinates)
        print("Les coordonnées ont été écrites dans le fichier coordinates.csv.")

        # Récupération des images Google Street View et des images satellites
        get_street_view_images(api_key, route_coordinates)
        print("Les images Google Street View et satellites ont été récupérées.")



def get_route_coordinates(api_key, origin, destination, STEP_SIZE_FT):
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': origin,
        'destination': destination,
        'key': api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'routes' in data and len(data['routes']) > 0:
        route = data['routes'][0]
        steps = route['legs'][0]['steps']
        coordinates = []

        for step in steps:
            start_location = step['start_location']
            end_location = step['end_location']

            distance = step['distance']['value']

            interpolated_coords = interpolate_coordinates(start_location, end_location, distance, STEP_SIZE_FT)

            coordinates.extend(interpolated_coords)

        # Ajouter la dernière étape (destination)
        last_step_end_location = steps[-1]['end_location']
        coordinates.append((last_step_end_location['lat'], last_step_end_location['lng']))

        return coordinates
    else:
        print("Aucun itinéraire trouvé entre les adresses spécifiées.")
        if 'status' in data:
            print("Statut de la requête:", data['status'])
        return None

def get_street_view_images(api_key, coordinates):
    for i, coord in enumerate(coordinates, start=1):
        lat, lng = coord
        # Récupération de l'image Street View
        street_view_url = f"https://maps.googleapis.com/maps/api/streetview?size=1920x1080&location={lat},{lng}&key={api_key}"
        street_view_response = requests.get(street_view_url)
        if street_view_response.status_code == 200:
            with open(f"streetview_{i}.jpg", 'wb') as f:
                f.write(street_view_response.content)
                print(f"{i}: Image street view aux coordonnéeslat:{lat} lng:{lng} enregistrée")
        else:
            print(f"Impossible de récupérer l'image Street View pour la coordonnée {lat}, {lng}")

        # Récupération de l'image satellite
        satellite_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom=17&size=1920x1080&maptype=satellite&key={api_key}"
        satellite_response = requests.get(satellite_url)
        if satellite_response.status_code == 200:
            with open(f"satellite_{i}.jpg", 'wb') as f:
                f.write(satellite_response.content)
                print(f"{i}: Image satellite aux coordonnées lat:{lat} lng:{lng} enregistrée")
        else:
            print(f"Impossible de récupérer l'image satellite pour la coordonnée {lat}, {lng}")

def write_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Latitude', 'Longitude'])

        for item in data:
            csv_writer.writerow(item)

def interpolate_coordinates(start, end, distance, step_size):
    units = step_size/3.28
    segments = 1 if distance/units < 1 else int(distance/units)
    # Calculer les deltas latitudinaux et longitudinaux
    delta_lat = (end['lat'] - start['lat']) / segments
    delta_lng = (end['lng'] - start['lng']) / segments

    # Générer les coordonnées intermédiaires
    interpolated_coordinates = []
    for i in range(segments):
        lat = round(start['lat'] + i * delta_lat, 7)
        lng = round(start['lng'] + i * delta_lng, 7)
        interpolated_coordinates.append((lat, lng))


    return interpolated_coordinates


if __name__ == "__main__":
    main()
