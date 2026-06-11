# RouteWise Fuel Optimizer

## Overview

RouteWise Fuel Optimizer is a backend service that helps identify cost-effective fuel stops for long-haul trucking routes.

The service:

* Accepts a start location and destination within the USA
* Calculates route distance using OpenRouteService
* Estimates fuel consumption and fuel cost
* Recommends fuel stations from the provided dataset
* Returns route geometry for map visualization

---

## Features

* Route optimization
* Fuel cost estimation
* Fuel stop recommendations
* Geocoded fuel station dataset
* REST API using Django REST Framework

---

## Tech Stack

* Python 3
* Django
* Django REST Framework
* OpenRouteService API
* GeoPy
* SQLite

---

## Dataset

The provided fuel station dataset contained:

* Truck stop name
* Address
* City
* State
* Fuel price

The dataset did not include latitude and longitude coordinates.

To support route-aware fuel optimization, a geocoding enrichment process was implemented.

### Geocoding Results

* Total Fuel Stations: 8151
* Successfully Geocoded: 8151
* Coverage: 100%

Coordinates are persisted in the database and reused during route optimization to avoid repeated external geocoding calls.

---

## Setup

### Clone Repository

```bash
git clone https://github.com/Ranjanshukla/fuel-route-optimizer.git
cd fuel-route-optimizer
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Import Fuel Dataset

```bash
python manage.py import_fuel_prices
```

### Run Server

```bash
python manage.py runserver
```

---

## API Endpoint

### Optimize Route

**POST**

```text
/api/route/optimize/
```

### Request

```json
{
  "start": "Dallas, TX",
  "destination": "Chicago, IL"
}
```

### Sample Response

```json
{
    "start": "Dallas, TX",
    "destination": "Chicago, IL",
    "distance_miles": 969.66,
    "duration_seconds": 55702.0,
    "fuel_stops_required": 1,
    "estimated_fuel_cost": 267.24,
    "recommended_fuel_stops": [
        {
            "name": "One9 #1248",
            "city": "Wilmer",
            "state": "TX",
            "price": 2.756
        }
    ],
  "route_geometry": "..."
}
```

---

## Design Decisions

To reduce external API usage:

* Fuel stations are geocoded once and stored locally.
* Route data is fetched from OpenRouteService.
* Geocoded coordinates are reused for future requests.

This approach minimizes routing and geocoding API calls while improving response time.

---

## Future Improvements

* Spatial indexing for faster proximity searches
* PostGIS integration
* Advanced route-aware fuel stop selection
* Multi-stop route planning
* Real-time fuel price updates

---

## Author

Ranjan Shukla
