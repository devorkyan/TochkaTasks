import sys
from collections import deque, defaultdict


def convert_input():
    graph = defaultdict(list)
    for line in sys.stdin:
        try:
            node1, node2 = line.strip().split('-')
            graph[node1].append(node2)
            graph[node2].append(node1)
        except ValueError:
            continue

    for node in graph:
        graph[node].sort()
    return graph


def find_shortest_path_to_gateway(graph, start_node, end_node):
    queue = deque([(start_node, [start_node])])
    visited = {start_node}

    while queue:
        node, path = queue.popleft()
        if node == end_node:
            return path
        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))
    return None


def find_virus_target_path(graph, virus_pos, gateways):
    best_path = None
    for gw in gateways:
        path = find_shortest_path_to_gateway(graph, virus_pos, gw)
        if path:
            if best_path is None or len(path) < len(best_path):
                best_path = path
    return best_path


def bfs_distances(graph, start_node):
    distances = {start_node: 0}
    queue = deque([start_node])
    while queue:
        node = queue.popleft()
        for neighbour in graph.get(node, []):
            if neighbour not in distances:
                distances[neighbour] = distances[node] + 1
                queue.append(neighbour)
    return distances


def solve():
    virus_position = 'a'
    graph = convert_input()
    gateways = sorted([node for node in graph if node.isupper()])
    closed_gateways = []

    while True:
        distances_from_virus = bfs_distances(graph, virus_position)

        min_dist = float('inf')
        for gw in gateways:
            if gw in distances_from_virus:
                min_dist = min(min_dist, distances_from_virus[gw])

        if min_dist == float('inf'):
            break

        critical_links = []
        for gw in gateways:
            if distances_from_virus.get(gw) == min_dist:
                for neighbour in graph[gw]:
                    if distances_from_virus.get(neighbour) == min_dist - 1:
                        critical_links.append(f"{gw}-{neighbour}")

        if not critical_links:
            break

        link_to_sever = min(critical_links)
        target_gateway, node_to_sever = link_to_sever.split('-')

        closed_gateways.append(link_to_sever)

        graph[node_to_sever].remove(target_gateway)
        graph[target_gateway].remove(node_to_sever)

        next_best_path = find_virus_target_path(graph, virus_position, gateways)

        if next_best_path and len(next_best_path) > 1:
            virus_position = next_best_path[1]

    return closed_gateways


def main():
    result = solve()
    print('\n'.join(result))


if __name__ == "__main__":
    main()