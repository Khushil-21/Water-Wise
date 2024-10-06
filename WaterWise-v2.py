import tkinter as tk
from tkinter import messagebox, scrolledtext

def water_jug_problem():
    """
    Main function that sets up the GUI and handles the water jug problem solving process.
    """
    def solve_problem():
        """
        Function to solve the water jug problem based on user inputs.
        It validates inputs, sets up the problem, finds the solution, and displays the result.
        """
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
                """
                Helper function to get the current state of all jugs.
                Returns a tuple of current water amounts in each jug.
                """
                return tuple(jug["current"] for jug in jugs)

            def solve():
                """
                Core function to solve the water jug problem using BFS algorithm.
                Returns the solution path if found, otherwise returns None.
                """
                visited = set()
                queue = [(get_jug_state(), [])]

                while queue:
                    state, path = queue.pop(0)
                    if state in visited:
                        continue
                    visited.add(state)

                    # Check if current state matches the target state
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
                                # Calculate the amount to pour
                                amount = min(state[i], jugs[j]["capacity"] - state[j])
                                new_state[i] -= amount
                                new_state[j] += amount
                                queue.append((tuple(new_state), path + [(f"Pour {amount}L from jug {jug_letters[i]} to jug {jug_letters[j]}", new_state)]))

                return None

            solution = solve()

            if solution:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Solution:\n")
                # Create header for solution display
                result_text.insert(tk.END, f"{'Step':^5} | {'Action':^30} | {'Jug States':^{num_jugs * 5}}\n")
                result_text.insert(tk.END, "-" * (40 + num_jugs * 5) + "\n")
                for step, (action, state) in enumerate(solution, 1):
                    # Format jug states for display
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

"""
Execution flow and features of the code:

1. The code starts by importing necessary modules from tkinter.

2. The main function `water_jug_problem()` is defined, which sets up the GUI for the Water Jug Problem Solver.

3. Inside `water_jug_problem()`, a nested function `solve_problem()` is defined to handle the problem-solving logic.

4. The GUI is created using tkinter, including:
   - A title and welcome message
   - Rules of the game
   - Input fields for the number of jugs (max 5)
   - Input fields for jug capacities and target amounts
   - A "Solve" button
   - A text area to display the solution

5. When the user clicks the "Solve" button, `solve_problem()` is called:
   - It retrieves and validates user inputs
   - Sets up the problem with jugs and targets
   - Calls the `solve()` function to find a solution using BFS algorithm
   - Displays the solution or an error message in the result text area

6. The `solve()` function uses a breadth-first search algorithm to find the shortest path to the target state:
   - It explores all possible actions: filling a jug, emptying a jug, or transferring water between jugs
   - It keeps track of visited states to avoid loops
   - If a solution is found, it returns the path of actions to reach the target state

7. The solution, if found, is displayed step by step in the result text area, showing each action and the resulting jug states.

8. The code handles various error cases, such as invalid inputs or when no solution is found.

9. The GUI remains active and responsive, allowing the user to solve multiple problems without restarting the application.

This code provides a user-friendly interface for solving the Water Jug Problem, with clear instructions, input validation, and detailed solution output.
"""
