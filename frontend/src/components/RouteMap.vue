<template>
  <div class="route-map">
    <div class="route-map__stage">
      <div class="route-map__canvas">
        <img
          :src="mapImage"
          alt="Campus route map"
          class="route-map__image"
          @load="handleImageLoad"
        />

        <svg
          class="route-map__overlay"
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          <polyline
            v-if="routePolylinePoints.length > 1"
            :points="routePolyline"
            class="route-map__route-shadow"
          />
          <polyline
            v-if="routePolylinePoints.length > 1"
            :points="routePolyline"
            class="route-map__route-line"
          />
        </svg>

        <div
          v-for="node in visualNodes"
          :key="node.id"
          class="route-map__node"
          :style="{
            left: `${node.position.x}%`,
            top: `${node.position.y}%`
          }"
          :title="`${node.name} (${node.id}) • Fill ${node.fillPercent}% • Weight ${node.weightKg} kg`"
        >
          <span
            class="route-map__node-dot"
            :class="{
              'route-map__node-dot--full': node.isFull,
              'route-map__node-dot--path': routeNodeLookup.has(node.id)
            }"
          >
            {{ node.id }}
          </span>
        </div>
      </div>

      <div class="route-map__legend">
        <div class="route-map__legend-title">YAML Overlay</div>
        <div class="route-map__legend-item">
          <span class="route-map__legend-swatch route-map__legend-swatch--route"></span>
          Yellow route
        </div>
        <div class="route-map__legend-item">
          <span class="route-map__legend-swatch route-map__legend-swatch--full"></span>
          Alarm node
        </div>
        <div class="route-map__legend-item">
          <span class="route-map__legend-swatch route-map__legend-swatch--normal"></span>
          Normal node
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  },
  routeCoordinates: {
    type: Array,
    default: () => []
  },
  routeNodeIds: {
    type: Array,
    default: () => []
  }
})

const mapImage = '/sunum_map.png'
const mapMetadata = ref(null)
const mapWaypoints = ref([])
const imageSize = ref(null)
const occupancyGrid = ref(null)
const SEGMENT_GUIDE_POINTS = {
  'N6->N3': [
    [190, 565],
    [190, 515]
  ]
}

function handleImageLoad(event) {
  const imageElement = event.target

  imageSize.value = {
    width: imageElement.naturalWidth,
    height: imageElement.naturalHeight
  }

  const canvas = document.createElement('canvas')
  canvas.width = imageElement.naturalWidth
  canvas.height = imageElement.naturalHeight

  const context = canvas.getContext('2d', { willReadFrequently: true })

  if (!context) {
    occupancyGrid.value = null
    return
  }

  context.drawImage(imageElement, 0, 0)

  const { data } = context.getImageData(0, 0, canvas.width, canvas.height)
  const walkable = new Uint8Array(canvas.width * canvas.height)

  for (let index = 0; index < walkable.length; index += 1) {
    walkable[index] = data[index * 4] >= 240 ? 1 : 0
  }

  occupancyGrid.value = {
    width: canvas.width,
    height: canvas.height,
    walkable
  }
}

function compactNodeIds(nodeIds) {
  return nodeIds.filter((nodeId, index) => nodeId && nodeId !== nodeIds[index - 1])
}

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max)
}

function parseMapYaml(text) {
  const resolutionMatch = text.match(/^resolution:\s*([-\d.]+)/m)
  const originMatch = text.match(/^origin:\s*\[([^\]]+)\]/m)

  return {
    resolution: Number(resolutionMatch?.[1] ?? 0.05),
    origin: originMatch
      ? originMatch[1].split(',').map((value) => Number(value.trim()))
      : [0, 0, 0]
  }
}

function parseWaypointsYaml(text) {
  const waypointRegex =
    /-\s+id:\s*([^\n]+)\s*\n\s*name:\s*["']?([^"\n]+)["']?\s*\n\s*x:\s*([-\d.]+)\s*\n\s*y:\s*([-\d.]+)\s*\n\s*yaw:\s*([-\d.]+)\s*\n\s*active:\s*(true|false)/g

  const parsedWaypoints = []
  let match

  while ((match = waypointRegex.exec(text)) !== null) {
    parsedWaypoints.push({
      id: match[1].trim(),
      name: match[2].trim(),
      x: Number(match[3]),
      y: Number(match[4]),
      yaw: Number(match[5]),
      active: match[6] === 'true'
    })
  }

  return parsedWaypoints
}

async function loadMapFiles() {
  try {
    const [mapResponse, waypointResponse] = await Promise.all([
      fetch('/sunum_map.yaml'),
      fetch('/waypoints.yaml')
    ])

    const [mapYaml, waypointYaml] = await Promise.all([
      mapResponse.text(),
      waypointResponse.text()
    ])

    mapMetadata.value = parseMapYaml(mapYaml)
    mapWaypoints.value = parseWaypointsYaml(waypointYaml)
  } catch (error) {
    console.error('Failed to load map metadata', error)
  }
}

onMounted(() => {
  loadMapFiles()
})

const waypointPixelLookup = computed(() => {
  if (!mapMetadata.value || !imageSize.value) {
    return new Map()
  }

  const [originX, originY] = mapMetadata.value.origin
  const { resolution } = mapMetadata.value
  const { width, height } = imageSize.value

  return new Map(
    mapWaypoints.value.map((waypoint) => {
      const pixelX = (waypoint.x - originX) / resolution
      const pixelY = height - (waypoint.y - originY) / resolution

      return [
        waypoint.id,
        {
          pixelX,
          pixelY,
          x: clamp((pixelX / width) * 100, 0, 100),
          y: clamp((pixelY / height) * 100, 0, 100)
        }
      ]
    })
  )
})

function resolveWaypointId(nodeId) {
  const numericSuffix = String(nodeId).match(/(\d+)$/)

  if (!numericSuffix) {
    return nodeId
  }

  return `bin_${numericSuffix[1]}`
}

function resolvePositionForNodeId(nodeId) {
  return waypointPixelLookup.value.get(resolveWaypointId(nodeId)) ?? null
}

function createPixelPoint(x, y) {
  if (!imageSize.value) {
    return null
  }

  return {
    pixelX: x,
    pixelY: y,
    x: clamp((x / imageSize.value.width) * 100, 0, 100),
    y: clamp((y / imageSize.value.height) * 100, 0, 100)
  }
}

function findNearestWalkablePoint(point, maxRadius = 32) {
  if (!occupancyGrid.value || !point) {
    return point
  }

  const { width, height, walkable } = occupancyGrid.value
  const startX = Math.round(point.pixelX)
  const startY = Math.round(point.pixelY)

  const isWalkable = (x, y) => walkable[y * width + x] === 1

  if (
    startX >= 0 &&
    startY >= 0 &&
    startX < width &&
    startY < height &&
    isWalkable(startX, startY)
  ) {
    return createPixelPoint(startX, startY)
  }

  for (let radius = 1; radius <= maxRadius; radius += 1) {
    let bestCandidate = null

    for (let offsetY = -radius; offsetY <= radius; offsetY += 1) {
      for (let offsetX = -radius; offsetX <= radius; offsetX += 1) {
        if (Math.abs(offsetX) !== radius && Math.abs(offsetY) !== radius) {
          continue
        }

        const x = startX + offsetX
        const y = startY + offsetY

        if (x < 0 || y < 0 || x >= width || y >= height || !isWalkable(x, y)) {
          continue
        }

        const distance = offsetX * offsetX + offsetY * offsetY

        if (!bestCandidate || distance < bestCandidate.distance) {
          bestCandidate = { x, y, distance }
        }
      }
    }

    if (bestCandidate) {
      return createPixelPoint(bestCandidate.x, bestCandidate.y)
    }
  }

  return point
}

function resolveSegmentGuidePoints(fromNodeId, toNodeId) {
  const guidePoints = SEGMENT_GUIDE_POINTS[`${fromNodeId}->${toNodeId}`] ?? []

  return guidePoints
    .map(([pixelX, pixelY]) => createPixelPoint(pixelX, pixelY))
    .filter(Boolean)
}

function traceWalkablePath(startPoint, endPoint) {
  if (!occupancyGrid.value || !startPoint || !endPoint) {
    return [startPoint, endPoint].filter(Boolean)
  }

  const snappedStart = findNearestWalkablePoint(startPoint)
  const snappedEnd = findNearestWalkablePoint(endPoint)

  if (!snappedStart || !snappedEnd) {
    return [startPoint, endPoint].filter(Boolean)
  }

  const { width, height, walkable } = occupancyGrid.value
  const toIndex = (x, y) => y * width + x
  const startIndex = toIndex(Math.round(snappedStart.pixelX), Math.round(snappedStart.pixelY))
  const endIndex = toIndex(Math.round(snappedEnd.pixelX), Math.round(snappedEnd.pixelY))
  const previous = new Int32Array(width * height)

  previous.fill(-1)
  previous[startIndex] = startIndex

  const queue = new Int32Array(width * height)
  let head = 0
  let tail = 0

  queue[tail] = startIndex
  tail += 1

  while (head < tail) {
    const currentIndex = queue[head]
    head += 1

    if (currentIndex === endIndex) {
      break
    }

    const x = currentIndex % width
    const y = Math.floor(currentIndex / width)
    const neighbors = [
      [x, y - 1],
      [x + 1, y],
      [x, y + 1],
      [x - 1, y]
    ]

    for (const [neighborX, neighborY] of neighbors) {
      if (neighborX < 0 || neighborY < 0 || neighborX >= width || neighborY >= height) {
        continue
      }

      const neighborIndex = toIndex(neighborX, neighborY)

      if (walkable[neighborIndex] !== 1 || previous[neighborIndex] !== -1) {
        continue
      }

      previous[neighborIndex] = currentIndex
      queue[tail] = neighborIndex
      tail += 1
    }
  }

  if (previous[endIndex] === -1) {
    return [snappedStart, snappedEnd]
  }

  const pixelPath = []
  let cursor = endIndex

  while (cursor !== startIndex) {
    pixelPath.push(createPixelPoint(cursor % width, Math.floor(cursor / width)))
    cursor = previous[cursor]
  }

  pixelPath.push(createPixelPoint(snappedStart.pixelX, snappedStart.pixelY))
  pixelPath.reverse()

  return pixelPath
}

function simplifyWalkablePath(pixelPath) {
  if (pixelPath.length <= 2) {
    return pixelPath
  }

  const simplifiedPath = [pixelPath[0]]

  for (let index = 1; index < pixelPath.length - 1; index += 1) {
    const previousPoint = pixelPath[index - 1]
    const currentPoint = pixelPath[index]
    const nextPoint = pixelPath[index + 1]
    const directionX = Math.sign(currentPoint.pixelX - previousPoint.pixelX)
    const directionY = Math.sign(currentPoint.pixelY - previousPoint.pixelY)
    const nextDirectionX = Math.sign(nextPoint.pixelX - currentPoint.pixelX)
    const nextDirectionY = Math.sign(nextPoint.pixelY - currentPoint.pixelY)

    if (directionX !== nextDirectionX || directionY !== nextDirectionY) {
      simplifiedPath.push(currentPoint)
    }
  }

  simplifiedPath.push(pixelPath[pixelPath.length - 1])

  return simplifiedPath
}

function resolveClosestNodeId(coordinate) {
  if (!Array.isArray(coordinate) || coordinate.length < 2 || props.nodes.length === 0) {
    return null
  }

  const [lat, lng] = coordinate.map(Number)
  let bestMatch = null

  props.nodes.forEach((node) => {
    const distance = Math.hypot(node.lat - lat, node.lng - lng)

    if (!bestMatch || distance < bestMatch.distance) {
      bestMatch = { id: node.id, distance }
    }
  })

  return bestMatch && bestMatch.distance < 0.003 ? bestMatch.id : null
}

const coordinateRouteNodeIds = computed(() =>
  compactNodeIds(props.routeCoordinates.map((coordinate) => resolveClosestNodeId(coordinate)))
)

const routeNodeIds = computed(() => {
  const preferredNodeIds =
    coordinateRouteNodeIds.value.length > 0
      ? coordinateRouteNodeIds.value
      : compactNodeIds(props.routeNodeIds)

  return preferredNodeIds.filter((nodeId) => resolvePositionForNodeId(nodeId))
})

const routePolylinePoints = computed(() =>
  routeNodeIds.value.reduce((pathPoints, nodeId, index) => {
    const currentPoint = resolvePositionForNodeId(nodeId)

    if (!currentPoint) {
      return pathPoints
    }

    if (index === 0) {
      return [currentPoint]
    }

    const previousNodeId = routeNodeIds.value[index - 1]
    const previousPoint = resolvePositionForNodeId(previousNodeId)

    if (!previousPoint) {
      return pathPoints
    }

    const segmentStops = [
      previousPoint,
      ...resolveSegmentGuidePoints(previousNodeId, nodeId),
      currentPoint
    ]

    const segmentPath = segmentStops.reduce((points, point, stopIndex) => {
      if (stopIndex === 0) {
        return [point]
      }

      const tracedPath = simplifyWalkablePath(
        traceWalkablePath(segmentStops[stopIndex - 1], point)
      )

      if (tracedPath.length === 0) {
        return points
      }

      if (points.length === 0) {
        return tracedPath
      }

      return [...points, ...tracedPath.slice(1)]
    }, [])

    if (segmentPath.length === 0) {
      return pathPoints
    }

    if (pathPoints.length === 0) {
      return segmentPath
    }

    return [...pathPoints, ...segmentPath.slice(1)]
  }, [])
)

const routePolyline = computed(() =>
  routePolylinePoints.value.map((point) => `${point.x},${point.y}`).join(' ')
)

const routeNodeLookup = computed(() => new Set(routeNodeIds.value))

const visualNodes = computed(() =>
  props.nodes
    .map((node) => ({
      ...node,
      position: resolvePositionForNodeId(node.id)
    }))
    .filter((node) => node.position)
)
</script>
