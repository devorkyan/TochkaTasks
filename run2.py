import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(list)
    gateways = set()
    for node1, node2 in edges:
        graph[node1].append(node2)
        graph[node2].append(node1)
        if node1.isupper(): gateways.add(node1)
        if node2.isupper(): gateways.add(node2)

    for node in graph:
        graph[node].sort()

    virus_position = 'a'
    severed_links = []

    sorted_gateways = sorted(list(gateways))

    while True:
        # --- Ход игрока: найти и отключить коридор (1 BFS) ---
        dist_from_virus = {virus_position: 0}
        queue = deque([virus_position])
        head = 0
        while head < len(queue):
            u = queue[head];
            head += 1
            for v in graph[u]:
                if v not in dist_from_virus:
                    dist_from_virus[v] = dist_from_virus[u] + 1
                    queue.append(v)

        target_gateway = None
        min_dist = float('inf')
        for gw in sorted_gateways:
            dist = dist_from_virus.get(gw, float('inf'))
            if dist < min_dist:
                min_dist = dist
                target_gateway = gw

        if target_gateway is None:
            break

        node_to_sever_from = ""
        for neighbor in graph[target_gateway]:
            if dist_from_virus.get(neighbor) == min_dist - 1:
                node_to_sever_from = neighbor
                break

        link_to_sever_str = f"{target_gateway}-{node_to_sever_from}"
        severed_links.append(link_to_sever_str)
        graph[target_gateway].remove(node_to_sever_from)
        graph[node_to_sever_from].remove(target_gateway)

        # --- Ход вируса: перемещение в измененной сети (2 BFS) ---
        dist_from_virus_after_cut = {virus_position: 0}
        queue = deque([virus_position])
        head = 0
        while head < len(queue):
            u = queue[head];
            head += 1
            for v in graph[u]:
                if v not in dist_from_virus_after_cut:
                    dist_from_virus_after_cut[v] = dist_from_virus_after_cut[u] + 1
                    queue.append(v)

        new_target = None
        min_dist = float('inf')
        for gw in sorted_gateways:
            dist = dist_from_virus_after_cut.get(gw, float('inf'))
            if dist < min_dist:
                min_dist = dist
                new_target = gw

        if new_target is None:
            continue

        dist_from_new_target = {new_target: 0}
        queue = deque([new_target])
        head = 0
        while head < len(queue):
            u = queue[head];
            head += 1
            for v in graph[u]:
                if v not in dist_from_new_target:
                    dist_from_new_target[v] = dist_from_new_target[u] + 1
                    queue.append(v)

        next_virus_pos = None
        current_dist_to_target = dist_from_new_target.get(virus_position, float('inf'))
        if current_dist_to_target != float('inf'):
            for neighbor in graph[virus_position]:
                if dist_from_new_target.get(neighbor) == current_dist_to_target - 1:
                    next_virus_pos = neighbor
                    break

        if next_virus_pos:
            virus_position = next_virus_pos

    return severed_links


def main():
    edges = []
    try:
        for line in sys.stdin:
            line = line.strip()
            if line and '-' in line:
                node1, node2 = line.split('-')
                edges.append((node1, node2))
    except (IOError, BrokenPipeError):
        pass

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()