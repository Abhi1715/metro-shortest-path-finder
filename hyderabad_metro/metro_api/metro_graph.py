"""
Hyderabad Metro Rail Network Data
Lines:
- Red Line (Miyapur ↔ LB Nagar)
- Blue Line (Nagole ↔ Raidurg)  
- Green Line (JBS ↔ MGBS)
"""

import heapq
from collections import defaultdict

# Station data: id -> {name, line, interchange}
STATIONS = {
    # RED LINE (Miyapur ↔ LB Nagar) - 29 stations
    "miyapur": {"name": "Miyapur", "line": ["Red"], "color": "#E53E3E"},
    "jntu_college": {"name": "JNTU College", "line": ["Red"], "color": "#E53E3E"},
    "kphb_colony": {"name": "KPHB Colony", "line": ["Red"], "color": "#E53E3E"},
    "kukatpally": {"name": "Kukatpally", "line": ["Red"], "color": "#E53E3E"},
    "balanagar": {"name": "Balanagar", "line": ["Red"], "color": "#E53E3E"},
    "moosapet": {"name": "Moosapet", "line": ["Red"], "color": "#E53E3E"},
    "bharat_nagar": {"name": "Bharat Nagar", "line": ["Red"], "color": "#E53E3E"},
    "erragadda": {"name": "Erragadda", "line": ["Red"], "color": "#E53E3E"},
    "esp_colony": {"name": "ESI Hospital", "line": ["Red"], "color": "#E53E3E"},
    "sr_nagar": {"name": "SR Nagar", "line": ["Red"], "color": "#E53E3E"},
    "ameerpet": {"name": "Ameerpet", "line": ["Red", "Blue"], "color": "#805AD5"},
    "punjagutta": {"name": "Punjagutta", "line": ["Red"], "color": "#E53E3E"},
    "irrum_manzil": {"name": "Irrum Manzil", "line": ["Red"], "color": "#E53E3E"},
    "khairatabad": {"name": "Khairatabad", "line": ["Red"], "color": "#E53E3E"},
    "lakdikapul": {"name": "Lakdi Ka Pul", "line": ["Red"], "color": "#E53E3E"},
    "assembly": {"name": "Assembly", "line": ["Red"], "color": "#E53E3E"},
    "nampally": {"name": "Nampally", "line": ["Red"], "color": "#E53E3E"},
    "gandhi_bhavan": {"name": "Gandhi Bhavan", "line": ["Red"], "color": "#E53E3E"},
    "osmania_medical": {"name": "Osmania Medical College", "line": ["Red"], "color": "#E53E3E"},
    "mg_bus_station": {"name": "MG Bus Station", "line": ["Red", "Green"], "color": "#805AD5"},
    "malakpet": {"name": "Malakpet", "line": ["Red"], "color": "#E53E3E"},
    "new_market": {"name": "New Market", "line": ["Red"], "color": "#E53E3E"},
    "musarambagh": {"name": "Musarambagh", "line": ["Red"], "color": "#E53E3E"},
    "dilsukhnagar": {"name": "Dilsukhnagar", "line": ["Red"], "color": "#E53E3E"},
    "chaitanyapuri": {"name": "Chaitanyapuri", "line": ["Red"], "color": "#E53E3E"},
    "victoria_memorial": {"name": "Victoria Memorial", "line": ["Red"], "color": "#E53E3E"},
    "lb_nagar": {"name": "LB Nagar", "line": ["Red"], "color": "#E53E3E"},

    # BLUE LINE (Nagole ↔ Raidurg) - 27 stations
    "nagole": {"name": "Nagole", "line": ["Blue"], "color": "#3182CE"},
    "uppal": {"name": "Uppal", "line": ["Blue"], "color": "#3182CE"},
    "stadium": {"name": "Stadium", "line": ["Blue"], "color": "#3182CE"},
    "ngri": {"name": "NGRI", "line": ["Blue"], "color": "#3182CE"},
    "habsiguda": {"name": "Habsiguda", "line": ["Blue"], "color": "#3182CE"},
    "tarnaka": {"name": "Tarnaka", "line": ["Blue"], "color": "#3182CE"},
    "mettuguda": {"name": "Mettuguda", "line": ["Blue"], "color": "#3182CE"},
    "secunderabad_east": {"name": "Secunderabad East", "line": ["Blue"], "color": "#3182CE"},
    "parade_grounds": {"name": "Parade Grounds", "line": ["Blue"], "color": "#3182CE"},
    "secunderabad_west": {"name": "Secunderabad West", "line": ["Blue", "Green"], "color": "#805AD5"},
    "Gandhi_hospital": {"name": "Gandhi Hospital", "line": ["Blue"], "color": "#3182CE"},
    "musheerabad": {"name": "Musheerabad", "line": ["Blue"], "color": "#3182CE"},
    "rsp_south": {"name": "RTC Cross Roads", "line": ["Blue"], "color": "#3182CE"},
    "chikkadpally": {"name": "Chikkadpally", "line": ["Blue"], "color": "#3182CE"},
    "narayanaguda": {"name": "Narayanaguda", "line": ["Blue"], "color": "#3182CE"},
    "sultan_bazar": {"name": "Sultan Bazar", "line": ["Blue"], "color": "#3182CE"},
    "central_secretariat": {"name": "Central Secretariat", "line": ["Blue"], "color": "#3182CE"},
    "khairatabad_blue": {"name": "Khairatabad (Blue)", "line": ["Blue"], "color": "#3182CE"},
    "imax": {"name": "Imax", "line": ["Blue"], "color": "#3182CE"},
    "panjagutta_blue": {"name": "Panjagutta (Blue)", "line": ["Blue"], "color": "#3182CE"},
    "yousufguda": {"name": "Yousufguda", "line": ["Blue"], "color": "#3182CE"},
    "road_no5_jubilee_hills": {"name": "Road No. 5 Jubilee Hills", "line": ["Blue"], "color": "#3182CE"},
    "jubilee_hills_check_post": {"name": "Jubilee Hills Check Post", "line": ["Blue"], "color": "#3182CE"},
    "peddamma_temple": {"name": "Peddamma Temple", "line": ["Blue"], "color": "#3182CE"},
    "madhapur": {"name": "Madhapur", "line": ["Blue"], "color": "#3182CE"},
    "durgam_cheruvu": {"name": "Durgam Cheruvu", "line": ["Blue"], "color": "#3182CE"},
    "hitec_city": {"name": "HITEC City", "line": ["Blue"], "color": "#3182CE"},
    "raidurg": {"name": "Raidurg", "line": ["Blue"], "color": "#3182CE"},

    # GREEN LINE (JBS ↔ MGBS) - 8 stations
    "jbs": {"name": "Jubilee Bus Station", "line": ["Green"], "color": "#38A169"},
    "parade_grounds_green": {"name": "Parade Grounds", "line": ["Green"], "color": "#38A169"},
    "rasoolpura": {"name": "Rasoolpura", "line": ["Green"], "color": "#38A169"},
    "prakash_nagar": {"name": "Prakash Nagar", "line": ["Green"], "color": "#38A169"},
    "begumpet": {"name": "Begumpet", "line": ["Green"], "color": "#38A169"},
    "madhura_nagar": {"name": "Madhura Nagar", "line": ["Green"], "color": "#38A169"},
    "yousufguda_green": {"name": "Yousufguda (Green)", "line": ["Green"], "color": "#38A169"},
    "greenlands": {"name": "Greenlands", "line": ["Green"], "color": "#38A169"},
    "irrum_manzil_green": {"name": "Irrum Manzil (Green)", "line": ["Green"], "color": "#38A169"},
    "khairatabad_green": {"name": "Khairatabad (Green)", "line": ["Green"], "color": "#38A169"},
    "lakdikapul_green": {"name": "Lakdi Ka Pul (Green)", "line": ["Green"], "color": "#38A169"},
    "assembly_green": {"name": "Assembly (Green)", "line": ["Green"], "color": "#38A169"},
    "nampally_green": {"name": "Nampally (Green)", "line": ["Green"], "color": "#38A169"},
}

# Edges: (station1, station2, distance_in_km, time_in_minutes)
EDGES = [
    # RED LINE
    ("miyapur", "jntu_college", 1.8, 3),
    ("jntu_college", "kphb_colony", 1.2, 2),
    ("kphb_colony", "kukatpally", 1.5, 3),
    ("kukatpally", "balanagar", 2.1, 4),
    ("balanagar", "moosapet", 1.7, 3),
    ("moosapet", "bharat_nagar", 1.3, 2),
    ("bharat_nagar", "erragadda", 1.4, 3),
    ("erragadda", "esp_colony", 1.2, 2),
    ("esp_colony", "sr_nagar", 1.0, 2),
    ("sr_nagar", "ameerpet", 1.5, 3),
    ("ameerpet", "punjagutta", 1.2, 2),
    ("punjagutta", "irrum_manzil", 1.1, 2),
    ("irrum_manzil", "khairatabad", 0.9, 2),
    ("khairatabad", "lakdikapul", 1.1, 2),
    ("lakdikapul", "assembly", 0.8, 2),
    ("assembly", "nampally", 0.9, 2),
    ("nampally", "gandhi_bhavan", 0.7, 2),
    ("gandhi_bhavan", "osmania_medical", 0.8, 2),
    ("osmania_medical", "mg_bus_station", 0.6, 2),
    ("mg_bus_station", "malakpet", 1.3, 3),
    ("malakpet", "new_market", 1.1, 2),
    ("new_market", "musarambagh", 1.2, 2),
    ("musarambagh", "dilsukhnagar", 1.4, 3),
    ("dilsukhnagar", "chaitanyapuri", 1.6, 3),
    ("chaitanyapuri", "victoria_memorial", 1.3, 3),
    ("victoria_memorial", "lb_nagar", 1.5, 3),

    # BLUE LINE
    ("nagole", "uppal", 2.5, 5),
    ("uppal", "stadium", 1.8, 3),
    ("stadium", "ngri", 1.2, 2),
    ("ngri", "habsiguda", 1.3, 3),
    ("habsiguda", "tarnaka", 1.5, 3),
    ("tarnaka", "mettuguda", 1.1, 2),
    ("mettuguda", "secunderabad_east", 1.4, 3),
    ("secunderabad_east", "parade_grounds", 1.0, 2),
    ("parade_grounds", "secunderabad_west", 0.8, 2),
    ("secunderabad_west", "Gandhi_hospital", 1.2, 2),
    ("Gandhi_hospital", "musheerabad", 1.1, 2),
    ("musheerabad", "rsp_south", 0.9, 2),
    ("rsp_south", "chikkadpally", 1.0, 2),
    ("chikkadpally", "narayanaguda", 1.2, 2),
    ("narayanaguda", "sultan_bazar", 0.9, 2),
    ("sultan_bazar", "central_secretariat", 1.1, 2),
    ("central_secretariat", "khairatabad_blue", 1.3, 3),
    ("khairatabad_blue", "imax", 1.0, 2),
    ("imax", "panjagutta_blue", 1.1, 2),
    ("panjagutta_blue", "yousufguda", 1.2, 2),
    ("yousufguda", "road_no5_jubilee_hills", 1.4, 3),
    ("road_no5_jubilee_hills", "jubilee_hills_check_post", 1.0, 2),
    ("jubilee_hills_check_post", "peddamma_temple", 1.3, 3),
    ("peddamma_temple", "madhapur", 1.5, 3),
    ("madhapur", "durgam_cheruvu", 1.2, 2),
    ("durgam_cheruvu", "hitec_city", 1.0, 2),
    ("hitec_city", "raidurg", 1.8, 3),

    # BLUE LINE INTERCHANGE at Ameerpet
    ("ameerpet", "central_secretariat", 2.5, 5),  

    # GREEN LINE
    ("jbs", "parade_grounds_green", 1.5, 3),
    ("parade_grounds_green", "rasoolpura", 1.0, 2),
    ("rasoolpura", "prakash_nagar", 0.8, 2),
    ("prakash_nagar", "begumpet", 1.2, 2),
    ("begumpet", "madhura_nagar", 1.0, 2),
    ("madhura_nagar", "yousufguda_green", 1.1, 2),
    ("yousufguda_green", "greenlands", 0.9, 2),
    ("greenlands", "irrum_manzil_green", 1.2, 2),
    ("irrum_manzil_green", "khairatabad_green", 0.9, 2),
    ("khairatabad_green", "lakdikapul_green", 1.1, 2),
    ("lakdikapul_green", "assembly_green", 0.8, 2),
    ("assembly_green", "nampally_green", 0.9, 2),
    ("nampally_green", "mg_bus_station", 0.6, 2),

    # INTERCHANGE CONNECTIONS
    ("secunderabad_west", "jbs", 0.5, 2),  # Green-Blue interchange
    ("ameerpet", "panjagutta_blue", 0.8, 2),  # Red-Blue interchange at Ameerpet area
]


def build_graph():
    graph = defaultdict(list)
    for s1, s2, dist, time in EDGES:
        graph[s1].append((s2, dist, time))
        graph[s2].append((s1, dist, time))
    return graph


def dijkstra(graph, start, end, weight='time'):
    
    # priority queue: (cost, node, path, time, distance)
    pq = [(0, start, [start], 0, 0.0)]
    visited = {}

    while pq:
        cost, node, path, total_time, total_dist = heapq.heappop(pq)

        if node in visited:
            continue
        visited[node] = cost

        if node == end:
            return cost, path, total_time, total_dist

        for neighbor, dist, time in graph[node]:
            if neighbor not in visited:
                edge_weight = time if weight == 'time' else dist
                new_cost = cost + edge_weight
                new_time = total_time + time
                new_dist = total_dist + dist
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor], new_time, new_dist))

    return None, [], 0, 0.0


def find_shortest_path(source_id, dest_id, optimize='time'):
    """
    Find shortest path between two stations.
    Returns dict with path details.
    """
    if source_id not in STATIONS:
        return {"error": f"Station '{source_id}' not found"}
    if dest_id not in STATIONS:
        return {"error": f"Station '{dest_id}' not found"}
    if source_id == dest_id:
        return {"error": "Source and destination cannot be the same"}

    graph = build_graph()
    cost, path, total_time, total_dist = dijkstra(graph, source_id, dest_id, weight=optimize)

    if not path:
        return {"error": "No path found between the selected stations"}

    # Build step-by-step instructions
    steps = []
    current_line = None
    segment_start = path[0]

    for i in range(1, len(path)):
        prev = path[i - 1]
        curr = path[i]
        prev_lines = set(STATIONS[prev]["line"])
        curr_lines = set(STATIONS[curr]["line"])
        common_lines = prev_lines & curr_lines

        line = list(common_lines)[0] if common_lines else "Interchange"

        if line != current_line:
            if current_line is not None:
                steps.append({
                    "action": "change",
                    "from_line": current_line,
                    "to_line": line,
                    "at_station": STATIONS[prev]["name"]
                })
            current_line = line
            steps.append({
                "action": "board",
                "line": line,
                "at_station": STATIONS[path[i - 1]]["name"]
            })

    steps.append({
        "action": "alight",
        "at_station": STATIONS[dest_id]["name"]
    })

    # Estimate fare (basic: Rs 10 + Rs 3/km)
    fare = round(10 + (total_dist * 3), 0)

    return {
        "source": {"id": source_id, "name": STATIONS[source_id]["name"]},
        "destination": {"id": dest_id, "name": STATIONS[dest_id]["name"]},
        "path": [
            {"id": s, "name": STATIONS[s]["name"], "line": STATIONS[s]["line"]}
            for s in path
        ],
        "total_stations": len(path),
        "total_distance_km": round(total_dist, 2),
        "total_time_minutes": total_time,
        "fare_inr": int(fare),
        "steps": steps,
        "optimized_for": optimize,
    }


def get_all_stations():
    return [
        {"id": sid, "name": data["name"], "line": data["line"]}
        for sid, data in sorted(STATIONS.items(), key=lambda x: x[1]["name"])
    ]
