import requests
import pandas as pd

# Your OpenWeatherMap API Key
api_key = "19822d28f1855e39280a2235f69a5c06"

# List of cities with their latitude and longitude
cities = [
    {"name": "London", "lat": 51.5074, "lon": -0.1278},
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "Delhi", "lat": 28.6139, "lon": 77.2090}
]

# List to store weather data
weather_data = []

# Function to fetch weather data for the forecast
def fetch_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={city['lat']}&lon={city['lon']}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Collecting 5-day forecast data (3-hour intervals)
        for entry in data['list']:
            timestamp = entry['dt']  # Timestamp of the weather data
            temp = entry['main']['temp']  # Temperature in Celsius
            humidity = entry['main']['humidity']  # Humidity in percentage
            weather_description = entry['weather'][0]['description']  # Weather condition (e.g., "clear sky")
            wind_speed = entry['wind']['speed']  # Wind speed in m/s
            
            # Convert timestamp to readable date and time
            date_time = pd.to_datetime(timestamp, unit='s')
            
            # Save the data in a dictionary
            weather_data.append({
                'city': city['name'],
                'date_time': date_time,
                'temp': temp,
                'humidity': humidity,
                'weather_description': weather_description,
                'wind_speed': wind_speed
            })
    else:
        print(f"Failed to fetch data for {city['name']}: {response.status_code}")

# Fetch the data for all cities
for city in cities:
    fetch_weather_data(city, api_key)

# Convert the collected data to a Pandas DataFrame
df = pd.DataFrame(weather_data)

# Save the data to a CSV file
df.to_csv('weather_forecast.csv', index=False)

print("Weather forecast data for 5 cities saved to weather_forecast_5_cities.csv.")
