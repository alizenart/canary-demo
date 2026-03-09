
from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest
import time
import random

app = Flask(__name__)



# adding metrics for Prometheus
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total number of requests',
    ['version']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency',
    ['version']
)


VERSION = "v2 (canary)" 

@app.route("/")
def home():
    start_time = time.time()

    # simulating work
    time.sleep(random.uniform(0.05, 0.2))

    REQUEST_COUNT.labels(version=VERSION).inc()
    REQUEST_LATENCY.labels(version=VERSION).observe(time.time() - start_time)

    return {
        "version": VERSION,
        "message": "Hi canary! 🐦"
    }


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
