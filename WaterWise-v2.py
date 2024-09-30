import tkinter as tk
from tkinter import messagebox, scrolledtext

def water_jug_problem():
    def solve_problem():
        # Define jug letters
        jug_letters = ['A', 'B', 'C', 'D', 'E']

        # Get user inputs
        try:
            num_jugs = int(num_jugs_entry.get())
            if num_jugs > 5:
                messagebox.showwarning("Warning", "Maximum number of jugs is 5. Setting to 5.")
                num_jugs = 5

            jugs = []
            for i in range(num_jugs):
                capacity = int(jug_capacities[i].get())
                jugs.append({"capacity": capacity, "current": 0})

            target = {}
            for i in range(num_jugs):
                amount = int(target_amounts[i].get())
                if amount > 0:
                    target[i] = amount

            # Initialize water supply (can be changed in the future)
            water_supply = 9999999999999999999999999999

            def get_jug_state():
                return tuple(jug["current"] for jug in jugs)

            def solve():
                visited = set()
                queue = [(get_jug_state(), [])]

                while queue:
                    state, path = queue.pop(0)
                    if state in visited:
                        continue
                    visited.add(state)

                    if all(state[i] == target.get(i, 0) for i in range(num_jugs)):
                        return path

                    for i in range(num_jugs):
                        # Fill jug
                        if state[i] < jugs[i]["capacity"] and water_supply > 0:
                            new_state = list(state)
                            fill_amount = min(jugs[i]["capacity"] - state[i], water_supply)
                            new_state[i] = jugs[i]["capacity"]
                            queue.append((tuple(new_state), path + [(f"Fill jug {jug_letters[i]}", new_state)]))

                        # Empty jug
                        if state[i] > 0:
                            new_state = list(state)
                            new_state[i] = 0
                            queue.append((tuple(new_state), path + [(f"Empty jug {jug_letters[i]}", new_state)]))

                        # Pour to another jug
                        for j in range(num_jugs):
                            if i != j and state[i] > 0 and state[j] < jugs[j]["capacity"]:
                                new_state = list(state)
                                amount = min(state[i], jugs[j]["capacity"] - state[j])
                                new_state[i] -= amount
                                new_state[j] += amount
                                queue.append((tuple(new_state), path + [(f"Pour {amount}L from jug {jug_letters[i]} to jug {jug_letters[j]}", new_state)]))

                return None

            solution = solve()

            if solution:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Solution:\n")
                result_text.insert(tk.END, f"{'Step':^5} | {'Action':^30} | {'Jug States':^{num_jugs * 5}}\n")
                result_text.insert(tk.END, "-" * (40 + num_jugs * 5) + "\n")
                for step, (action, state) in enumerate(solution, 1):
                    jug_states = " ".join(f"{s:3d}" for s in state)
                    result_text.insert(tk.END, f"{step:5d} | {action:30} | {jug_states:^{num_jugs * 5}}\n")
                result_text.insert(tk.END, f"\nTotal number of steps taken: {len(solution)}")
            else:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "No solution found for the given inputs.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values for all inputs.")

    # Create main window
    root = tk.Tk()
    root.title("Water Jug Problem Solver")

    # Create and pack widgets
    tk.Label(root, text="Welcome to the Water Jug Problem Solver!", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Rules:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)
    rules = [
        "1. You can only manipulate one jug at a time.",
        "2. Jugs can only be completely filled, completely emptied, or have water transferred between them.",
        "3. There are no measurement instruments available.",
        "4. Water can be transferred between jugs or poured onto the ground.",
        "5. By default, there's an unlimited water supply, but this can be changed."
    ]
    for rule in rules:
        tk.Label(root, text=rule).pack(anchor="w", padx=20)

    tk.Label(root, text="Number of jugs (max 5):").pack(pady=5)
    num_jugs_entry = tk.Entry(root)
    num_jugs_entry.pack()

    jug_frame = tk.Frame(root)
    jug_frame.pack(pady=10)

    jug_capacities = []
    target_amounts = []
    for i in range(5):
        tk.Label(jug_frame, text=f"Jug {chr(65+i)}:").grid(row=i, column=0, padx=5)
        capacity_entry = tk.Entry(jug_frame, width=10)
        capacity_entry.grid(row=i, column=1, padx=5)
        jug_capacities.append(capacity_entry)
        
        tk.Label(jug_frame, text="Target:").grid(row=i, column=2, padx=5)
        target_entry = tk.Entry(jug_frame, width=10)
        target_entry.grid(row=i, column=3, padx=5)
        target_amounts.append(target_entry)

    solve_button = tk.Button(root, text="Solve", command=solve_problem)
    solve_button.pack(pady=10)

    result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    result_text.pack(padx=10, pady=10)

    root.mainloop()

# Run the water jug problem solver
water_jug_problem()
