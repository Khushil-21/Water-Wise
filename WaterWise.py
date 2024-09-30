def water_jug_problem():
    print("Welcome to the Water Jug Problem Solver!")
    print("\nRules:")
    print("1. You can only manipulate one jug at a time.")
    print("2. Jugs can only be completely filled, completely emptied, or have water transferred between them.")
    print("3. There are no measurement instruments available.")
    print("4. Water can be transferred between jugs or poured onto the ground.")
    print("5. By default, there's an unlimited water supply, but this can be changed.")

    # Define jug letters
    jug_letters = ['A', 'B', 'C', 'D', 'E']

    # Get user inputs
    num_jugs = int(input("\nEnter the number of jugs (max 5): "))
    if num_jugs > 5:
        print("Maximum number of jugs is 5. Setting to 5.")
        num_jugs = 5

    jugs = []
    for i in range(num_jugs):
        capacity = int(input(f"Enter the capacity of jug {jug_letters[i]}: "))
        jugs.append({"capacity": capacity, "current": 0})

    target = {}
    print("\nNow, enter the target amounts for each jug:")
    for i in range(num_jugs):
        amount = int(input(f"Enter the target amount for jug {jug_letters[i]} (0 if no target): "))
        if amount > 0:
            target[i] = amount

    # Initialize water supply (can be changed in the future)
    water_supply = 9999999999999999999999999999

    # Initialize steps
    steps = []

    def pour(from_jug, to_jug):
        amount = min(jugs[from_jug]["current"], jugs[to_jug]["capacity"] - jugs[to_jug]["current"])
        jugs[from_jug]["current"] -= amount
        jugs[to_jug]["current"] += amount
        return amount

    def is_goal_reached():
        return all(jugs[i]["current"] == target.get(i, 0) for i in range(num_jugs))

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
        print("\nSolution:")
        jug_headers = " ".join(f"{jug_letters[i]:^5}" for i in range(num_jugs))
        print("-" * (40 + num_jugs * 6))
        print(f"{'Step':^5} | {'Action':^30} | {jug_headers}")
        print("-" * (40 + num_jugs * 6))
        for i, (action, state) in enumerate(solution, 1):
            jug_state = " ".join(f"{s:3}L" for s in state)
            print(f"{i:^5} | {action:^30} | {jug_state:^{num_jugs * 6}}")
            print("-" * (40 + num_jugs * 6))
        print(f"\nTotal number of steps: {len(solution)}")
    else:
        print("\nNo solution found for the given inputs.")

# Run the water jug problem solver
water_jug_problem()
