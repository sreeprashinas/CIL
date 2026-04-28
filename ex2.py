import heapq
from collections import deque

class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
            print(f"Node '{node}' added.")
        else:
            print("Node already exists.")

    def add_edge(self, u, v, cost=0):
        if u in self.graph and v in self.graph:
            if any(neighbor == v for neighbor, c in self.graph[u]):
                print("Edge already exists.")
            else:
                self.graph[u].append((v, cost))
                self.graph[v].append((u, cost))
                print(f"Edge {u}-{v} with cost {cost} added.")
        else:
            print("Error: Add both nodes first.")

    def delete_node(self, node):
        if node in self.graph:
            self.graph.pop(node)
            for n in self.graph:
                self.graph[n] = [(x, c) for x, c in self.graph[n] if x != node]
            print(f"Node '{node}' deleted.")
        else:
            print("Node not found.")

    def delete_edge(self, u, v):
        if u in self.graph and v in self.graph:
            initial_count = len(self.graph[u])
            self.graph[u] = [(x, c) for x, c in self.graph[u] if x != v]
            self.graph[v] = [(x, c) for x, c in self.graph[v] if x != u]
            if len(self.graph[u]) < initial_count:
                print(f"Edge {u}-{v} deleted.")
            else:
                print("Edge not found.")
        else:
            print("One or both nodes not found.")

    def display(self):
        print("\n--- Current Graph Structure ---")
        if not self.graph:
            print("Graph is empty.")
        for node in self.graph:
            print(f"{node} -> {self.graph[node]}")

    def get_heuristics(self, goal):
        h_table = {}
        print(f"\n--- Enter Heuristics (Goal: {goal}) ---")
        for node in self.graph:
            if node == goal:
                h_table[node] = 0
            else:
                while True:
                    try:
                        val = input(f"Heuristic for node '{node}': ")
                        h_table[node] = int(val)
                        break
                    except ValueError:
                        print("Invalid input! Please enter an integer.")
        return h_table

    def astar(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            print("Error: Start or Goal node not in graph.")
            return

        h_table = self.get_heuristics(goal)
        # Priority Queue stores: (f_score, g_score, current_node, path)
        frontier = []
        heapq.heappush(frontier, (h_table[start], 0, start, [start]))

        explored = []
        iteration = 1

        print(f"\n{'Iter':<5} | {'Fringe (Node, f=g+h)':<45} | {'Explored'}")
        print("-" * 85)

        while frontier:
            # Prepare fringe view for display (sorted by f_score)
            fringe_view = sorted([(node, f) for (f, g, node, path) in frontier], key=lambda x: x[1])
            print(f"{iteration:<5} | {str(fringe_view):<45} | {explored}")

            f, g, current_node, path = heapq.heappop(frontier)

            if current_node in explored:
                continue

            explored.append(current_node)

            if current_node == goal:
                print("\n" + "="*30)
                print(f"GOAL REACHED: {goal}")
                print(f"Optimized Path: {' -> '.join(path)}")
                print(f"Total Path Cost (g): {g}")
                print("="*30)
                return

            for neighbor, cost in self.graph[current_node]:
                if neighbor not in explored:
                    new_g = g + cost
                    new_f = new_g + h_table[neighbor]
                    heapq.heappush(frontier, (new_f, new_g, neighbor, path + [neighbor]))

            iteration += 1

        print("\nGoal not reachable.")

# --- Main Menu Loop ---
def main():
    g = Graph()
    while True:
        print("\n--- GRAPH SEARCH MENU ---")
        print("1. Add Node")
        print("2. Add Edge")
        print("3. Delete Node")
        print("4. Delete Edge")
        print("5. Display Graph")
        print("6. Run A* Search")
        print("7. Exit")

        choice = input("Enter choice (1-7): ").strip()

        if choice == '1':
            node = input("Enter node name: ")
            g.add_node(node)
        elif choice == '2':
            u = input("Enter start node: ")
            v = input("Enter end node: ")
            try:
                cost = int(input("Enter edge cost: "))
                g.add_edge(u, v, cost)
            except ValueError:
                print("Invalid cost! Must be an integer.")
        elif choice == '3':
            node = input("Enter node to delete: ")
            g.delete_node(node)
        elif choice == '4':
            u = input("Enter first node of edge: ")
            v = input("Enter second node of edge: ")
            g.delete_edge(u, v)
        elif choice == '5':
            g.display()
        elif choice == '6':
            start_node = input("Enter Start Node: ")
            goal_node = input("Enter Goal Node: ")
            g.astar(start_node, goal_node)
        elif choice == '7':
            print("Exiting program.")
            break
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    main()
