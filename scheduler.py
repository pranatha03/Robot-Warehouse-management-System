import queue
from robot import Task

HARDCODED_TASKS = [
    Task("Box-1", "Rack-A", "Station-Y", "P1", "P2", priority=2),
    Task("Box-2", "Rack-B", "Station-Y", "P2", "P3", priority=1),
    Task("Box-3", "Rack-C", "Station-Y", "P1", "P3", priority=3),
    Task("Box-4", "Rack-A", "Station-Y", "P2", "P1", priority=1),
    Task("Box-5", "Rack-B", "Station-Y", "P3", "P2", priority=2),
    Task("Box-6", "Rack-C", "Station-Y", "P1", "P2", priority=3),
]

def fcfs_schedule():
    print("\n[SCHEDULER] Mode: FCFS")
    q = queue.Queue()
    for task in HARDCODED_TASKS:
        q.put(task)
    return q

def priority_schedule():
    print("\n[SCHEDULER] Mode: PRIORITY")
    q = queue.PriorityQueue()
    for task in HARDCODED_TASKS:
        q.put(task)
    normal_q = queue.Queue()
    while not q.empty():
        normal_q.put(q.get())
    return normal_q

def round_robin_schedule(num_robots=4):
    print("\n[SCHEDULER] Mode: ROUND ROBIN")
    queues = [queue.Queue() for _ in range(num_robots)]
    for i, task in enumerate(HARDCODED_TASKS):
        queues[i % num_robots].put(task)
    return queues