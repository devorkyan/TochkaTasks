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

    def bfs_to_find_target_and_path():
        distances = {}
        prev = {}
        queue = deque([virus_pos])
        distances[virus_pos] = 0
        prev[virus_pos] = None

        while queue:
            node = queue.popleft()
            for neighbor in sorted(graph[node]):
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    prev[neighbor] = node
                    queue.append(neighbor)

        reachable_gateways = [g for g in gateways if g in distances]
        if not reachable_gateways:
            return None, None

        min_dist = min(distances[g] for g in reachable_gateways)
        candidate_gateways = sorted([g for g in reachable_gateways if distances[g] == min_dist])
        target_gateway = candidate_gateways[0]

        path = []
        node = target_gateway
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()

        return target_gateway, path

    while True:
        target_gateway, path = bfs_to_find_target_and_path()
        if target_gateway is None:
            break

        if len(path) == 2:
            edge_to_cut = f"{target_gateway}-{virus_pos}"
            if edge_to_cut in graph[target_gateway]:
                graph[target_gateway].remove(virus_pos)
                graph[virus_pos].remove(target_gateway)
                result.append(edge_to_cut)
                break
            continue

        next_node = path[1]

        available_edges = []
        for gateway in sorted(gateways):
            for neighbor in sorted(graph[gateway]):
                available_edges.append(f"{gateway}-{neighbor}")

        edge_to_cut = None
        for edge in available_edges:
            gateway, node = edge.split('-')
            if gateway == target_gateway and node in path:
                edge_to_cut = edge
                break

        if edge_to_cut is None and available_edges:
            edge_to_cut = available_edges[0]

        if edge_to_cut:
            gateway, node = edge_to_cut.split('-')
            graph[gateway].remove(node)
            graph[node].remove(gateway)
            result.append(edge_to_cut)

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