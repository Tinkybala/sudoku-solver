import sys
import math
from collections import deque, defaultdict
from typing import List, Tuple, DefaultDict, Deque
import time

class AC3():
    def __init__(self, domain: dict, constraints: List[Tuple[str, str]]):
        """
        Initialise the AC3 object

        Parameters:
        domain (dict): domain for each vairable stored as a list. Dictionary of lists
        constraints (list): list of tuples containing constraint between pairs of variables
        queue (deque): queue to store arcs. an arc is represented by a tuple of 2 variables
        neighbors (dict): dictionary that maps a variable to a set of its neighbors
        k (int): total number of variables
        """
        self.domain: dict = domain
        self.constraints: list = constraints
        self.queue: Deque[tuple] = deque(constraints)
        self.neighbors: DefaultDict[str, set] = defaultdict(set)
        self.k: int = len(domain)

        # Initialise neighbors
        for pair in constraints:
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
        while self.queue:
            c = self.queue.popleft()
            if self.remove_inconsistent_arcs(c[0], c[1]):
                for n in self.neighbors[c[0]]:
                    self.queue.append([n, c[0]])
            if self.remove_inconsistent_arcs(c[1], c[0]):
                for n in self.neighbors[c[1]]:
                    self.queue.append([n, c[1]])
    
    def __call__(self):
        self.generate_ac_graph()
        return self.domain

class Solver():
    def __init__(self):
        self.domain: dict = {}
        self.constraints: list = []

    def _get_grid(self) -> List[List[int]]:
        """
        Reads from stdin and converts it into a 2d list

        Returns:
            List[List[int]]: n x n list of the sudoku grid
        """
        grid = []
        for line in sys.stdin:
            line = line.strip()
            row = [int(c) for c in line]
            grid.append(row)
        return grid
    
    def _get_inequality_constraints(self, grid: List[List[int]]) -> List[Tuple[str, str]]:
        """
        Determines the inequality constraints of a n x n sudoku grid.

        Args:
            grid (List[List[int]]): n x n sudoku grid

        Returns:
            List[Tuple[int, int]]: A list of tuples, each tuples containing two cells which should
                                not be equal. Example: [("1-1","1-2")] has only one constraint between
                                the cells 1-1 and 1-2.
        """
        constraints = set([])
        region_size = math.isqrt(len(grid))
        proper_sudoku = True if region_size**2 == len(grid) else False
        for row_i in range(len(grid)):
            for col_i in range(len(grid)):
                cols = list(range(0,col_i)) + list(range(col_i+1, len(grid)))
                rows = list(range(0, row_i)) + list(range(row_i+1, len(grid)))
                for c in cols:
                    constraints.add(tuple(sorted((f"{row_i+1}-{col_i+1}",f"{row_i+1}-{c+1}"))))
                for r in rows:
                    constraints.add(tuple(sorted((f"{row_i+1}-{col_i+1}",f"{r+1}-{col_i+1}"))))
                if proper_sudoku:
                    top_left_row = (row_i)//region_size * region_size
                    top_left_col = (col_i)//region_size * region_size
                    for i in range(region_size):
                        for j in range(region_size):
                            if top_left_row + i != row_i or top_left_col + j != col_i:
                                constraints.add(tuple(sorted((f"{row_i+1}-{col_i+1}", f"{top_left_row + i + 1}-{top_left_col + j + 1}"))))
        
        constraints = sorted(list(constraints))

        return constraints
    
    def _get_graph(self):
        """
        Reads from stdin and updates the Solver object's domain and constraint variables
        """
        grid = self._get_grid()
        n = len(grid)

        # Domain
        domain = {}
        for row_i, row in enumerate(grid):
            for col_i in range(n):
                if grid[row_i][col_i] == 0: # Blank Cell
                    domain[f"{row_i+1}-{col_i+1}"] = [1,2,3,4,5,6,7,8,9] #doesnt have to be hardcoded but whatever
                else:
                    domain[f"{row_i+1}-{col_i+1}"] = [grid[row_i][col_i]]

        # Constraints
        constraints = self._get_inequality_constraints(grid)

        self.domain = domain
        self.constraints = constraints

        return domain, constraints

    def no_conflict(self, var, value, solution):
        row_i, col_i = map(int, var.split("-"))
        size = math.isqrt(len(self.domain))
        region_size = math.isqrt(size)

        # check horizontal and vertical
        for i in range(1,size+1):
            if i != row_i and solution.get(f"{i}-{col_i}") == value:
                return False    
            
            if i != col_i and solution.get(f"{row_i}-{i}") == value:
                return False
            
        # check region
        top_left_row = (row_i-1) //region_size * region_size + 1
        top_left_col = (col_i-1) //region_size * region_size + 1
        for i in range(region_size):
            for j in range(region_size):
                if top_left_row + i != row_i or top_left_col + j != col_i:
                    if solution.get(f"{top_left_row + i}-{top_left_col + j}") == value:
                        return False
        
        return True

        


    def solve(self):
        """
        Calls _get_graph to update constraint and domain then,
        performs AC3 algorithm for search space reduction then
        backtracking search to find and print the solution.
        """

        self._get_graph()
        reduced_domain = AC3(self.domain, self.constraints)()
        solution = {}
        remaining= []

        # Fix the variables with single valued domains
        for v, d in reduced_domain.items():
            if len(d) == 1:
                solution[v] = d[0]
            else:
                remaining.append(v)
        
        remaining.sort(key=lambda var: len(reduced_domain[var]))

        # Search over the remaining variables
        def search(i):
            # solution found
            if i == len(remaining):
                return True
            
            var = remaining[i]
            d = reduced_domain[var]

            for value in d:
                if self.no_conflict(var, value, solution):
                    solution[var] = value
                    reduced_domain = AC3(reduced_domain, self.constraints)()
                    if search(i+1):
                        return True
                    del solution[var]
                    
            return False

        search(0)
        
        # Print solution
        size = math.isqrt(len(self.domain))

        for i in range(1,size+1):
            row = []
            for j in range(1,size+1):
                key = f"{i}-{j}"
                # get the value from the dict, 0 if not present
                row.append(str(solution[key]))
            print("".join(row))
        

if __name__ == "__main__":
    start_time = time.time()
    solver = Solver()
    solver.solve()

    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time:.4f} seconds")
