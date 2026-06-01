NUM_ROBOTS = 4
NUM_RESOURCES = 3
RESOURCE_NAMES = ["P1", "P2", "P3"]

total_resources = [1, 1, 1]

max_need = [
    [1, 1, 0],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
]

allocated = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def get_available():
    avail = list(total_resources)
    for i in range(NUM_ROBOTS):
        for j in range(NUM_RESOURCES):
            avail[j] -= allocated[i][j]
    return avail

def get_need():
    need = []
    for i in range(NUM_ROBOTS):
        row = [max_need[i][j] - allocated[i][j] for j in range(NUM_RESOURCES)]
        need.append(row)
    return need

def is_safe_state():
    available = get_available()
    need = get_need()
    finish = [False] * NUM_ROBOTS
    safe_seq = []

    while len(safe_seq) < NUM_ROBOTS:
        found = False
        for i in range(NUM_ROBOTS):
            if not finish[i]:
                if all(need[i][j] <= available[j] for j in range(NUM_RESOURCES)):
                    for j in range(NUM_RESOURCES):
                        available[j] += allocated[i][j]
                    finish[i] = True
                    safe_seq.append(f"R{i+1}")
                    found = True
        if not found:
            break

    if len(safe_seq) == NUM_ROBOTS:
        return True, safe_seq
    else:
        return False, safe_seq

def request_resource(robot_index, request):
    available = get_available()
    need = get_need()
    print(f"\n[DEADLOCK] R{robot_index+1} requesting {dict(zip(RESOURCE_NAMES, request))}")

    for j in range(NUM_RESOURCES):
        if request[j] > need[robot_index][j]:
            print(f"[DEADLOCK] ERROR: Request exceeds max need. Denied.")
            return False

    for j in range(NUM_RESOURCES):
        if request[j] > available[j]:
            print(f"[DEADLOCK] Resources not available. R{robot_index+1} must wait.")
            return False

    for j in range(NUM_RESOURCES):
        allocated[robot_index][j] += request[j]

    safe, seq = is_safe_state()
    if safe:
        print(f"[DEADLOCK] Request GRANTED. Safe sequence: {' -> '.join(seq)}")
        return True
    else:
        for j in range(NUM_RESOURCES):
            allocated[robot_index][j] -= request[j]
        print(f"[DEADLOCK] Request DENIED — unsafe state")
        return False

def print_state():
    available = get_available()
    need = get_need()
    print("\n[DEADLOCK] Current State:")
    for i in range(NUM_ROBOTS):
        print(f"  R{i+1} | Allocated: {allocated[i]} | Need: {need[i]}")
    print(f"  Available: {dict(zip(RESOURCE_NAMES, available))}")