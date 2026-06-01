import queue
import threading

class CentralController:
    def __init__(self):
        self.robot_inboxes = {
            "R1": queue.Queue(),
            "R2": queue.Queue(),
            "R3": queue.Queue(),
            "R4": queue.Queue(),
        }
        self.controller_inbox = queue.Queue()

    def send_to_robot(self, robot_id, message):
        if robot_id in self.robot_inboxes:
            self.robot_inboxes[robot_id].put(message)
            print(f"[IPC] Controller -> {robot_id}: {message}")

    def robot_report(self, robot_id, message):
        self.controller_inbox.put({"from": robot_id, "msg": message})
        print(f"[IPC] {robot_id} -> Controller: {message}")

    def broadcast(self, message):
        for robot_id in self.robot_inboxes:
            self.robot_inboxes[robot_id].put(message)
        print(f"[IPC] BROADCAST: {message}")

    def read_controller_inbox(self):
        messages = []
        while not self.controller_inbox.empty():
            messages.append(self.controller_inbox.get_nowait())
        return messages