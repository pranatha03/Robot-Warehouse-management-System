import tkinter as tk
import threading
from robot import shared_states

# -----------------------
# WINDOW
# -----------------------
root = tk.Tk()
root.title("Robot Warehouse Management System")
root.geometry("1000x600")

# -----------------------
# CANVAS
# -----------------------
canvas = tk.Canvas(root, width=650, height=600, bg="white")
canvas.pack(side=tk.LEFT)

# -----------------------
# SIDE PANEL
# -----------------------
panel = tk.Frame(root, width=350)
panel.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(
    panel,
    text="ROBOT WAREHOUSE DASHBOARD",
    font=("Arial", 16, "bold")
).pack(pady=10)

scheduler_label = tk.Label(
    panel,
    text="Scheduler: FCFS",
    font=("Arial", 12)
)
scheduler_label.pack()

deadlock_label = tk.Label(
    panel,
    text="Banker's Algorithm: SAFE",
    fg="green",
    font=("Arial", 12, "bold")
)
deadlock_label.pack(pady=10)

robot_status = tk.Label(
    panel,
    text="Waiting to start...",
    justify="left",
    font=("Consolas", 12)
)
robot_status.pack(pady=20)

# -----------------------
# TITLE
# -----------------------
canvas.create_text(
    325,
    30,
    text="ROBOT WAREHOUSE MANAGEMENT SYSTEM",
    font=("Arial", 16, "bold")
)

# -----------------------
# PATHS
# -----------------------
canvas.create_rectangle(250,100,450,150,fill="lightgray")
canvas.create_text(350,125,text="P1")

canvas.create_rectangle(250,250,450,300,fill="lightgray")
canvas.create_text(350,275,text="P2")

canvas.create_rectangle(250,400,450,450,fill="lightgray")
canvas.create_text(350,425,text="P3")

# -----------------------
# ROBOTS
# -----------------------
r1 = canvas.create_oval(50,80,100,130,fill="blue")
r2 = canvas.create_oval(50,200,100,250,fill="blue")
r3 = canvas.create_oval(50,320,100,370,fill="blue")
r4 = canvas.create_oval(50,440,100,490,fill="blue")

canvas.create_text(75,70,text="R1")
canvas.create_text(75,190,text="R2")
canvas.create_text(75,310,text="R3")
canvas.create_text(75,430,text="R4")

# -----------------------
# UPDATE GUI
# -----------------------
def update_robot_colors():

    colors = {
        "IDLE": "blue",
        "MOVING": "green",
        "WAITING": "yellow",
        "CHARGING": "orange",
        "TERMINATED": "red"
    }

    s1 = shared_states.get("R1", "IDLE")
    s2 = shared_states.get("R2", "IDLE")
    s3 = shared_states.get("R3", "IDLE")
    s4 = shared_states.get("R4", "IDLE")

    canvas.itemconfig(r1, fill=colors.get(s1, "blue"))
    canvas.itemconfig(r2, fill=colors.get(s2, "blue"))
    canvas.itemconfig(r3, fill=colors.get(s3, "blue"))
    canvas.itemconfig(r4, fill=colors.get(s4, "blue"))

    robot_status.config(
        text=
        f"R1 : {s1}\n"
        f"R2 : {s2}\n"
        f"R3 : {s3}\n"
        f"R4 : {s4}"
    )

    root.after(500, update_robot_colors)

# -----------------------
# RUN BACKEND
# -----------------------
def run_backend():
    import main

def start_simulation():
    threading.Thread(
        target=run_backend,
        daemon=True
    ).start()

# -----------------------
# BUTTON
# -----------------------
tk.Button(
    panel,
    text="START SIMULATION",
    font=("Arial", 12, "bold"),
    command=start_simulation
).pack(pady=20)

# Start GUI updates
update_robot_colors()

root.mainloop()
