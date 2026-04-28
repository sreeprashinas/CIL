import heapq
from collections import deque

class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
            print("Node added")
        else:
            print("Node already exists")

    def add_edge(self, u, v, cost=0):
        if u in self.graph and v in self.graph:
            if any(neighbor == v for neighbor, c in self.graph[u]):
                print("Edge already exists")
            else:
                self.graph[u].append((v, cost))
                self.graph[v].append((u, cost))
                print("Edge added")
        else:
            print("Add nodes first")

    def delete_node(self, node):
        if node in self.graph:
            self.graph.pop(node)
            for n in self.graph:
                self.graph[n] = [(x, c) for x, c in self.graph[n] if x != node]
            print("Node deleted")
        else:
            print("Node not found")

    def delete_edge(self, u, v):
        if u in self.graph:
            initial_count = len(self.graph[u])
            self.graph[u] = [(x, c) for x, c in self.graph[u] if x != v]
            self.graph[v] = [(x, c) for x, c in self.graph[v] if x != u]
            if len(self.graph[u]) < initial_count:
                print("Edge deleted")
            else:
                print("Edge not found")
        else:
            print("Edge not found")

    def display(self):
        print("\nGraph Structure:")
        for node in self.graph:
            print(f"{node} -> {self.graph[node]}")

    def display_adj_list(self, node):
        if node in self.graph:
            print(f"{node} -> {self.graph[node]}")
        else:
            print("Node not found")

    def _print_step(self, iteration, fringe, explored, is_ucs=False):
        if is_ucs:
            # For UCS, fringe contains (cost, node, path)
            fringe_str = str([(item[1], item[0]) for item in fringe])
            explored_str = str(explored)
        else:
            fringe_str = str([item[0] for item in fringe])
            explored_str = str(sorted(list(explored)))

        print(f"{iteration:<10} | {fringe_str:<40} | {explored_str}")

    def bfs_lr(self, start, goal_node=None):
        if start not in self.graph:
            print("Start node not found")
            return
        explored = set()
        fringe = deque([(start, [start])])
        iteration = 1
        print(f"\n{'Iter':<10} | {'Fringe (Queue)':<40} | {'Explored Set'}")
        print("-" * 80)
        while fringe:
            self._print_step(iteration, fringe, explored)
            node, path = fringe.popleft()
            if node not in explored:
                explored.add(node)
                if node == goal_node:
                    print(f"\nGoal '{goal_node}' reached! Path: {' -> '.join(path)}")
                    return
                for neigh, _ in self.graph[node]:
                    if neigh not in explored:
                        fringe.append((neigh, path + [neigh]))
            iteration += 1

    def bfs_rl(self, start, goal_node=None):
        if start not in self.graph: return
        explored = set()
        fringe = deque([(start, [start])])
        iteration = 1
        print(f"\n{'Iter':<10} | {'Fringe (Queue)':<40} | {'Explored Set'}")
        print("-" * 80)
        while fringe:
            self._print_step(iteration, fringe, explored)
            node, path = fringe.popleft()
            if node not in explored:
                explored.add(node)
                if node == goal_node:
                    print(f"\nGoal '{goal_node}' reached! Path: {' -> '.join(path)}")
                    return
                for neigh, _ in reversed(self.graph[node]):
                    if neigh not in explored:
                        fringe.append((neigh, path + [neigh]))
            iteration += 1

    def dfs_lr(self, start, goal_node=None):
        if start not in self.graph: return
        explored = set()
        fringe = [(start, [start])]
        iteration = 1
        print(f"\n{'Iter':<10} | {'Fringe (Stack)':<40} | {'Explored Set'}")
        print("-" * 80)
        while fringe:
            self._print_step(iteration, fringe, explored)
            node, path = fringe.pop()
            if node not in explored:
                explored.add(node)
                if node == goal_node:
                    print(f"\nGoal '{goal_node}' reached! Path: {' -> '.join(path)}")
                    return
                for neigh, _ in reversed(self.graph[node]):
                    if neigh not in explored:
                        fringe.append((neigh, path + [neigh]))
            iteration += 1

    def dfs_rl(self, start, goal_node=None):
        if start not in self.graph: return
        explored = set()
        fringe = [(start, [start])]
        iteration = 1
        print(f"\n{'Iter':<10} | {'Fringe (Stack)':<40} | {'Explored Set'}")
        print("-" * 80)
        while fringe:
            self._print_step(iteration, fringe, explored)
            node, path = fringe.pop()
            if node not in explored:
                explored.add(node)
                if node == goal_node:
                    print(f"\nGoal '{goal_node}' reached! Path: {' -> '.join(path)}")
                    return
                for neigh, _ in self.graph[node]:
                    if neigh not in explored:
                        fringe.append((neigh, path + [neigh]))
            iteration += 1

    def ucs(self, start, goal_node=None):
        if start not in self.graph:
            print("Start node not found")
            return

        # Priority Queue: (cumulative_cost, current_node, path)
        fringe = [(0, start, [start])]
        visited_costs = {start: 0}
        iteration = 1

        print(f"\n{'Iter':<10} | {'Fringe (Node, Cost)':<40} | {'Best Costs found'}")
        print("-" * 85)

        while fringe:
            # Always pop the path with the lowest cost
            cost, node, path = heapq.heappop(fringe)

            self._print_step(iteration, fringe, visited_costs, is_ucs=True)

            if node == goal_node:
                print(f"\nGoal reached! Optimal Path: {' -> '.join(path)} | Total Cost: {cost}")
                return

            for neigh, weight in self.graph[node]:
                new_cost = cost + weight
                # If we find a shorter path to neighbor, or it's new
                if neigh not in visited_costs or new_cost < visited_costs[neigh]:
                    visited_costs[neigh] = new_cost
                    heapq.heappush(fringe, (new_cost, neigh, path + [neigh]))

            iteration += 1
        print("\nGoal not reachable.")

# --- Driver Code ---
g = Graph()

while True:
    print("\n--- MENU ---")
    print("1  Add Node")
    print("2  Add Edge")
    print("3  Delete Node")
    print("4  Delete Edge")
    print("5  Display Graph")
    print("6  Display Adjacency List")
    print("7  BFS Left to Right")
    print("8  BFS Right to Left")
    print("9  DFS Left to Right")
    print("10 DFS Right to Left")
    print("11 Uniform Cost Search (UCS)")
    print("12 Exit")

    try:
        ch = int(input("Enter choice: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    if ch == 1:
        count = int(input("Number of nodes: "))
        for _ in range(count):
            g.add_node(input("Node name: "))
    elif ch == 2:
        count = int(input("Number of edges: "))
        for _ in range(count):
            u, v = input("From: "), input("To: ")
            c = int(input("Cost: "))
            g.add_edge(u, v, c)
    elif ch == 3:
        g.delete_node(input("Node: "))
    elif ch == 4:
        g.delete_edge(input("From: "), input("To: "))
    elif ch == 5:
        g.display()
    elif ch == 6:
        g.display_adj_list(input("Node: "))
    elif ch >= 7 and ch <= 11:
        s = input("Start node: ")
        gl = input("Goal node (optional): ")
        goal = gl if gl.strip() else None
        if ch == 7: g.bfs_lr(s, goal)
        elif ch == 8: g.bfs_rl(s, goal)
        elif ch == 9: g.dfs_lr(s, goal)
        elif ch == 10: g.dfs_rl(s, goal)
        elif ch == 11: g.ucs(s, goal)
    elif ch == 12:
        print("Exiting...")
        break
    else:
        print("Invalid choice.")
