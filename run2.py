import sys
from collections import deque, defaultdict


def _find_distances_via_bfs(graph, start_node):
    distances = {start_node: 0}
    queue = deque([start_node])

    while queue:
        current_node = queue.popleft()
        for neighbor in sorted(graph.get(current_node, [])):
            if neighbor not in distances:
                distances[neighbor] = distances[current_node] + 1
                queue.append(neighbor)
    return distances


def _determine_virus_target(graph, virus_position, gateways):
    distances_from_virus = _find_distances_via_bfs(graph, virus_position)

    best_target_gateway = None
    min_distance_to_gateway = float('inf')

    for gateway in sorted(gateways):
        if gateway in distances_from_virus:
            distance = distances_from_virus[gateway]
            if distance < min_distance_to_gateway:
                min_distance_to_gateway = distance
                best_target_gateway = gateway

    return best_target_gateway


def _find_critical_link_to_sever(graph, virus_position, target_gateway):
    distances_from_gateway = _find_distances_via_bfs(graph, target_gateway)

    current_path_node = virus_position

    while target_gateway not in graph[current_path_node]:
        best_next_hop = None
        min_dist_to_target = float('inf')

        for neighbor in sorted(graph[current_path_node]):
            if neighbor in distances_from_gateway and distances_from_gateway[neighbor] < min_dist_to_target:
                min_dist_to_target = distances_from_gateway[neighbor]
                best_next_hop = neighbor

        current_path_node = best_next_hop

    return f"{target_gateway}-{current_path_node}"


def _calculate_virus_next_position(graph, virus_position, gateways):
    new_target_gateway = _determine_virus_target(graph, virus_position, gateways)

    if not new_target_gateway:
        return None

    distances_from_new_gateway = _find_distances_via_bfs(graph, new_target_gateway)

    best_next_hop = None
    min_dist_to_target = float('inf')

    for neighbor in sorted(graph[virus_position]):
        if neighbor in distances_from_new_gateway and distances_from_new_gateway[neighbor] < min_dist_to_target:
            min_dist_to_target = distances_from_new_gateway[neighbor]
            best_next_hop = neighbor

    return best_next_hop


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(list)
    gateways = set()
    for node1, node2 in edges:
        graph[node1].append(node2)
        graph[node2].append(node1)
        if node1.isupper(): gateways.add(node1)
        if node2.isupper(): gateways.add(node2)

    virus_position = 'a'
    severed_links = []

    while True:
        target_gateway = _determine_virus_target(graph, virus_position, gateways)

        if target_gateway is None:
            break

        link_to_sever = _find_critical_link_to_sever(graph, virus_position, target_gateway)
        severed_links.append(link_to_sever)

        gateway_node, neighbor_node = link_to_sever.split('-')
        graph[gateway_node].remove(neighbor_node)
        graph[neighbor_node].remove(gateway_node)

        next_pos = _calculate_virus_next_position(graph, virus_position, gateways)
        if next_pos:
            virus_position = next_pos

    return severed_links


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line and '-' in line:
            node1, node2 = line.split('-')
            edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()