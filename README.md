## Switchbot Temperature Dashboard

### Overview

This project provides a simple end-to-end setup for collecting, storing, and visualizing temperature data from SwitchBot devices.

It consists of:
- A Python-based logging application that collects temperature data
- **InfluxDB** as a time-series database for storing the data
- **Grafana** for visualizing the data in real time

Using Docker Compose, InfluxDB and Grafana can be started quickly with minimal configuration.
Once the services are running, you can configure the data source and dashboard through the web UI and immediately start monitoring temperature trends.

### Getting Started

1. Clone the repository:
   ```bash
   git clone
   ```
1. Navigate to the project directory:
   ```bash
   cd switchbot-temperature-dashboard
   ```
1. Install the required dependencies:
   ```bash
   uv sync
   ```
1. Copy .env.example to .env and fill in your configurations:
   ```bash
   cp .env.example .env
   ```
1. Start the InfluxDB and Grafana:
   ```bash
   docker compose up -d
   ```
1. Configure InfluxDB:
    1.  Open the InfluxDB UI in your browser:
        ```
        http://localhost:8086
        ```
    1. Log in using the following credentials:
        - Username: value of the `DOCKER_INFLUXDB_INIT_USERNAME` environment variable
        - Password: value of the `DOCKER_INFLUXDB_INIT_PASSWORD` environment variable
    1. Once logged in successfully, the InfluxDB setup is complete.
1. Configure Grafana:
    1. Log in to Grafana
        ```
        http://localhost:3000
        ```
    1. Log in with the following credentials:
        - Username: `admin`
        - Password: value of the `GF_SECURITY_ADMIN_PASSWORD` environment variable
    1. Register InfluxDB as a Data Source
        1. Click Data sources from the left-hand menu
        1. Click Add data source and select InfluxDB
        1. Query Language
            - Select Flux
        1. HTTP
            - URL: `http://influxdb:8086`
        1. InfluxDB Details
            - Organization: value of the `INFLUXDB_ORG` environment variable
            - Token: value of the environment `INFLUXDB_TOKEN` variable
            - Default bucket: value of the `INFLUXDB_BUCKET` environment variable
        1. Click Save & test
1. Start the logging application:
   ```bash
   uv run main.py
   ```
1. Set up Dashboard (Grafana):
    1. Create a New Dashboard
        1. In Grafana, click Dashboards from the left-hand menu
        1. Click New → New dashboard
        1. Click Add visualization
    1. Configure the Panel Query
        1. In the Query section at the bottom of the screen:
           - Data source: Select the InfluxDB data source you added earlier
           - Query language: Flux
        1. Example Flux query:
           ```flux
           from(bucket: "your-bucket-name")
             |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
             |> filter(fn: (r) => r._measurement == "sensor")
             |> filter(fn: (r) => r._field == "temp_c")
        1. Configure Visualization
            1. In the Visualization panel:
                - Select Time series (recommended for temperature data)
            1. Set a panel title, for example:
                - Title: Temperature
        1. Save the Dashboard
            1. Click Save dashboard (disk icon in the top right)
            1. Enter a dashboard name, for example:
                - SwitchBot Temperature Dashboard
            1. Click Save
        1. Verify the Data
            1. If data is being written correctly to InfluxDB, the graph should display time-series data.
            1. Adjust the time range (top-right corner) if no data is visible.

        You have now successfully set up a Grafana dashboard connected to InfluxDB.
