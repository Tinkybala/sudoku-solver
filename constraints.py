import sys
import math
from typing import List, Tuple

def get_grid() -> List[List[int]]:
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


def get_inequality_constraints(grid: List[List[int]]) -> List[Tuple[str, str]]:
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





def get_graph():
    """
    Reads from stdin and prints out the answer to a) in proper format
    """
    grid = get_grid()
    n = len(grid)
    k = n*n

    # Domain
    domain = {}
    for row_i, row in enumerate(grid):
        for col_i in range(n):
            if grid[row_i][col_i] == 0: # Blank Cell
                domain[f"{row_i+1}-{col_i+1}"] = [1,2,3,4,5,6,7,8,9]
            else:
                domain[f"{row_i+1}-{col_i+1}"] = [grid[row_i][col_i]]

    # Constraints
    constraints = get_inequality_constraints(grid)

    # Do the printing
    print(k)
    for key, value in domain.items():
        value = " ".join(map(str, value))
        print(f"{key} {value}")
    print(len(constraints))

    
    for c in constraints:
        print(f"1 {c[0]} {c[1]}")
    




if __name__ == "__main__":
    get_graph()