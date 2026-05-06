<template>
  <div ref="mapEl" class="route-map"></div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import L from 'leaflet'

const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  },
  routeCoordinates: {
    type: Array,
    default: () => []
  }
})

const mapEl = ref(null)
let map
let markersLayer
let routeLayer

function markerColor(node) {
  return node.isFull ? '#cf1322' : '#389e0d'
}

function renderNodes() {
  markersLayer.clearLayers()

  props.nodes.forEach((node) => {
    const marker = L.circleMarker([node.lat, node.lng], {
      radius: 10,
      color: '#10239e',
      weight: 2,
      fillColor: markerColor(node),
      fillOpacity: 0.95
    })

    marker
      .bindPopup(`
        <strong>${node.name}</strong><br />
        ${node.id}<br />
        Fill: ${node.fillPercent}%<br />
        Weight: ${node.weightKg} kg
      `)
      .bindTooltip(node.id, {
        permanent: true,
        direction: 'top',
        className: 'node-tooltip'
      })

    marker.addTo(markersLayer)
  })
}

function renderRoute() {
  routeLayer.setLatLngs(props.routeCoordinates)

  const allPoints = [
    ...props.nodes.map((node) => [node.lat, node.lng]),
    ...props.routeCoordinates
  ]

  if (allPoints.length > 0) {
    map.fitBounds(allPoints, { padding: [28, 28] })
  }
}

onMounted(() => {
  map = L.map(mapEl.value, {
    zoomControl: false,
    attributionControl: true
  }).setView([39.8689, 32.7525], 16)

  L.control.zoom({ position: 'topright' }).addTo(map)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map)

  markersLayer = L.layerGroup().addTo(map)
  routeLayer = L.polyline([], {
    color: '#fa8c16',
    weight: 6,
    opacity: 0.85,
    lineJoin: 'round'
  }).addTo(map)

  renderNodes()
  renderRoute()
})

watch(
  () => props.nodes,
  () => {
    if (!map) {
      return
    }
    renderNodes()
    renderRoute()
  },
  { deep: true }
)

watch(
  () => props.routeCoordinates,
  () => {
    if (!map) {
      return
    }
    renderRoute()
  },
  { deep: true }
)

onBeforeUnmount(() => {
  if (map) {
    map.remove()
  }
})
</script>
