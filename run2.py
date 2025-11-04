import sys
from collections import deque


def solve(edges):
    graph = {}
    gateways = set()
    regular_nodes = set()

    for node1, node2 in edges:
        if node1 not in graph:
            graph[node1] = set()
        if node2 not in graph:
            graph[node2] = set()
        graph[node1].add(node2)
        graph[node2].add(node1)

        if node1.isupper():
            gateways.add(node1)
            regular_nodes.add(node2)
        elif node2.isupper():
            gateways.add(node2)
            regular_nodes.add(node1)
        else:
            regular_nodes.add(node1)
            regular_nodes.add(node2)

    virus_position = 'a'
    result = []

    def find_target_gateway_and_path(current_pos):
        distances = {}
        previous = {}
        queue = deque([current_pos])
        distances[current_pos] = 0
        previous[current_pos] = None

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    previous[neighbor] = node
                    queue.append(neighbor)

        reachable_gateways = [g for g in gateways if g in distances]
        if not reachable_gateways:
            return None, None

        closest_distance = min(distances[g] for g in reachable_gateways)
        candidate_gateways = [g for g in reachable_gateways if distances[g] == closest_distance]
        target_gateway = min(candidate_gateways)

        path = []
        current = target_gateway
        while current != current_pos:
            path.append(current)
            current = previous[current]
        path.append(current_pos)
        path.reverse()

        return target_gateway, path

    def get_available_gate_edges():
        gate_edges = []
        for gateway in gateways:
            for neighbor in graph[gateway]:
                if neighbor in regular_nodes:
                    gate_edges.append(f"{gateway}-{neighbor}")
        return sorted(gate_edges)

    while True:
        target_gateway, path = find_target_gateway_and_path(virus_position)
        if target_gateway is None:
            break

        if len(path) == 2:
            edge_to_cut = f"{target_gateway}-{virus_position}"
            if edge_to_cut in graph[target_gateway] and edge_to_cut in graph[virus_position]:
                graph[target_gateway].remove(virus_position)
                graph[virus_position].remove(target_gateway)
                result.append(edge_to_cut)
            continue

        next_node = path[1]

        available_edges = get_available_gate_edges()

        edge_found = False
        for edge in available_edges:
            gateway, node = edge.split('-')
            if gateway == target_gateway and node in path:
                graph[gateway].remove(node)
                graph[node].remove(gateway)
                result.append(edge)
                edge_found = True
                break

        if not edge_found:
            for edge in available_edges:
                gateway, node = edge.split('-')
                graph[gateway].remove(node)
                graph[node].remove(gateway)
                result.append(edge)
                edge_found = True
                break

        if not edge_found:
            break

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