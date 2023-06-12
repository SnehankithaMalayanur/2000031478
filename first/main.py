from flask import Flask, jsonify
import requests
import time
from datetime import datetime, timedelta

app = Flask(__name__)

JOHN_DOE_RAILWAYS_API = "http://104.211.219.98/train/trains"
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODY1NDkxMTAsImNvbXBhbnlOYW1lIjoiVHJhaW4gQ2VudHJhbCIsImNsaWVudElEIjoiNGQ3NTUyYmMtYWFjNi00YmExLTg2ZDEtNjgyNDc5MzBlYWJmIiwib3duZXJOYW1lIjoiIiwib3duZXJFbWFpbCI6IiIsInJvbGxObyI6IjIwMDAwMzE0NzgifQ.b50_BC8OFBHzg9va7AKtstOHLmgOMR8T16ujXYkrYlM"

@app.route('/trains', methods=['GET'])
def get_trains():
    current_time = int(time.time())  # Get current Unix timestamp
    end_time = current_time + 12 * 60 * 60  # Set end time 12 hours from now

    trains = fetch_train_schedules(current_time, end_time)
    filtered_trains = filter_trains(trains)
    sorted_trains = sort_trains(filtered_trains)

    response = {
        "trains": sorted_trains
    }

    return jsonify(response)

def fetch_train_schedules(start_time, end_time):
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }

    url = f"{JOHN_DOE_RAILWAYS_API}/trains?scheduled_start_time={start_time}&scheduled_end_time={end_time}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        trains = response.json().get('trains', [])
        return trains
    else:
        return []

def filter_trains(trains):
    filtered_trains = []
    current_time = int(time.time())

    for train in trains:
        departure_time = train.get('departure_time')
        if departure_time - current_time > 30 * 60:  # Ignore trains departing in the next 30 minutes
            filtered_trains.append(train)

    return filtered_trains

def sort_trains(trains):
    sorted_trains = sorted(trains, key=lambda x: (x['price'], -x['ticket_availability'], -x['departure_time']))

    return sorted_trains

if __name__ == '__main__':
    app.run()
