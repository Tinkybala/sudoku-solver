import sys
from collections import deque, defaultdict
from typing import DefaultDict, Deque, List

class AC3():
    def __init__(self):
        """
        Initialise the AC3 object

        Parameters:
        domain (dict): domain for each vairable stored as a list
        constraints (deque): queue to store arcs. List of Lists
        neighbors (dict): dictionary that maps a variable to a set of its neighbors
        k (int): total number of variables
        """
        self.domain: dict = {}
        self.constraints: Deque[list] = deque([])
        self.neighbors: DefaultDict[str, set] = defaultdict(set)
        self.k: int = 0
    
    def _read_input(self) -> None:
        """
        Reads the input from stdin and populates the object variables.
        """
        # Extract Domain
        self.k = int(sys.stdin.readline().strip())
        for i in range(self.k):
            # Split the cell name and the domain
            line = sys.stdin.readline().strip()
            line_arr = line.split()
            key = line_arr[0]
            value = line_arr[1:]
            self.domain[key] = value
        
        # Extract Constraints
        constraints_n = int(sys.stdin.readline().strip())
        for i in range(constraints_n):
            line = sys.stdin.readline().strip()
            line_arr = line.split()
            pair = line_arr[1:]
            self.constraints.append(pair)
            self.neighbors[pair[0]].add(pair[1])
            self.neighbors[pair[1]].add(pair[0])


    
    def remove_inconsistent_arcs(self, node1: str, node2: str) -> bool:
        """
        Determines if node1 is arc consistent with respect to node2.
        If not arc consistent, will reduce the domain of node1 to obtain arc consistency

        Args:
            node1 (str): variable 1
            node2 (str): variable 2

        Returns:
            bool: Whether node1 is arc-consistent with respect to node2
        """
        removed = False
        new_domain = []
        for i, x_i in enumerate(self.domain[node1]):
                if any([x_i != x_j for x_j in self.domain[node2]]):
                    new_domain.append(x_i)
                    continue
                removed = True
        self.domain[node1] = new_domain

        return removed

    def generate_ac_graph(self):
        self._read_input()
        while self.constraints:
            c = self.constraints.popleft()
            if self.remove_inconsistent_arcs(c[0], c[1]):
                for n in self.neighbors[c[0]]:
                    self.constraints.append([n, c[0]])
            if self.remove_inconsistent_arcs(c[1], c[0]):
                for n in self.neighbors[c[1]]:
                    self.constraints.append([n, c[1]])
    
    def __call__(self):
        self.generate_ac_graph()
        print(self.k)
        for key, value in self.domain.items():
            print(f"{key} {' '.join(str(num) for num in value)}")

    



if __name__ == "__main__":
    ac3 = AC3()
    ac3()