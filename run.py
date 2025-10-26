import sys
import heapq
import itertools

ENERGY_COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
TARGET_ROOM_FOR = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
ROOM_ENTRANCES = (2, 4, 6, 8)
HALLWAY_STOPS = frozenset({0, 1, 3, 5, 7, 9, 10})

def solve(input_lines: list[str]) -> int:
    def parse_layout(input_lines: list[str]):
        hallway = tuple([None] * 11)
        room_depth = len(input_lines) - 3
        room_columns = [[line[3 + 2 * i] for line in input_lines[2:-1]] for i in range(4)]
        return (hallway, tuple(map(tuple, room_columns))), room_depth

    def get_solved_layout(room_depth: int):
        return (tuple([None] * 11), tuple(tuple([owner] * room_depth) for owner in "ABCD"))

    def get_possible_moves(layout, room_depth):
        hallway, rooms = layout
        for hall_pos, mover in enumerate(hallway):
            if not mover: continue
            room_idx = TARGET_ROOM_FOR[mover]
            if any(occupant and occupant != mover for occupant in rooms[room_idx]): continue
            dest_entrance = ROOM_ENTRANCES[room_idx]
            start, end = min(hall_pos, dest_entrance), max(hall_pos, dest_entrance)
            if any(hallway[i] for i in range(start, end + 1) if i != hall_pos): continue
            dest_depth = next((i for i in range(room_depth - 1, -1, -1) if rooms[room_idx][i] is None), -1)

            distance = abs(hall_pos - dest_entrance) + (dest_depth + 1)
            move_energy = distance * ENERGY_COST[mover]

            new_hallway, new_rooms = list(hallway), [list(r) for r in rooms]
            new_hallway[hall_pos], new_rooms[room_idx][dest_depth] = None, mover
            yield move_energy, (tuple(new_hallway), tuple(map(tuple, new_rooms)))
            return

        for room_idx, room in enumerate(rooms):
            if all(occupant is None or TARGET_ROOM_FOR.get(occupant) == room_idx for occupant in room): continue
            source_depth, mover = next(((i, occupant) for i, occupant in enumerate(room) if occupant), (None, None))
            if mover is None: continue

            source_entrance = ROOM_ENTRANCES[room_idx]
            for hall_stop in HALLWAY_STOPS:
                start, end = min(source_entrance, hall_stop), max(source_entrance, hall_stop)
                if any(hallway[i] for i in range(start, end + 1)): continue

                distance = (source_depth + 1) + abs(hall_stop - source_entrance)
                move_energy = distance * ENERGY_COST[mover]

                new_hallway, new_rooms = list(hallway), [list(r) for r in rooms]
                new_hallway[hall_stop], new_rooms[room_idx][source_depth] = mover, None
                yield move_energy, (tuple(new_hallway), tuple(map(tuple, new_rooms)))


    initial_layout, room_depth = parse_layout(input_lines)
    target_layout = get_solved_layout(room_depth)

    tie_breaker = itertools.count()
    queue = [(0, next(tie_breaker), initial_layout)]
    min_energy_map = {initial_layout: 0}

    while queue:
        current_energy, _, current_layout = heapq.heappop(queue)
        if current_layout == target_layout: return current_energy
        if current_energy > min_energy_map.get(current_layout, float('inf')): continue

        for move_energy, next_layout in get_possible_moves(current_layout, room_depth):
            new_energy = current_energy + move_energy
            if new_energy < min_energy_map.get(next_layout, float('inf')):
                min_energy_map[next_layout] = new_energy
                heapq.heappush(queue, (new_energy, next(tie_breaker), next_layout))
    return -1

def main():
    input_lines = [line.rstrip('\n') for line in sys.stdin]
    print(solve(input_lines))

if __name__ == "__main__":
    main()