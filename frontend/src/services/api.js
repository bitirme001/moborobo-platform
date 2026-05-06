import { mockNodes, mockRouteResponse } from '../data/mockData'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

async function requestJson(path) {
  const response = await fetch(`${API_BASE_URL}${path}`)
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`)
  }
  return response.json()
}

function normalizeNode(node) {
  return {
    id: node.id ?? node.node_id,
    name: node.name ?? `Node ${node.id ?? node.node_id}`,
    lat: Number(node.lat),
    lng: Number(node.lng),
    weightKg: Number(node.weightKg ?? node.weight_kg ?? node.weight ?? 0),
    fillPercent: Number(node.fillPercent ?? node.fill_percent ?? 0),
    isFull: Boolean(node.isFull ?? node.is_full),
    lastSeen: node.lastSeen ?? node.last_seen ?? null
  }
}

export async function fetchNodes() {
  try {
    const data = await requestJson('/nodes')
    return Array.isArray(data) ? data.map(normalizeNode) : mockNodes
  } catch {
    return mockNodes
  }
}

export async function fetchRoute() {
  try {
    const data = await requestJson('/route')
    if (Array.isArray(data?.path) && Array.isArray(data?.ordered_node_ids)) {
      return data
    }
    return mockRouteResponse
  } catch {
    return mockRouteResponse
  }
}
