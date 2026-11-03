"""
================================================================================
PROBLEM: N-Queens (LeetCode 51)
Difficulty: Hard | Pattern: Backtracking
================================================================================

PROBLEM STATEMENT:
The n-queens puzzle is the problem of placing n queens on an n x n chessboard 
such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle. 
You may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' 
placement, where 'Q' and '.' both indicate a queen and an empty space, 
respectively.

EXAMPLES:
    Input: n = 4
    Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
    
    Visualization of first solution:
    . Q . .
    . . . Q
    Q . . .
    . . Q .

    Input: n = 1
    Output: [["Q"]]

CONSTRAINTS:
- 1 <= n <= 9

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Backtracking with Sets
# ============================================================================
def solveNQueens(n: int) -> List[List[str]]:
    """
    Backtracking: place queen row by row, track attacked columns/diagonals.
    
    Key insight: 
    - Column: just track column number
    - Diagonal (↘): row - col is constant
    - Anti-diagonal (↙): row + col is constant
    
    Time: O(n!)
    Space: O(n) for recursion and sets
    """
    result = []
    cols = set()       # Columns with queens
    diags = set()      # row - col for diagonals
    anti_diags = set() # row + col for anti-diagonals
    
    board = [['.'] * n for _ in range(n)]
    
    def backtrack(row: int) -> None:
        if row == n:
            result.append([''.join(r) for r in board])
            return
        
        for col in range(n):
            diag = row - col
            anti_diag = row + col
            
            # Check if position is safe
            if col in cols or diag in diags or anti_diag in anti_diags:
                continue
            
            # Place queen
            board[row][col] = 'Q'
            cols.add(col)
            diags.add(diag)
            anti_diags.add(anti_diag)
            
            backtrack(row + 1)
            
            # Remove queen (backtrack)
            board[row][col] = '.'
            cols.remove(col)
            diags.remove(diag)
            anti_diags.remove(anti_diag)
    
    backtrack(0)
    return result


# ============================================================================
# SOLUTION 2: Backtracking with Array (No Sets)
# ============================================================================
def solveNQueens_array(n: int) -> List[List[str]]:
    """
    Use arrays instead of sets for O(1) lookup.
    
    Time: O(n!)
    Space: O(n)
    """
    result = []
    queens = [-1] * n  # queens[row] = column of queen in that row
    
    # Arrays for O(1) lookup
    cols = [False] * n
    diags = [False] * (2 * n - 1)      # row - col + (n-1) maps to 0..2n-2
    anti_diags = [False] * (2 * n - 1)  # row + col maps to 0..2n-2
    
    def backtrack(row: int) -> None:
        if row == n:
            board = []
            for r in range(n):
                row_str = ['.'] * n
                row_str[queens[r]] = 'Q'
                board.append(''.join(row_str))
            result.append(board)
            return
        
        for col in range(n):
            diag_idx = row - col + (n - 1)
            anti_idx = row + col
            
            if cols[col] or diags[diag_idx] or anti_diags[anti_idx]:
                continue
            
            queens[row] = col
            cols[col] = True
            diags[diag_idx] = True
            anti_diags[anti_idx] = True
            
            backtrack(row + 1)
            
            cols[col] = False
            diags[diag_idx] = False
            anti_diags[anti_idx] = False
    
    backtrack(0)
    return result


# ============================================================================
# SOLUTION 3: Backtracking with Validation Function
# ============================================================================
def solveNQueens_validate(n: int) -> List[List[str]]:
    """
    Simpler but slower: validate by checking all previous queens.
    
    Time: O(n! × n) - extra n for validation
    Space: O(n)
    """
    result = []
    queens = []  # List of (row, col) positions
    
    def is_safe(row: int, col: int) -> bool:
        for r, c in queens:
            # Same column
            if c == col:
                return False
            # Same diagonal
            if abs(r - row) == abs(c - col):
                return False
        return True
    
    def backtrack(row: int) -> None:
        if row == n:
            board = []
            for r, c in queens:
                row_str = '.' * c + 'Q' + '.' * (n - c - 1)
                board.append(row_str)
            result.append(board)
            return
        
        for col in range(n):
            if is_safe(row, col):
                queens.append((row, col))
                backtrack(row + 1)
                queens.pop()
    
    backtrack(0)
    return result


# ============================================================================
# SOLUTION 4: Count Only (N-Queens II - LC 52)
# ============================================================================
def totalNQueens(n: int) -> int:
    """
    Count solutions without building boards.
    
    Time: O(n!)
    Space: O(n)
    """
    count = 0
    cols = set()
    diags = set()
    anti_diags = set()
    
    def backtrack(row: int) -> None:
        nonlocal count
        
        if row == n:
            count += 1
            return
        
        for col in range(n):
            if col in cols or (row - col) in diags or (row + col) in anti_diags:
                continue
            
            cols.add(col)
            diags.add(row - col)
            anti_diags.add(row + col)
            
            backtrack(row + 1)
            
            cols.remove(col)
            diags.remove(row - col)
            anti_diags.remove(row + col)
    
    backtrack(0)
    return count


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: n = 4
    n1 = 4
    print(f"N-Queens for n = {n1}:")
    solutions = solveNQueens(n1)
    print(f"Number of solutions: {len(solutions)}")
    for i, sol in enumerate(solutions):
        print(f"\nSolution {i + 1}:")
        for row in sol:
            print(row)
    # Expected: 2 solutions
    print()
    
    # Test Case 2: n = 1
    n2 = 1
    print(f"N-Queens for n = {n2}:")
    print(solveNQueens(n2))
    # Expected: [["Q"]]
    print()
    
    # Test Case 3: n = 8 (classic problem)
    n3 = 8
    print(f"N-Queens for n = {n3}:")
    print(f"Number of solutions: {totalNQueens(n3)}")
    # Expected: 92 solutions
    print()
    
    # Test Case 4: Count for various n
    for n in range(1, 10):
        print(f"n = {n}: {totalNQueens(n)} solutions")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE DIAGONAL INSIGHT (CRUCIAL!):
   
   For a square at (row, col):
   - Diagonal (↘): row - col is constant
   - Anti-diagonal (↙): row + col is constant
   
   Example for 4×4:
   row-col:        row+col:
   0  -1  -2  -3    0   1   2   3
   1   0  -1  -2    1   2   3   4
   2   1   0  -1    2   3   4   5
   3   2   1   0    3   4   5   6

2. WHY PLACE ROW BY ROW?
   
   Each row must have exactly one queen.
   By going row by row, we only need to check columns
   and diagonals, not rows.

3. WHAT TO TRACK:
   
   - cols: which columns have queens
   - diags: which (row - col) values have queens
   - anti_diags: which (row + col) values have queens
   
   All O(1) lookup with set or array.

4. TIME COMPLEXITY:
   
   Upper bound: O(n!)
   - Row 0: n choices
   - Row 1: at most n-1 valid choices
   - ...
   
   Actually less due to diagonal constraints.

5. BOARD REPRESENTATION:
   
   Option 1: 2D array of chars
   Option 2: Array queens[row] = col
   
   Second is more memory efficient.

6. BUILDING OUTPUT:
   
   After finding valid placement, build board:
   
   for each row:
       '.' * col + 'Q' + '.' * (n - col - 1)

7. COMMON MISTAKES:
   
   ❌ Forgetting to backtrack (remove from sets)
   ❌ Wrong diagonal formula
   ❌ Checking rows (unnecessary if going row by row)

8. N-QUEENS II (LC 52):
   
   Just count solutions, don't build boards.
   Same algorithm, simpler output.

9. KNOWN COUNTS:
   
   n=1: 1, n=2: 0, n=3: 0, n=4: 2
   n=5: 10, n=6: 4, n=7: 40, n=8: 92

10. HOW TO EXPLAIN IT:
    
    "I'll place queens row by row. For each row, I try each
    column and check if it's safe using three sets:
    
    - cols: columns already used
    - diags: row - col values (main diagonal)
    - anti_diags: row + col values (anti-diagonal)
    
    The key insight is that squares on the same diagonal
    have the same row - col value, and squares on the
    same anti-diagonal have the same row + col value."
    
    Draw the diagonal pattern if asked!

================================================================================
"""
