import requests
from datetime import datetime, timedelta
import csv

def load_zip_code_database(file_path):
    zip_data = {}
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                zip_code = row['zip']
                zip_data[zip_code] = {
                    'city': row['city'],
                    'state_name': row['state_name']
                }
    except Exception as e:
        print(f"Error loading ZIP code database: {e}")
    return zip_data

def fetch_geocoding_data(query):
    url = f'https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1'
    headers = {'User-Agent': 'myweatherapp.com,/1.0 (contact@myweatherapp.com)'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    'lat': data[0]['lat'],
                    'lon': data[0]['lon'],
                    'address': data[0]['display_name']  
                }
            else:
                print("Enter valid city or zipcode")
        else:
            print(f"Geocoding API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    return None


def fetch_weather_data(lat, lon):
    url = f'https://api.weather.gov/points/{lat},{lon}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            forecast_url = response.json()['properties']['forecast']
            forecast_response = requests.get(forecast_url)
            if forecast_response.status_code == 200:
                return forecast_response.json()
            else:
                print(f"Forecast request failed with status code: {forecast_response.status_code}")
                print(f"Response: {forecast_response.text}")
        else:
            print(f"Weather API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    return None

def print_forecast(data):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    def is_today_or_tomorrow(time_str):
        date_part = time_str.split('T')[0]
        date_obj = datetime.fromisoformat(date_part).date()
        return date_obj == today or date_obj == tomorrow

    for period in data['properties']['periods']:
        time = period['startTime']
        if is_today_or_tomorrow(time):
            print(f"Time: {period['name']}")
            print(f"Temperature: {period['temperature']} {period['temperatureUnit']}")
            print(f"Short Forecast: {period['shortForecast']}")
            print(f"Detailed Forecast: {period['detailedForecast']}")
            print()

def main():
    zip_data = load_zip_code_database('C:/Users/megha/Downloads/zipcodes/uszips.csv')
    
    while True:
        user_input = input("Enter a city name or zipcode (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        # Determine if the input is a zipcode or city name
        if user_input.isdigit():  # Simple check for zipcode
            location = zip_data.get(user_input)
            if location:
                city = location['city']
                state = location['state_name']
                geocoding_data = fetch_geocoding_data(f"{city}, {state}")
                if geocoding_data:
                    lat, lon = geocoding_data['lat'], geocoding_data['lon']
                else:
                    print("Error fetching geocoding data.")
                    continue
            else:
                print("zipcode not found.")
                continue
        else:
            # Geocode city name
            geocoding_data = fetch_geocoding_data(user_input)
            if geocoding_data:
                city = geocoding_data['address']
            
                lat, lon = geocoding_data['lat'], geocoding_data['lon']
            else:
                print("City not found.")
                continue

        print(f"City: {city}")
        

        # Fetch weather data
        weather_data = fetch_weather_data(lat, lon)
        if weather_data:
            print("Weather Forecast:")
            print_forecast(weather_data)
        else:
            print("Error fetching weather data.")

if __name__ == '__main__':
    main()
