from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import requests
from urllib.request import urlretrieve
import geocoder

MAPBOX_KEY = "pk.eyJ1IjoiYW5pc292IiwiYSI6ImNrMm90Mm1sZTEzZGwzbmxubHlpanVwbnUifQ.pqzxDULrQBz-arhWo8BaKA"

def city_to_coordinates(name):
    g = geocoder.mapbox(f'{name}', country='BY', key=MAPBOX_KEY).json
    return f'{g["lng"]},{g["lat"]}'

def get_polyline(cities):
    start = city_to_coordinates(cities[0])
    finish = city_to_coordinates(cities[-1])

    directions = f'https://api.mapbox.com/directions/v5/mapbox/driving/{start};{finish}?access_token={MAPBOX_KEY}'
    response = requests.get(directions).json()
    polyline = response['routes'][0]['geometry']
    return polyline

def get_matrix(cities):
    cities_coordinates = ''
    for city in cities:
        cities_coordinates += f'{city_to_coordinates(city)};'
    
    url = f'https://api.mapbox.com/directions-matrix/v1/mapbox/driving/{cities_coordinates[:-1]}?access_token={MAPBOX_KEY}'
    matrix = requests.get(url).json()['durations']
    for i in range(len(cities)):
        matrix[i][i] = float('inf')
    return matrix

def get_map(cities, original_cities):
    matrix = get_matrix(cities)
    X = csr_matrix(matrix)
    Tcsr = minimum_spanning_tree(X)
    distance = int(sum(Tcsr.data)/100)
    start, finish = Tcsr.nonzero()
    index_of_cities = zip(start, finish)

    polyline = ""
    for index in index_of_cities:
        start_city = cities[index[0]]
        finish_city = cities[index[1]]
        new_line = get_polyline([start_city, finish_city])
        polyline += f'path-5+FF5721-0.5({new_line}),'

    markers = ""
    for index, city in enumerate(cities):
        number = original_cities.index(city) + 1
        markers += f"pin-l-{number}+000({city_to_coordinates(city)}),"

    url = f"https://api.mapbox.com/styles/v1/anisov/ck2otgw050fth1cqu9zrqxcdy/static/{polyline}{markers[:-1]}/auto/1280x720@2x?access_token={MAPBOX_KEY}&logo=false"
    urlretrieve(url, 'myimg.png')
    
    return distance

if __name__ == "__main__":
    s = ["Брест","Пинск","Минск"]
    get_map(s,s)
