import sys
from collections import deque


def solve(edges):
    graph = {}
    gateways = set()

    for node1, node2 in edges:
        if node1 not in graph:
            graph[node1] = set()
        if node2 not in graph:
            graph[node2] = set()
        graph[node1].add(node2)
        graph[node2].add(node1)

        if node1.isupper():
            gateways.add(node1)
        if node2.isupper():
            gateways.add(node2)

    virus_pos = 'a'
    result = []

    bfs_cache = {}

    def bfs_from_start(start):
        if start in bfs_cache:
            return bfs_cache[start]

        distances = {}
        prev = {}
        queue = deque([start])
        distances[start] = 0
        prev[start] = None

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    prev[neighbor] = node
                    queue.append(neighbor)

        bfs_cache[start] = (distances, prev)
        return distances, prev

    while True:
        distances, prev = bfs_from_start(virus_pos)

        reachable_gateways = [g for g in gateways if g in distances]
        if not reachable_gateways:
            break

        min_dist = float('inf')
        target_gateway = None
        for gateway in reachable_gateways:
            if distances[gateway] < min_dist or (distances[gateway] == min_dist and gateway < target_gateway):
                min_dist = distances[gateway]
                target_gateway = gateway

        path = []
        node = target_gateway
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()

        if len(path) == 2:
            edge_to_cut = f"{target_gateway}-{virus_pos}"
            if virus_pos in graph[target_gateway]:
                graph[target_gateway].remove(virus_pos)
                graph[virus_pos].remove(target_gateway)
                result.append(edge_to_cut)
            break

        next_node = path[1]

        available_edges = []
        for gateway in sorted(gateways):
            for neighbor in sorted(graph[gateway]):
                available_edges.append(f"{gateway}-{neighbor}")

        edge_to_cut = None
        for edge in available_edges:
            gateway, node_val = edge.split('-')
            if gateway == target_gateway:
                edge_to_cut = edge
                break

        if edge_to_cut is None and available_edges:
            edge_to_cut = available_edges[0]

        if edge_to_cut:
            gateway, node_val = edge_to_cut.split('-')
            graph[gateway].remove(node_val)
            graph[node_val].remove(gateway)
            result.append(edge_to_cut)
            # Инвалидируем кэш
            bfs_cache.clear()

        virus_pos = next_node

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()