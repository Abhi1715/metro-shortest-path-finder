# 🚇 Hyderabad Metro Path Finder

A Django REST Framework project that finds the **shortest path** between any two stations in the Hyderabad Metro Rail network using **Dijkstra's Algorithm**.

## Features

- ✅ Full Hyderabad Metro network (Red, Blue, Green lines — 70+ stations)
- ✅ Dijkstra's shortest path algorithm (pure Python, no external libs needed)
- ✅ Optimize by **time** (fastest) or **distance** (shortest km)
- ✅ Turn-by-turn journey instructions with interchange guidance
- ✅ Estimated fare calculation
- ✅ REST API endpoints (DRF)
- ✅ Beautiful dark-themed HTML/CSS/JS frontend

---

## Setup & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Apply migrations

```bash
python manage.py migrate
```

### 3. Run the development server

```bash
python manage.py runserver
```

### 4. Open in browser

```
http://127.0.0.1:8000/
```

---

## API Endpoints

### List all stations
```
GET /api/stations/
```

**Response:**
```json
{
    "count": 75,
    "stations": [
        {"id": "ameerpet", "name": "Ameerpet", "line": ["Red", "Blue"]},
        ...
    ]
}
```

---

### Find Shortest Path

```
POST /api/shortest-path/
Content-Type: application/json

{
    "source": "miyapur",
    "destination": "hitec_city",
    "optimize": "time"
}
```

**optimize** can be:
- `"time"` — minimize travel time (minutes)
- `"distance"` — minimize distance (km)

**Response:**
```json
{
    "source": {"id": "miyapur", "name": "Miyapur", "line": ["Red"]},
    "destination": {"id": "hitec_city", "name": "HITEC City", "line": ["Blue"]},
    "path": [...],
    "total_stations": 18,
    "total_distance_km": 22.4,
    "total_time_minutes": 42,
    "fare_inr": 77,
    "steps": [
        {"action": "board", "line": "Red", "at_station": "Miyapur"},
        {"action": "change", "from_line": "Red", "to_line": "Blue", "at_station": "Ameerpet"},
        {"action": "alight", "at_station": "HITEC City"}
    ],
    "optimized_for": "time"
}
```

---

### GET shorthand (for testing in browser)

```
GET /api/shortest-path/?source=ameerpet&destination=raidurg&optimize=time
```

---

## Project Structure

```
hyderabad_metro/
├── manage.py
├── requirements.txt
├── metro_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── metro_api/
    ├── metro_graph.py      ← Graph data + Dijkstra's algorithm
    ├── serializers.py      ← DRF serializers
    ├── views.py            ← API views + HTML view
    ├── urls.py             ← Frontend URL
    ├── api_urls.py         ← API URLs
    └── templates/
        └── metro_api/
            └── index.html  ← Frontend UI
```

## Metro Lines Covered

| Line  | Route                  | Stations |
|-------|------------------------|----------|
| 🔴 Red   | Miyapur ↔ LB Nagar     | 27       |
| 🔵 Blue  | Nagole ↔ Raidurg       | 28       |
| 🟢 Green | JBS ↔ MGBS             | 13       |

**Interchanges:** Ameerpet (Red ↔ Blue), Secunderabad West (Blue ↔ Green), MG Bus Station (Red ↔ Green)
