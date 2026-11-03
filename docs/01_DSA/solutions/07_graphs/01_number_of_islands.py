"""
================================================================================
PROBLEM: Number of Islands (LeetCode 200)
Difficulty: Medium | Pattern: Graph DFS/BFS
================================================================================

PROBLEM STATEMENT:
Given an m x n 2D binary grid which represents a map of '1's (land) and 
'0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands 
horizontally or vertically. You may assume all four edges of the grid are 
surrounded by water.

EXAMPLES:
    Input: grid = [
      ["1","1","1","1","0"],
      ["1","1","0","1","0"],
      ["1","1","0","0","0"],
      ["0","0","0","0","0"]
    ]
    Output: 1

    Input: grid = [
      ["1","1","0","0","0"],
      ["1","1","0","0","0"],
      ["0","0","1","0","0"],
      ["0","0","0","1","1"]
    ]
    Output: 3

CONSTRAINTS:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 300
- grid[i][j] is '0' or '1'

================================================================================
"""
from typing import List
from collections import deque


# ============================================================================
# SOLUTION 1: DFS (Optimal & Most Common)
# ============================================================================
def numIslands(grid: List[List[str]]) -> int:
    """
    DFS to explore and mark each island.
    When we find a '1', DFS to mark entire island, increment count.
    
    Time: O(m * n) - visit each cell once
    Space: O(m * n) - recursion stack in worst case (all land)
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r: int, c: int) -> None:
        # Boundary and water check
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        
        # Mark as visited (sink the island)
        grid[r][c] = '0'
        
        # Explore all 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)  # Sink the entire island
    
    return count


# ============================================================================
# SOLUTION 2: BFS
# ============================================================================
def numIslands_bfs(grid: List[List[str]]) -> int:
    """
    BFS to explore each island level by level.
    
    Time: O(m * n)
    Space: O(min(m, n)) - queue size
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def bfs(start_r: int, start_c: int) -> None:
        queue = deque([(start_r, start_c)])
        grid[start_r][start_c] = '0'
        
        while queue:
            r, c = queue.popleft()
            
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '0'  # Mark BEFORE adding to queue
                    queue.append((nr, nc))
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                bfs(r, c)
    
    return count


# ============================================================================
# SOLUTION 3: Union-Find (Alternative approach)
# ============================================================================
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = 0
    
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x: int, y: int) -> None:
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        self.count -= 1  # Merged two components


def numIslands_union_find(grid: List[List[str]]) -> int:
    """
    Union-Find approach. Good for dynamic connectivity queries.
    
    Time: O(m * n * α(m * n)) ≈ O(m * n)
    Space: O(m * n)
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    uf = UnionFind(rows * cols)
    
    # Count initial land cells
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                uf.count += 1
    
    # Union adjacent land cells
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                idx = r * cols + c
                
                # Only need to check right and down (avoid duplicates)
                if c + 1 < cols and grid[r][c + 1] == '1':
                    uf.union(idx, idx + 1)
                if r + 1 < rows and grid[r + 1][c] == '1':
                    uf.union(idx, idx + cols)
    
    return uf.count


# ============================================================================
# SOLUTION 4: DFS without Recursion (Iterative DFS)
# ============================================================================
def numIslands_iterative_dfs(grid: List[List[str]]) -> int:
    """
    Iterative DFS using stack to avoid stack overflow.
    
    Time: O(m * n)
    Space: O(m * n) for stack
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                
                # Iterative DFS
                stack = [(r, c)]
                grid[r][c] = '0'
                
                while stack:
                    cr, cc = stack.pop()
                    
                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nr, nc = cr + dr, cc + dc
                        
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'
                            stack.append((nr, nc))
    
    return count


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: One island
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    print("Grid 1:")
    for row in grid1:
        print(row)
    # Make copies since we modify grid
    grid1_copy = [row[:] for row in grid1]
    print(f"DFS: {numIslands(grid1)}")
    # Expected: 1
    print()
    
    # Test Case 2: Three islands
    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    print("Grid 2:")
    for row in grid2:
        print(row)
    grid2_copy = [row[:] for row in grid2]
    print(f"BFS: {numIslands_bfs(grid2)}")
    # Expected: 3
    print()
    
    # Test Case 3: No islands
    grid3 = [["0","0"],["0","0"]]
    print(f"Empty grid: {numIslands(grid3)}")
    # Expected: 0
    print()
    
    # Test Case 4: All land
    grid4 = [["1","1"],["1","1"]]
    print(f"All land: {numIslands(grid4)}")
    # Expected: 1


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE CORE IDEA - FLOOD FILL:
   
   When we find a '1' (land):
   1. Increment island count
   2. "Sink" the entire island (mark all connected '1's as '0')
   
   This ensures we count each island only once.

2. WHY MODIFY INPUT?
   
   Instead of using a visited set:
   - Mark visited cells as '0' directly
   - Saves O(m*n) space
   
   Ask interviewer: "Can I modify the input grid?"
   If not, use a visited set.

3. THE 4-DIRECTIONAL PATTERN:
   
   directions = [(1,0), (-1,0), (0,1), (0,-1)]
   
   OR in DFS:
   dfs(r+1, c)
   dfs(r-1, c)
   dfs(r, c+1)
   dfs(r, c-1)
   
   This is used in MANY grid problems!

4. BFS GOTCHA - MARK BEFORE ENQUEUEING:
   
   ❌ Wrong: Mark when dequeuing
   ✓ Right: Mark when adding to queue
   
   Why? Multiple cells might add same neighbor!
   
   grid[nr][nc] = '0'  # Mark BEFORE
   queue.append((nr, nc))

5. DFS VS BFS FOR THIS PROBLEM:
   
   DFS:
   - Simpler code (recursive)
   - Can stack overflow for huge grids
   - Use iterative DFS for safety
   
   BFS:
   - No stack overflow risk
   - Slightly more code
   - Better for distance problems

6. WHEN TO USE UNION-FIND:
   
   - Dynamic connectivity (cells added/removed)
   - Multiple queries about connectivity
   - Finding connected components
   
   For single "count islands", DFS/BFS is simpler.

7. RELATED PROBLEMS:
   
   - Max Area of Island (LC 695)
   - Surrounded Regions (LC 130)
   - Number of Distinct Islands (LC 694)
   - Word Search (LC 79)

8. COMMON MISTAKES:
   
   ❌ Not checking boundaries
   ❌ BFS: marking after dequeue (duplicate visits)
   ❌ DFS: stack overflow on large grids

9. TIME COMPLEXITY EXPLANATION:
   
   O(m * n) because:
   - We iterate through grid once: O(m * n)
   - Each cell is visited at most once by DFS/BFS
   - Even though DFS seems nested, total visits = O(m * n)

10. practice TIP:
    
    Start with recursive DFS (cleanest).
    Mention: "For very large grids, I'd use iterative DFS
    or BFS to avoid stack overflow."
    
    If asked about dynamic queries, mention Union-Find.

================================================================================
"""
