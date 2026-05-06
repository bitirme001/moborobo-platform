# Initial API Contract

## `GET /nodes`
Returns all known garbage nodes.

```json
[
  {
    "id": "N1",
    "name": "Library",
    "lat": 39.8721,
    "lng": 32.7352,
    "weightKg": 18.4,
    "fillPercent": 56,
    "isFull": false,
    "lastSeen": "2026-05-06T18:20:00Z"
  }
]
```

## `GET /route`
Returns the ordered shortest path for the currently full nodes.

```json
{
  "ordered_node_ids": ["N2", "N5", "N7"],
  "path": [
    [39.8726, 32.7344],
    [39.8734, 32.7359],
    [39.8741, 32.7372]
  ],
  "total_distance_m": 940
}
```
