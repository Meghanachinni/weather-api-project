from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Replace 'your_geocodio_api_key' with your actual Geocodio API key
GEOCODIO_API_KEY = 'api code'
GEOCODIO_URL = 'https://api.geocod.io/v1.6/geocode'

WEATHER_API_URL = 'https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    location = request.form.get('location')
    
    # Get coordinates from Geocodio
    geocodio_params = {
        'q': location,
        'api_key': GEOCODIO_API_KEY
    }
    geocodio_response = requests.get(GEOCODIO_URL, params=geocodio_params)
    geocodio_data = geocodio_response.json()
    print("Geocodio Response:", geocodio_data)
    
    if 'results' in geocodio_data and geocodio_data['results']:
        first_result = geocodio_data['results'][0]
        lat = first_result['location']['lat']
        lon = first_result['location']['lng']
        city = first_result['address_components']['city']
        state = first_result['address_components']['state']
        zip_code = first_result['address_components']['zip']
        
        # Convert lat/lon to grid points
        points_url = f'https://api.weather.gov/points/{lat},{lon}'
        points_response = requests.get(points_url)
        points_data = points_response.json()
        print("Points API Response:", points_data)

        if 'properties' in points_data:
            office = points_data['properties']['gridId']
            gridX = points_data['properties']['gridX']
            gridY = points_data['properties']['gridY']
            
            # Get weather data from weather.gov API
            weather_url = WEATHER_API_URL.format(office=office, gridX=gridX, gridY=gridY)
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()
            print("Weather API Response:", weather_data)
            
            if 'properties' in weather_data and 'periods' in weather_data['properties']:
                # Add city, state, and zip to the response
                response_data = {
                    'city': city,
                    'state': state,
                    'zip_code': zip_code,
                    'weather': weather_data
                }
                return jsonify(response_data)
    
    return jsonify({'error': 'No weather data available'}), 404

if __name__ == '__main__':
    app.run(debug=True)
