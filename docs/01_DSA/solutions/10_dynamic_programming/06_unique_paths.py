"""
================================================================================
PROBLEM: Unique Paths (LeetCode 62)
Difficulty: Medium | Pattern: DP (2D)
================================================================================

PROBLEM STATEMENT:
There is a robot on an m x n grid. The robot is initially located at the top-left 
corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner 
(i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any 
point in time.

Given the two integers m and n, return the number of possible unique paths that 
the robot can take to reach the bottom-right corner.

EXAMPLES:
    Input: m = 3, n = 7
    Output: 28

    Input: m = 3, n = 2
    Output: 3
    Explanation: There are 3 ways:
    1. Right -> Down -> Down
    2. Down -> Down -> Right
    3. Down -> Right -> Down

CONSTRAINTS:
- 1 <= m, n <= 100

================================================================================
"""
from typing import List
from math import comb


# ============================================================================
# SOLUTION 1: 2D DP
# ============================================================================
def uniquePaths_2d(m: int, n: int) -> int:
    """
    dp[i][j] = number of paths to reach (i, j)
    dp[i][j] = dp[i-1][j] + dp[i][j-1] (from above + from left)
    
    Time: O(m × n)
    Space: O(m × n)
    """
    dp = [[1] * n for _ in range(m)]
    
    # First row and first column are all 1s (only one way to reach)
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    
    return dp[m - 1][n - 1]


# ============================================================================
# SOLUTION 2: 1D DP (Space Optimized)
# ============================================================================
def uniquePaths(m: int, n: int) -> int:
    """
    Only need previous row, so use 1D array.
    
    Time: O(m × n)
    Space: O(n)
    """
    dp = [1] * n
    
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]  # dp[j] already has from above
    
    return dp[n - 1]


# ============================================================================
# SOLUTION 3: Math (Combinatorics)
# ============================================================================
def uniquePaths_math(m: int, n: int) -> int:
    """
    Total moves: (m-1) down + (n-1) right = m+n-2 moves
    Need to choose which (m-1) are down moves.
    
    Answer = C(m+n-2, m-1) = C(m+n-2, n-1)
    
    Time: O(min(m, n))
    Space: O(1)
    """
    return comb(m + n - 2, m - 1)


# ============================================================================
# SOLUTION 4: Math (Manual calculation)
# ============================================================================
def uniquePaths_manual_math(m: int, n: int) -> int:
    """
    Calculate C(m+n-2, m-1) without using math.comb.
    
    C(n, r) = n! / (r! × (n-r)!)
    
    Time: O(min(m, n))
    Space: O(1)
    """
    # Choose smaller of m-1 or n-1 for fewer iterations
    if m < n:
        m, n = n, m  # Ensure m >= n
    
    # Calculate C(m+n-2, n-1)
    numerator = 1
    denominator = 1
    
    for i in range(n - 1):
        numerator *= (m + n - 2 - i)
        denominator *= (i + 1)
    
    return numerator // denominator


# ============================================================================
# SOLUTION 5: Memoization
# ============================================================================
def uniquePaths_memo(m: int, n: int) -> int:
    """
    Top-down with memoization.
    
    Time: O(m × n)
    Space: O(m × n)
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> int:
        if i == 0 or j == 0:
            return 1
        return dp(i - 1, j) + dp(i, j - 1)
    
    return dp(m - 1, n - 1)


# ============================================================================
# UNIQUE PATHS II (LC 63) - With obstacles
# ============================================================================
def uniquePathsWithObstacles(obstacleGrid: List[List[int]]) -> int:
    """
    Same as Unique Paths but with obstacles (1 = obstacle).
    
    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    
    if obstacleGrid[0][0] == 1:
        return 0
    
    dp = [0] * n
    dp[0] = 1
    
    for i in range(m):
        for j in range(n):
            if obstacleGrid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]
    
    return dp[n - 1]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    m1, n1 = 3, 7
    print(f"m = {m1}, n = {n1}")
    print(f"2D DP: {uniquePaths_2d(m1, n1)}")
    print(f"1D DP: {uniquePaths(m1, n1)}")
    print(f"Math: {uniquePaths_math(m1, n1)}")
    # Expected: 28
    print()
    
    # Test Case 2: Small grid
    m2, n2 = 3, 2
    print(f"m = {m2}, n = {n2}")
    print(f"Result: {uniquePaths(m2, n2)}")
    # Expected: 3
    print()
    
    # Test Case 3: Single row
    m3, n3 = 1, 5
    print(f"m = {m3}, n = {n3}")
    print(f"Result: {uniquePaths(m3, n3)}")
    # Expected: 1
    print()
    
    # Test Case 4: Square grid
    m4, n4 = 5, 5
    print(f"m = {m4}, n = {n4}")
    print(f"Result: {uniquePaths(m4, n4)}")
    # Expected: 70
    print()
    
    # Test Case 5: With obstacles
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    print(f"Grid with obstacle: {grid}")
    print(f"Result: {uniquePathsWithObstacles(grid)}")
    # Expected: 2


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. RECURRENCE:
   
   dp[i][j] = dp[i-1][j] + dp[i][j-1]
   
   "Paths to (i,j) = paths from above + paths from left"

2. BASE CASE:
   
   First row: all 1s (can only come from left)
   First column: all 1s (can only come from above)

3. SPACE OPTIMIZATION:
   
   Only need previous row, so use 1D array:
   
   dp[j] += dp[j-1]
   
   dp[j] already contains value from above (previous iteration).

4. MATH SOLUTION (OPTIMAL!):
   
   Total moves = (m-1) down + (n-1) right
   Choose which (m-1) moves are down.
   
   Answer = C(m+n-2, m-1)
   
   This is O(min(m,n)) time, O(1) space!

5. WHY COMBINATORICS WORKS:
   
   Every path is a sequence of (m-1) D's and (n-1) R's.
   Example for 2×3: "DR", "RD" are the only paths.
   
   Count = ways to arrange (m-1) D's among (m+n-2) moves.

6. UNIQUE PATHS II (OBSTACLES):
   
   If cell has obstacle: dp[i][j] = 0
   Otherwise: same recurrence
   
   Handle obstacle at start: return 0 if obstacleGrid[0][0] == 1

7. COMMON MISTAKES:
   
   ❌ Forgetting first row/column are 1s
   ❌ Off-by-one in dimensions
   ❌ Not handling obstacle at start

8. RELATED PROBLEMS:
   
   - Unique Paths II (LC 63)
   - Minimum Path Sum (LC 64)
   - Dungeon Game (LC 174)
   - Out of Boundary Paths (LC 576)

9. FOLLOW-UP: COUNT SPECIFIC PATH:
   
   If you need to track the actual path:
   - Store parent pointers during DP
   - Backtrack from (m-1, n-1) to (0, 0)

10. HOW TO EXPLAIN IT:
    
    "This is a classic grid DP. Each cell's path count is
    the sum of paths from above and from left.
    
    dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    Space optimization: only need 1D array since we process
    row by row.
    
    Even better: This is pure combinatorics! We need (m-1)
    down moves and (n-1) right moves. Answer is C(m+n-2, m-1).
    This gives O(min(m,n)) time and O(1) space."

================================================================================
"""
