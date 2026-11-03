"""
================================================================================
PROBLEM: Pacific Atlantic Water Flow (LeetCode 417)
Difficulty: Medium | Pattern: Graph DFS/BFS
================================================================================

PROBLEM STATEMENT:
There is an m x n rectangular island that borders both the Pacific Ocean and 
Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, 
and the Atlantic Ocean touches the island's right and bottom edges.

The island is partitioned into a grid of square cells. You are given an m x n 
integer matrix heights where heights[r][c] represents the height above sea 
level of the cell at coordinate (r, c).

The island receives a lot of rain, and the rain water can flow to neighboring 
cells directly north, south, east, and west if the neighboring cell's height 
is less than or equal to the current cell's height. Water can flow from any 
cell adjacent to an ocean into the ocean.

Return a 2D list of grid coordinates result where result[i] = [ri, ci] denotes 
that rain water can flow from cell (ri, ci) to both the Pacific and Atlantic 
oceans.

EXAMPLES:
    Input: heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
    Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
    
    Pacific ~ ~ ~ ~ ~
          ~ 1 2 2 3 (5) ~
          ~ 3 2 3 (4)(4) ~
          ~ 2 4 (5) 3 1 ~
          ~(6)(7) 1 4 5 ~
          ~(5) 1 1 2 4 ~
              ~ ~ ~ ~ ~ Atlantic
    
    Cells that can reach both oceans are marked with ()

    Input: heights = [[1]]
    Output: [[0,0]]

CONSTRAINTS:
- m == heights.length
- n == heights[r].length
- 1 <= m, n <= 200
- 0 <= heights[r][c] <= 10^5

================================================================================
"""
from typing import List
from collections import deque


# ============================================================================
# SOLUTION 1: DFS from Ocean Borders (Optimal)
# ============================================================================
def pacificAtlantic(heights: List[List[int]]) -> List[List[int]]:
    """
    Reverse the problem: Start from oceans, go uphill.
    
    Find cells reachable from Pacific.
    Find cells reachable from Atlantic.
    Return intersection.
    
    Time: O(m × n)
    Space: O(m × n)
    """
    if not heights or not heights[0]:
        return []
    
    rows, cols = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()
    
    def dfs(r: int, c: int, visited: set, prev_height: int) -> None:
        # Out of bounds, already visited, or can't flow uphill
        if (r < 0 or r >= rows or c < 0 or c >= cols or 
            (r, c) in visited or heights[r][c] < prev_height):
            return
        
        visited.add((r, c))
        
        # Explore all 4 directions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, visited, heights[r][c])
    
    # Start DFS from Pacific border (top row and left column)
    for c in range(cols):
        dfs(0, c, pacific, 0)  # Top row
    for r in range(rows):
        dfs(r, 0, pacific, 0)  # Left column
    
    # Start DFS from Atlantic border (bottom row and right column)
    for c in range(cols):
        dfs(rows - 1, c, atlantic, 0)  # Bottom row
    for r in range(rows):
        dfs(r, cols - 1, atlantic, 0)  # Right column
    
    # Return intersection
    return [[r, c] for r, c in pacific & atlantic]


# ============================================================================
# SOLUTION 2: BFS from Ocean Borders
# ============================================================================
def pacificAtlantic_bfs(heights: List[List[int]]) -> List[List[int]]:
    """
    Same approach using BFS instead of DFS.
    
    Time: O(m × n)
    Space: O(m × n)
    """
    if not heights or not heights[0]:
        return []
    
    rows, cols = len(heights), len(heights[0])
    
    def bfs(starts: List[tuple]) -> set:
        """BFS from starting positions, going uphill"""
        visited = set(starts)
        queue = deque(starts)
        
        while queue:
            r, c = queue.popleft()
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                
                if (0 <= nr < rows and 0 <= nc < cols and 
                    (nr, nc) not in visited and 
                    heights[nr][nc] >= heights[r][c]):  # Can go uphill
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        
        return visited
    
    # Pacific: top row + left column
    pacific_starts = [(0, c) for c in range(cols)] + [(r, 0) for r in range(1, rows)]
    pacific = bfs(pacific_starts)
    
    # Atlantic: bottom row + right column
    atlantic_starts = [(rows-1, c) for c in range(cols)] + [(r, cols-1) for r in range(rows-1)]
    atlantic = bfs(atlantic_starts)
    
    return [[r, c] for r, c in pacific & atlantic]


# ============================================================================
# SOLUTION 3: Naive DFS from each cell (Less efficient)
# ============================================================================
def pacificAtlantic_naive(heights: List[List[int]]) -> List[List[int]]:
    """
    For each cell, check if it can reach both oceans.
    Less efficient but more intuitive.
    
    Time: O((m × n)²) - worst case
    Space: O(m × n)
    """
    if not heights or not heights[0]:
        return []
    
    rows, cols = len(heights), len(heights[0])
    result = []
    
    def can_reach(r: int, c: int, visited: set) -> tuple:
        """Returns (can_reach_pacific, can_reach_atlantic)"""
        if (r, c) in visited:
            return False, False
        
        # Check if at ocean border
        pacific = (r == 0 or c == 0)
        atlantic = (r == rows - 1 or c == cols - 1)
        
        visited.add((r, c))
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if (0 <= nr < rows and 0 <= nc < cols and 
                (nr, nc) not in visited and 
                heights[nr][nc] <= heights[r][c]):  # Flow downhill
                
                p, a = can_reach(nr, nc, visited)
                pacific = pacific or p
                atlantic = atlantic or a
        
        return pacific, atlantic
    
    for r in range(rows):
        for c in range(cols):
            p, a = can_reach(r, c, set())
            if p and a:
                result.append([r, c])
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    heights1 = [
        [1, 2, 2, 3, 5],
        [3, 2, 3, 4, 4],
        [2, 4, 5, 3, 1],
        [6, 7, 1, 4, 5],
        [5, 1, 1, 2, 4]
    ]
    print("Heights:")
    for row in heights1:
        print(row)
    result1 = pacificAtlantic(heights1)
    print(f"DFS Result: {sorted(result1)}")
    # Expected: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
    print()
    
    # Test Case 2: Single cell
    heights2 = [[1]]
    print(f"Heights: {heights2}")
    print(f"Result: {pacificAtlantic(heights2)}")
    # Expected: [[0,0]]
    print()
    
    # Test Case 3: Using BFS
    heights3 = [[1, 2, 3], [8, 9, 4], [7, 6, 5]]
    print("Heights:")
    for row in heights3:
        print(row)
    print(f"BFS Result: {sorted(pacificAtlantic_bfs(heights3))}")
    print()
    
    # Test Case 4: All same height
    heights4 = [[1, 1], [1, 1]]
    print(f"All same: {pacificAtlantic(heights4)}")
    # Expected: All cells


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE KEY INSIGHT - REVERSE THE DIRECTION:
   
   Instead of: "From each cell, can water reach ocean?"
   Think: "From ocean, which cells can water reach going UPHILL?"
   
   This changes O((m×n)²) to O(m×n)!

2. WHY REVERSE WORKS:
   
   Water flows downhill: A → B if height[A] >= height[B]
   Reverse: B can reach A going uphill
   
   Start from ocean, go uphill = find all cells that drain to ocean

3. TWO SEPARATE TRAVERSALS:
   
   1. From Pacific (top + left) → find all cells draining to Pacific
   2. From Atlantic (bottom + right) → find all cells draining to Atlantic
   3. Intersection = answer

4. OCEAN BORDERS:
   
   Pacific: row 0 (top) + column 0 (left)
   Atlantic: row m-1 (bottom) + column n-1 (right)
   
   Corner cells touch both!

5. UPHILL CONDITION:
   
   heights[nr][nc] >= heights[r][c]
   
   We're going FROM ocean TO cells (reverse of water flow).

6. DFS VS BFS:
   
   Both work well here.
   DFS: Cleaner recursive code
   BFS: Better for finding shortest path (not needed here)

7. COMMON MISTAKES:
   
   ❌ Starting from each cell (O(n²×m²))
   ❌ Wrong direction (downhill vs uphill)
   ❌ Missing corner cells in ocean borders

8. VISUALIZATION:
   
   Pacific Ocean
   ~  ~  ~  ~  ~
   ~ [1][2][2][3][5] ~
   ~ [3][2][3][4][4] ~
   ~ [2][4][5][3][1] ~
   ~ [6][7][1][4][5] ~
   ~ [5][1][1][2][4] ~
      ~  ~  ~  ~  ~
        Atlantic Ocean

9. RELATED PROBLEMS:
   
   - Number of Islands (LC 200)
   - Surrounded Regions (LC 130)
   - Walls and Gates (LC 286)
   - Rotting Oranges (LC 994)

10. HOW TO EXPLAIN IT:
    
    "The naive approach checks from each cell - O(n²×m²).
    
    I'll reverse the problem: start from oceans and see
    which cells can reach them going uphill. This is O(n×m).
    
    I'll do two traversals - one from Pacific border,
    one from Atlantic border - and return the intersection."
    
    This shows optimization thinking!

================================================================================
"""
