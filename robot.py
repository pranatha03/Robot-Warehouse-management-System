import threading
import time
shared_states = {}

class RobotState:
    IDLE = "IDLE"
    MOVING = "MOVING"
    WAITING = "WAITING"
    CHARGING = "CHARGING"
    TERMINATED = "TERMINATED"

class Task:
    _id = 0
    def __init__(self, item, source, destination, path_to_source, path_to_dest, priority=1):
        Task._id += 1
        self.task_id = Task._id
        self.item = item
        self.source = source
        self.destination = destination
        self.path_to_source = path_to_source
        self.path_to_dest = path_to_dest
        self.priority = priority
        self.status = "PENDING"

    def __str__(self):
        return f"Task#{self.task_id} [{self.item}: {self.source} -> {self.destination}, priority={self.priority}]"

    def __lt__(self, other):
        return self.priority > other.priority


class Robot(threading.Thread):
    def __init__(self, robot_id, path_locks, task_queue, log_func=print):
        super().__init__(name=robot_id, daemon=True)
        self.robot_id = robot_id
        self.path_locks = path_locks
        self.task_queue = task_queue
        self.log = log_func
        self.state = RobotState.IDLE
        shared_states[self.robot_id] = self.state
        self.battery = 100
        self.position = "Base"
        self.tasks_done = 0
        self.current_task = None

    def get_info(self):
        return {
            "robot_id": self.robot_id,
            "state": self.state,
            "battery": self.battery,
            "position": self.position,
            "tasks_done": self.tasks_done,
            "current_task": str(self.current_task) if self.current_task else "None"
        }

    def run(self):
        self.log(f"[{self.robot_id}] STARTED")
        while True:
            self.state = RobotState.IDLE
            shared_states[self.robot_id] = self.state
            task = self.task_queue.get()
            if task is None:
                break
            self.current_task = task
            self.log(f"[{self.robot_id}] Got {task}")
            self._execute_task(task)
        self.state = RobotState.TERMINATED
        shared_states[self.robot_id] = self.state
        self.log(f"[{self.robot_id}] TERMINATED")

    def _execute_task(self, task):
        self._move(task.source, task.path_to_source)
        self.log(f"[{self.robot_id}] Picked up {task.item} from {task.source}")
        time.sleep(0.3)
        self._move(task.destination, task.path_to_dest)
        self.log(f"[{self.robot_id}] Delivered {task.item} to {task.destination}")
        time.sleep(0.3)
        self.position = "Base"
        self.battery = max(0, self.battery - 15)
        self.tasks_done += 1
        self.current_task = None
        self.task_queue.task_done()
        self.log(f"[{self.robot_id}] Task done. Battery: {self.battery}%")
        if self.battery <= 30:
            self._charge()

    def _move(self, destination, path_name):
        lock = self.path_locks.get(path_name)
        if lock:
            self.state = RobotState.WAITING
            shared_states[self.robot_id] = self.state
            self.log(f"[{self.robot_id}] Waiting for path {path_name}...")
            lock.acquire()
            self.state = RobotState.MOVING
            shared_states[self.robot_id] = self.state
            self.log(f"[{self.robot_id}] Acquired {path_name}, moving to {destination}")
        time.sleep(0.8)
        self.position = destination
        if lock:
            lock.release()
            self.log(f"[{self.robot_id}] Released {path_name}")

    def _charge(self):
        self.state = RobotState.CHARGING
        shared_states[self.robot_id] = self.state
        self.log(f"[{self.robot_id}] Charging...")
        time.sleep(1.0)
        self.battery = 100
        self.log(f"[{self.robot_id}] Fully charged")
