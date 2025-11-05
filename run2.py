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

    virus_position = 'a'
    result = []

    def bfs_distances(start):
        distances = {}
        queue = deque([start])
        distances[start] = 0

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        return distances

    def find_next_move(current_pos):
        distances = bfs_distances(current_pos)

        reachable_gateways = [g for g in gateways if g in distances]
        if not reachable_gateways:
            return None

        min_dist = min(distances[g] for g in reachable_gateways)
        candidate_gateways = [g for g in reachable_gateways if distances[g] == min_dist]
        target_gateway = min(candidate_gateways)

        queue = deque([current_pos])
        visited = {current_pos}
        prev = {current_pos: None}

        while queue:
            node = queue.popleft()
            if node == target_gateway:
                break
            neighbors = sorted(graph[node])
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    prev[neighbor] = node
                    queue.append(neighbor)

        path = []
        node = target_gateway
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()

        return path[1] if len(path) > 1 else None

    def get_critical_edge(target_gateway, virus_path):
        gateway_edges = []
        for gateway in sorted(gateways):
            for neighbor in sorted(graph[gateway]):
                gateway_edges.append(f"{gateway}-{neighbor}")

        for edge in gateway_edges:
            gateway, node = edge.split('-')
            if gateway == target_gateway and node in virus_path:
                return edge

        return gateway_edges[0] if gateway_edges else None

    while True:
        next_node = find_next_move(virus_position)
        if next_node is None:
            break

        distances = bfs_distances(virus_position)
        reachable_gateways = [g for g in gateways if g in distances]
        if not reachable_gateways:
            break

        min_dist = min(distances[g] for g in reachable_gateways)
        candidate_gateways = [g for g in reachable_gateways if distances[g] == min_dist]
        target_gateway = min(candidate_gateways)

        virus_path = []
        current = virus_position
        while current != target_gateway:
            virus_path.append(current)
            next_candidates = []
            for neighbor in graph[current]:
                if neighbor not in virus_path:
                    neighbor_dist = bfs_distances(neighbor)
                    if target_gateway in neighbor_dist and neighbor_dist[target_gateway] == distances[target_gateway] - \
                            distances[current]:
                        next_candidates.append(neighbor)
            if not next_candidates:
                break
            current = min(next_candidates)
        virus_path.append(target_gateway)

        edge_to_cut = get_critical_edge(target_gateway, virus_path)
        if edge_to_cut is None:
            break

        gateway, node = edge_to_cut.split('-')
        graph[gateway].remove(node)
        graph[node].remove(gateway)
        result.append(edge_to_cut)

        virus_position = next_node

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