from math import atan2, cos, radians, sin, sqrt

from app.models import WasteNode


EARTH_RADIUS_M = 6_371_000


def haversine_m(a: WasteNode, b: WasteNode) -> float:
    lat1 = radians(a.lat)
    lat2 = radians(b.lat)
    delta_lat = radians(b.lat - a.lat)
    delta_lng = radians(b.lng - a.lng)

    h = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lng / 2) ** 2
    return 2 * EARTH_RADIUS_M * atan2(sqrt(h), sqrt(1 - h))


def order_full_nodes(nodes: list[WasteNode]) -> list[WasteNode]:
    remaining = [node for node in nodes if node.is_full]
    if not remaining:
        return []

    ordered = [min(remaining, key=lambda node: (node.lat, node.lng, node.id))]
    remaining.remove(ordered[0])

    while remaining:
        current = ordered[-1]
        next_node = min(remaining, key=lambda node: (haversine_m(current, node), node.id))
        ordered.append(next_node)
        remaining.remove(next_node)

    return ordered


def calculate_route(nodes: list[WasteNode]) -> dict:
    ordered = order_full_nodes(nodes)
    total_distance = sum(haversine_m(a, b) for a, b in zip(ordered, ordered[1:]))

    return {
        "ordered_node_ids": [node.id for node in ordered],
        "path": [(node.lat, node.lng) for node in ordered],
        "total_distance_m": round(total_distance),
    }
