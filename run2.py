import sys
from collections import deque, defaultdict

def convert_input():
    graph = defaultdict(list)
    for line in sys.stdin:
        node1, node2 = line.strip().split('-')
        graph[node1].append(node2)
        graph[node2].append(node1)

    for node in graph:
        graph[node].sort()

    return graph

def find_shortest_path_to_gateway(graph, start_node, end_node):

    visited = set(start_node)
    queue = deque(
        [
            (start_node, [start_node])
        ]
    )

    while queue:
        node, path = queue.popleft()
        if node == end_node:
            return path

        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)

                new_path = list(path)
                new_path.append(neighbour)
                queue.append((neighbour, new_path))

    return None

def find_virus_target_path(graph, virus_pos, gateways):
    best_path = None
    for gw in gateways:
        path = find_shortest_path_to_gateway(graph, virus_pos, gw)
        if path:
            if best_path is None or len(path) < len(best_path):
                best_path = path
    return best_path

def solve():
    virus_position = 'a'
    graph = convert_input()
    gateways = sorted([node for node in graph if node.isupper()])

    closed_gateways = []
    while True:
        best_path = find_virus_target_path(graph, virus_position, gateways)
        if not best_path:
            break

        target_gateway = best_path[-1]
        node_to_sever_with_gateway = best_path[-2]

        closed_gateways.append(f"{target_gateway}-{node_to_sever_with_gateway}")

        graph[node_to_sever_with_gateway].remove(target_gateway)
        graph[target_gateway].remove(node_to_sever_with_gateway)

        next_best_path = find_virus_target_path(graph, virus_position, gateways)

        if next_best_path and len(next_best_path) > 1:
            virus_position = next_best_path[1]

    return closed_gateways

def main():
    result = solve()
    print('\n'.join(result))

if __name__ == "__main__":
    main()