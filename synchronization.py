import threading

path_locks = {
    "P1": threading.Lock(),
    "P2": threading.Lock(),
    "P3": threading.Lock()
}

robot_semaphore = threading.Semaphore(3)

charging_lock = threading.Lock()

def acquire_path(path_name):
    lock = path_locks.get(path_name)
    if lock:
        lock.acquire()
        print(f"[SYNC] Path {path_name} LOCKED")

def release_path(path_name):
    lock = path_locks.get(path_name)
    if lock:
        lock.release()
        print(f"[SYNC] Path {path_name} UNLOCKED")

def is_path_locked(path_name):
    lock = path_locks.get(path_name)
    if lock:
        acquired = lock.acquire(blocking=False)
        if acquired:
            lock.release()
            return False
        return True
    return False