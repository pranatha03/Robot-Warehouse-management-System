import threading
import queue
import time

from robot import Robot, Task
from synchronization import path_locks
from scheduler import fcfs_schedule
from deadlock import request_resource, print_state
from resource_manager import ResourceManager
from ipc import CentralController

print("=" * 55)
print("   ROBOT WAREHOUSE MANAGEMENT SYSTEM")
print("=" * 55)

resource_manager = ResourceManager()
controller = CentralController()

task_queue = fcfs_schedule()

NUM_ROBOTS = 4
for _ in range(NUM_ROBOTS):
    task_queue.put(None)

robots = [
    Robot("R1", path_locks, task_queue),
    Robot("R2", path_locks, task_queue),
    Robot("R3", path_locks, task_queue),
    Robot("R4", path_locks, task_queue),
]

controller.broadcast("Warehouse OPEN")

print("\n--- Banker's Algorithm Check ---")
print_state()
request_resource(0, [1, 0, 0])
request_resource(1, [0, 1, 0])
print_state()

print("\n--- Starting Robots ---")
for r in robots:
    r.start()
    controller.robot_report(r.robot_id, "Started")

for r in robots:
    r.join()

print("\n" + "=" * 55)
print("   FINAL REPORT")
print("=" * 55)
for r in robots:
    info = r.get_info()
    print(f"  {info['robot_id']} | Tasks: {info['tasks_done']} | Battery: {info['battery']}%")

resource_manager.print_status()
msgs = controller.read_controller_inbox()
print(f"\n[IPC] Controller got {len(msgs)} messages")
print("\n  Done!")