<template>
  <a-layout class="app-shell">
    <a-layout-header class="topbar">
      <div>
        <p class="eyebrow">Moborobo Platform</p>
        <h1>Smart Waste Route Monitor</h1>
      </div>
    </a-layout-header>

    <a-layout class="content-shell">
      <a-layout-content class="map-column">
        <a-card :bordered="false" class="map-card">
          <template #title>Campus Map</template>
          <template #extra>
            <a-tag color="blue">{{ displayNodes.length }} Nodes</a-tag>
            <a-tag :color="fullNodes.length ? 'red' : 'green'">
              {{ fullNodes.length }} Full
            </a-tag>
          </template>
          <RouteMap
            :nodes="displayNodes"
            :route-coordinates="displayRoute.path"
            :route-node-ids="displayRoute.ordered_node_ids"
          />
        </a-card>
      </a-layout-content>

      <a-layout-sider class="side-column" width="380">
        <a-space direction="vertical" size="middle" style="width: 100%">
          <a-card :bordered="false" title="Live Status">
            <div class="stats-row">
              <a-statistic title="Total Nodes" :value="displayNodes.length" />
              <a-statistic title="Full Nodes" :value="fullNodes.length" />
            </div>
            <a-list :data-source="displayNodes" size="small">
              <template #renderItem="{ item }">
                <a-list-item>
                  <div class="node-row">
                    <strong>{{ item.id }}</strong>
                    <div class="node-meta">
                      <a-tag :color="item.isFull ? 'red' : 'green'">
                        {{ item.fillPercent }}%
                      </a-tag>
                      <span>{{ formatWeight(item.weightKg) }} / 20 kg</span>
                    </div>
                  </div>
                </a-list-item>
              </template>
            </a-list>
          </a-card>

          <a-card :bordered="false" title="Route Summary">
            <a-alert
              type="info"
              show-icon
              message="Manual route order is fixed as 4 → 6 → 3 → 2 and the yellow line follows the open corridors on the YAML map."
            />
            <div class="route-summary">
              <div>
                <span class="summary-label">Stops</span>
                <strong>{{ displayRoute.ordered_node_ids?.length ?? 0 }}</strong>
              </div>
              <div>
                <span class="summary-label">Nodes</span>
                <strong>{{ displayRoute.ordered_node_ids.join(' - ') }}</strong>
              </div>
            </div>
          </a-card>

          <a-card :bordered="false" title="Backend Status">
            <p class="muted">
              API base: <code>{{ apiBaseUrl }}</code>
            </p>
            <p class="muted">
              If FastAPI is not running yet, the UI uses mock nodes and a mock route so the map can still be designed now.
            </p>
          </a-card>
        </a-space>
      </a-layout-sider>
    </a-layout>
  </a-layout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import RouteMap from './components/RouteMap.vue'
import { fetchNodes } from './services/api'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const VISIBLE_NODE_IDS = new Set(['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7'])
const MANUAL_ROUTE_NODE_IDS = ['N4', 'N6', 'N3', 'N2']
const manualRouteNodeLookup = new Set(MANUAL_ROUTE_NODE_IDS)
const nodes = ref([])
const displayNodes = computed(() =>
  nodes.value
    .filter((node) => VISIBLE_NODE_IDS.has(node.id))
    .map((node) => ({
      ...node,
      isFull: manualRouteNodeLookup.has(node.id)
    }))
)
const fullNodes = computed(() => displayNodes.value.filter((node) => node.isFull))

function formatWeight(weightKg) {
  return Math.min(Number(weightKg) || 0, 20).toFixed(1)
}

function haversineDistanceMeters([lat1, lng1], [lat2, lng2]) {
  const earthRadiusMeters = 6371000
  const toRadians = (degrees) => (degrees * Math.PI) / 180
  const deltaLat = toRadians(lat2 - lat1)
  const deltaLng = toRadians(lng2 - lng1)
  const startLat = toRadians(lat1)
  const endLat = toRadians(lat2)
  const haversine =
    Math.sin(deltaLat / 2) ** 2 +
    Math.cos(startLat) * Math.cos(endLat) * Math.sin(deltaLng / 2) ** 2

  return 2 * earthRadiusMeters * Math.asin(Math.sqrt(haversine))
}

const displayRoute = computed(() => {
  const orderedNodes = MANUAL_ROUTE_NODE_IDS.map((nodeId) =>
    displayNodes.value.find((node) => node.id === nodeId)
  ).filter(Boolean)
  const path = orderedNodes.map((node) => [node.lat, node.lng])
  const totalDistanceMeters = path.slice(1).reduce((distance, point, index) => {
    return distance + haversineDistanceMeters(path[index], point)
  }, 0)

  return {
    ordered_node_ids: orderedNodes.map((node) => node.id),
    path,
    total_distance_m: Math.round(totalDistanceMeters)
  }
})

async function loadNodes() {
  nodes.value = await fetchNodes()
}

onMounted(async () => {
  await loadNodes()
})
</script>
