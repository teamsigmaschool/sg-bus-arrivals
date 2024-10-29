from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def query_bus_id():
    id = request.args.get('id')
    if id:
        timings = get_bus_stop_timings(id)
        return jsonify(timings)
    else:
        return '''
        <p>
        To use, you have to type in the bus stop number (e.g. <strong>18141</strong>) as such:

        https://your-vercel-domain.vercel.app/?id=<strong>18141</strong>
        </p>
        '''

def get_bus_stop_timings(bus_stop_id):
    bus_timings = []
    api_url = f'https://arrivelah2.busrouter.sg/?id={bus_stop_id}'
    response = requests.get(api_url)
    services = response.json().get('services', [])
    if not services:
        return {"response": f'Bus stop {bus_stop_id} not found'}
    for service in services:
        bus_no = service['no']
        next_bus = service['next']
        operator = service['operator']
        next_bus_mins = round(next_bus['duration_ms'] / 1000 / 60)
        bus_timings.append({
            'bus_no': bus_no,
            'next_bus_mins': next_bus_mins,
            'operator': operator,
        })

    return {"bus_stop_id": bus_stop_id, "services": bus_timings}

# This block allows running locally
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
