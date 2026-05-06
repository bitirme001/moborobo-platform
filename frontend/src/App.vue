<template>
  <a-layout class="app-shell">
    <a-layout-header class="topbar">
      <div>
        <p class="eyebrow">Moborobo Platform</p>
        <h1>Smart Waste Route Monitor</h1>
      </div>
      <a-space>
        <a-button size="large" @click="loadNodes">Refresh Nodes</a-button>
        <a-button size="large" type="primary" @click="loadRoute">Calculate Route</a-button>
      </a-space>
    </a-layout-header>

    <a-layout class="content-shell">
      <a-layout-content class="map-column">
        <a-card :bordered="false" class="map-card">
          <template #title>Campus Map</template>
          <template #extra>
            <a-tag color="blue">8 Nodes</a-tag>
            <a-tag :color="fullNodes.length ? 'red' : 'green'">
              {{ fullNodes.length }} Full
            </a-tag>
          </template>
          <RouteMap :nodes="nodes" :route-coordinates="routeCoordinates" />
        </a-card>
      </a-layout-content>

      <a-layout-sider class="side-column" width="380">
        <a-space direction="vertical" size="middle" style="width: 100%">
          <a-card :bordered="false" title="Live Status">
            <div class="stats-row">
              <a-statistic title="Total Nodes" :value="nodes.length" />
              <a-statistic title="Full Nodes" :value="fullNodes.length" />
            </div>
            <a-list :data-source="nodes" size="small">
              <template #renderItem="{ item }">
                <a-list-item>
                  <div class="node-row">
                    <div>
                      <strong>{{ item.id }}</strong>
                      <div class="node-name">{{ item.name }}</div>
                    </div>
                    <div class="node-meta">
                      <a-tag :color="item.isFull ? 'red' : 'green'">
                        {{ item.fillPercent }}%
                      </a-tag>
                      <span>{{ item.weightKg }} kg</span>
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
              message="The route line comes from the backend shortest path response."
            />
            <div class="route-summary">
              <div>
                <span class="summary-label">Distance</span>
                <strong>{{ route.total_distance_m ?? 0 }} m</strong>
              </div>
              <div>
                <span class="summary-label">Stops</span>
                <strong>{{ route.ordered_node_ids?.length ?? 0 }}</strong>
              </div>
            </div>
            <a-divider />
            <a-space wrap>
              <a-tag v-for="nodeId in route.ordered_node_ids" :key="nodeId" color="orange">
                {{ nodeId }}
              </a-tag>
            </a-space>
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
import { fetchNodes, fetchRoute } from './services/api'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const nodes = ref([])
const route = ref({
  ordered_node_ids: [],
  path: [],
  total_distance_m: 0
})

const fullNodes = computed(() => nodes.value.filter((node) => node.isFull))
const routeCoordinates = computed(() => route.value.path || [])

async function loadNodes() {
  nodes.value = await fetchNodes()
}

async function loadRoute() {
  route.value = await fetchRoute()
}

onMounted(async () => {
  await loadNodes()
  await loadRoute()
})
</script>
