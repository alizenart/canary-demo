# Canary Staged Deployment Demo with Monitoring

There are two versions of deployment

* **v1 (stable)** – the current production version
* **v2 (canary)** – the new version released to a small portion of users

In Canary Deployment, we slowly roll out the deployment of the new canary version by testing smaller amounts of traffic at a time and monitoring for errors.


# Components:

* **NGINX** – splits traffic between application versions
* **Flask apps** – simple apps to serve responses and expose metrics
* **Prometheus** – scrapes metrics from the apps
* **Grafana** – visualizes metrics in dashboards

# To run:

You must have **Docker Desktop** installed.

Download Docker Desktop:

https://www.docker.com/products/docker-desktop/

Verify installation:

```bash
docker --version
docker compose version
```


# This is the project structure

```
canary-demo/
│
├── docker-compose.yml
├── nginx.conf
├── prometheus.yml
│
├── app_v1/
│   ├── app.py
│   └── Dockerfile
│
└── app_v2/
    ├── app.py
    └── Dockerfile
```


# Step 1: Clone the Repository

```
git clone https://github.com/YOUR_USERNAME/canary-demo.git
cd canary-demo
```

# Step 2: Start the System

Build and start all containers:

```
docker compose up --build
```

The following services will be started:

* app_v1
* app_v2
* nginx
* prometheus
* grafana


# Step 3: Test the Canary Deployment

Open your browser:

```
http://localhost:8080
```

Refresh the page a couple times.

You should the messages below.

```
{
  "version": "v1 (stable)",
  "message": "Hello from v1 (stable)"
}
```

Sometimes you will see:

```
{
  "version": "v2 (canary)",
  "message": "Hello from v2 (canary)"
}
```

According to the current NGINX weight settings, stable should be seen 90% and canary 10%.


# Step 5: View Prometheus Metrics

Open Prometheus:

```
http://localhost:9090
```

The current metrics tracked are the total app requests for each version and the latency rate.

Example queries:

```
app_requests_total
```

or

```
rate(app_requests_total[1m])
```


# Step 6: View Grafana Dashboards

Open Grafana:

```
http://localhost:3000
```

Login credentials:

```
username: admin
password: admin
```

Add Prometheus as a data source:

1. Go to **Settings → Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. Set URL:

```
http://prometheus:9090
```

5. Click **Save & Test**


# Step 7: Create Monitoring Panels in Grafana

Create a dashboard panel with the query:

```
rate(app_requests_total[1m])
```

This shows the request rate per application version.

You can also monitor latency:

```
rate(app_request_latency_seconds_sum[1m])
/
rate(app_request_latency_seconds_count[1m])
```

# Changing Percentage

Traffic distribution is controlled in `nginx.conf`.

To change the rollout to be 50/50


```
server app_v1:5000 weight=5;
server app_v2:5000 weight=5;
```

Restart NGINX after changes:

```
docker compose restart nginx
```


# Stopping the System

To stop all containers, run:

```
docker compose down
```
