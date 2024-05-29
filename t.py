

from flask import request
import requests

# Get the user's IP address
user_ip = request.remote_addr

# Attempt to get information from the IP info service
try:
    response = requests.get(f"https://ipinfo.io/{user_ip}")
    response.raise_for_status()  # Raise an error for bad status codes
    data = response.json()
    city = data.get('city', '')
    region = data.get('region', '')
    country = data.get('country', '')
except requests.exceptions.RequestException as e:
    # Handle the error appropriately
    print(f"Error fetching data: {e}")
    city, region, country = '', '', ''

# Find the IP in the database
dag = ips.find_one({"ip": user_ip})

# Use the city, region, country variables as needed
