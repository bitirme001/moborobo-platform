export const mockNodes = [
  {
    id: 'N1',
    name: 'Engineering Gate',
    lat: 39.86782,
    lng: 32.74894,
    weightKg: 12.4,
    fillPercent: 41,
    isFull: false,
    lastSeen: '2026-05-06T17:42:00Z'
  },
  {
    id: 'N2',
    name: 'Library Square',
    lat: 39.86834,
    lng: 32.75008,
    weightKg: 24.9,
    fillPercent: 91,
    isFull: true,
    lastSeen: '2026-05-06T17:44:00Z'
  },
  {
    id: 'N3',
    name: 'Cafeteria North',
    lat: 39.86911,
    lng: 32.75136,
    weightKg: 16.8,
    fillPercent: 57,
    isFull: false,
    lastSeen: '2026-05-06T17:46:00Z'
  },
  {
    id: 'N4',
    name: 'Dorm Entrance',
    lat: 39.86976,
    lng: 32.75221,
    weightKg: 14.2,
    fillPercent: 38,
    isFull: false,
    lastSeen: '2026-05-06T17:49:00Z'
  },
  {
    id: 'N5',
    name: 'Lab Block A',
    lat: 39.87021,
    lng: 32.75361,
    weightKg: 27.3,
    fillPercent: 95,
    isFull: true,
    lastSeen: '2026-05-06T17:50:00Z'
  },
  {
    id: 'N6',
    name: 'Admin Garden',
    lat: 39.86948,
    lng: 32.75492,
    weightKg: 10.6,
    fillPercent: 29,
    isFull: false,
    lastSeen: '2026-05-06T17:53:00Z'
  },
  {
    id: 'N7',
    name: 'Sports Hall',
    lat: 39.86877,
    lng: 32.75584,
    weightKg: 26.1,
    fillPercent: 89,
    isFull: true,
    lastSeen: '2026-05-06T17:56:00Z'
  },
  {
    id: 'N8',
    name: 'Student Center',
    lat: 39.86794,
    lng: 32.75448,
    weightKg: 11.3,
    fillPercent: 34,
    isFull: false,
    lastSeen: '2026-05-06T17:58:00Z'
  }
]

export const mockRouteResponse = {
  ordered_node_ids: ['N2', 'N5', 'N7'],
  path: [
    [39.86834, 32.75008],
    [39.86911, 32.75136],
    [39.87021, 32.75361],
    [39.86948, 32.75492],
    [39.86877, 32.75584]
  ],
  total_distance_m: 640
}
