from flask import Flask, jsonify, request
import requests
import asyncio

app = Flask(__name__)

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    numbers = []

    async def fetch_numbers(url):
        try:
            response = await asyncio.wait_for(requests.get(url), timeout=0.5)
            if response.status_code == 200:
                data = response.json()
                numbers.extend(data.get('numbers', []))
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except (requests.exceptions.Timeout, asyncio.TimeoutError):
            print(f"Timeout occurred for URL: {url}")

    async def fetch_all_numbers():
        tasks = [fetch_numbers(url) for url in urls]
        await asyncio.gather(*tasks)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_all_numbers())

    unique_numbers = list(set(numbers))
    unique_numbers.sort()

    response = {
        "numbers": unique_numbers
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)  # Adjust the port number as per your preference
