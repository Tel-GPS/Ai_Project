import csv
import requests

def get_route_coordinates(api_key, origin, destination):
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
            coordinates.append((start_location['lat'], start_location['lng']))

        # Ajouter la dernière étape (destination)
        end_location = steps[-1]['end_location']
        coordinates.append((end_location['lat'], end_location['lng']))

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
        street_view_url = f"https://maps.googleapis.com/maps/api/streetview?size=600x400&location={lat},{lng}&key={api_key}"
        street_view_response = requests.get(street_view_url)
        if street_view_response.status_code == 200:
            with open(f"streetview_{i}.jpg", 'wb') as f:
                f.write(street_view_response.content)
        else:
            print(f"Impossible de récupérer l'image Street View pour la coordonnée {lat}, {lng}")

        # Récupération de l'image satellite
        satellite_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom=17&size=600x400&maptype=satellite&key={api_key}"
        satellite_response = requests.get(satellite_url)
        if satellite_response.status_code == 200:
            with open(f"satellite_{i}.jpg", 'wb') as f:
                f.write(satellite_response.content)
        else:
            print(f"Impossible de récupérer l'image satellite pour la coordonnée {lat}, {lng}")

def write_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Latitude', 'Longitude'])

        for item in data:
            csv_writer.writerow(item)

def main():
    # Insérez votre clé API Google Maps
    api_key = 'AIzaSyC3bKufPC-AeeCrONHR2bCDulr0hJbEh6w'

    # Adresses de départ et d'arrivée
    origin = 'Central Park, New York'
    destination = 'East Village, New York, État de New York, États-Unis'

    # Récupération des coordonnées le long de l'itinéraire
    route_coordinates = get_route_coordinates(api_key, origin, destination)
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

if __name__ == "__main__":
    main()
