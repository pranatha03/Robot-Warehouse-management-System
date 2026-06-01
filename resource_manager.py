import threading

PATHS    = ["P1", "P2", "P3"]
RACKS    = ["Rack-A", "Rack-B", "Rack-C"]
CHARGERS = ["Charger-1", "Charger-2"]

class ResourceManager:
    def __init__(self):
        self.path_status    = {p: None for p in PATHS}
        self.rack_status    = {r: None for r in RACKS}
        self.charger_status = {c: None for c in CHARGERS}
        self._lock = threading.Lock()

    def allocate_path(self, path, robot_id):
        with self._lock:
            if self.path_status[path] is None:
                self.path_status[path] = robot_id
                print(f"[RESOURCE] {robot_id} allocated {path}")
                return True
            print(f"[RESOURCE] {path} busy. {robot_id} waits.")
            return False

    def release_path(self, path, robot_id):
        with self._lock:
            self.path_status[path] = None
            print(f"[RESOURCE] {robot_id} released {path}")

    def allocate_charger(self, robot_id):
        with self._lock:
            for c in CHARGERS:
                if self.charger_status[c] is None:
                    self.charger_status[c] = robot_id
                    print(f"[RESOURCE] {robot_id} allocated {c}")
                    return c
            print(f"[RESOURCE] No charger free for {robot_id}")
            return None

    def release_charger(self, charger, robot_id):
        with self._lock:
            self.charger_status[charger] = None
            print(f"[RESOURCE] {robot_id} released {charger}")

    def print_status(self):
        print("\n[RESOURCE] Status:")
        print(f"  Paths:    {self.path_status}")
        print(f"  Racks:    {self.rack_status}")
        print(f"  Chargers: {self.charger_status}")