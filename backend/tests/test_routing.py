from app.models import WasteNode
from app.services.routing import calculate_route


def make_node(node_id: str, lat: float, lng: float, is_full: bool = True) -> WasteNode:
    return WasteNode(
        id=node_id,
        name=node_id,
        lat=lat,
        lng=lng,
        weight_kg=1,
        fill_percent=90 if is_full else 20,
        is_full=is_full,
    )


def test_calculate_route_ignores_non_full_nodes() -> None:
    route = calculate_route(
        [
            make_node("N2", 39.86834, 32.75008),
            make_node("N1", 39.86782, 32.74894, is_full=False),
            make_node("N5", 39.87021, 32.75361),
        ]
    )

    assert route["ordered_node_ids"] == ["N2", "N5"]
    assert route["path"] == [(39.86834, 32.75008), (39.87021, 32.75361)]
    assert route["total_distance_m"] > 0


def test_calculate_route_returns_empty_route_when_no_nodes_are_full() -> None:
    route = calculate_route([make_node("N1", 39.86782, 32.74894, is_full=False)])

    assert route == {"ordered_node_ids": [], "path": [], "total_distance_m": 0}
