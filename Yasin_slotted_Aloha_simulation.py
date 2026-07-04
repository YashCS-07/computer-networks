import random
import matplotlib.pyplot as plt

# Total number of time slots for simulation
TSLOTS = 100000

# Optional: Use a fixed seed for reproducible results
random.seed(42)


class Node:
    def __init__(self, window):
        self.window = window
        # Random initial backoff timer
        self.timer = random.randint(0, window - 1)

    def tick(self):
        # Decrease the timer by one slot
        if self.timer > 0:
            self.timer -= 1

    def backoff(self):
        # Choose a new random backoff after success or collision
        self.timer = random.randint(0, self.window - 1)


def simulate(window, max_nodes):
    """
    Simulate Slotted ALOHA for a given contention window.
    Returns lists of node counts and efficiencies.
    """

    nodes_list = []
    efficiency_list = []

    print(f"\nWindow Size = {window}")

    for N in range(1, max_nodes + 1):

        # Create N nodes
        nodes = [Node(window) for _ in range(N)]
        successful = 0

        # Simulate all time slots
        for _ in range(TSLOTS):

            transmitters = []

            # Check which nodes are ready to transmit
            for i in range(N):
                if nodes[i].timer == 0:
                    transmitters.append(i)
                else:
                    nodes[i].tick()

            # One transmitter -> Successful transmission
            if len(transmitters) == 1:
                successful += 1
                nodes[transmitters[0]].backoff()

            # More than one transmitter -> Collision
            elif len(transmitters) > 1:
                for i in transmitters:
                    nodes[i].backoff()

        # Calculate slot efficiency
        efficiency = successful / TSLOTS

        print(f"Nodes = {N:2d}   Efficiency = {efficiency:.4f}")

        nodes_list.append(N)
        efficiency_list.append(efficiency)

    return nodes_list, efficiency_list


def main():

    windows = [8, 16, 32]

    for window in windows:
        nodes, efficiency = simulate(window, 32)
        plt.plot(nodes, efficiency, marker='o', label=f"W={window}")

    plt.title("Simulation of Slotted ALOHA")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Slot Efficiency")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()