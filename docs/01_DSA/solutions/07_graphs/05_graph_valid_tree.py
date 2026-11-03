"""
================================================================================
PROBLEM: Graph Valid Tree (LeetCode 261)
Difficulty: Medium | Pattern: Graph + Union-Find
================================================================================

PROBLEM STATEMENT:
Given n nodes labeled from 0 to n-1 and a list of undirected edges (each edge 
is a pair of nodes), write a function to check whether these edges make up a 
valid tree.

A valid tree must satisfy:
1. The graph is fully connected (all nodes reachable from any node)
2. The graph has no cycles

EXAMPLES:
    Input: n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
    Output: true
    
        0
       /|\
      1 2 3
      |
      4

    Input: n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
    Output: false
    Explanation: Cycle exists: 1-2-3-1

CONSTRAINTS:
- 1 <= n <= 2000
- 0 <= edges.length <= 5000
- edges[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- There are no self-loops or repeated edges

================================================================================
"""
from typing import List
from collections import defaultdict, deque


# ============================================================================
# SOLUTION 1: Union-Find (Optimal)
# ============================================================================
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n
    
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """Returns False if x and y already connected (cycle!)"""
        px, py = self.find(x), self.find(y)
        
        if px == py:
            return False  # Already connected = cycle
        
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        self.components -= 1
        return True


def validTree_union_find(n: int, edges: List[List[int]]) -> bool:
    """
    Use Union-Find to detect cycles and check connectivity.
    
    Tree property: n nodes, n-1 edges, no cycles, connected
    
    Time: O(E × α(N)) ≈ O(E)
    Space: O(N)
    """
    # Tree must have exactly n-1 edges
    if len(edges) != n - 1:
        return False
    
    uf = UnionFind(n)
    
    for a, b in edges:
        if not uf.union(a, b):
            return False  # Cycle detected
    
    return True  # n-1 edges and no cycle means connected tree


# ============================================================================
# SOLUTION 2: DFS (Check connectivity and cycles)
# ============================================================================
def validTree_dfs(n: int, edges: List[List[int]]) -> bool:
    """
    DFS to check for cycles and connectivity.
    
    Tree: connected, no cycles
    
    Time: O(N + E)
    Space: O(N + E)
    """
    # Tree must have exactly n-1 edges
    if len(edges) != n - 1:
        return False
    
    # Build adjacency list
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    
    # DFS to check all nodes are reachable and no cycles
    visited = set()
    
    def dfs(node: int, parent: int) -> bool:
        """Returns False if cycle detected"""
        if node in visited:
            return False  # Cycle!
        
        visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor == parent:
                continue  # Don't go back to parent
            if not dfs(neighbor, node):
                return False
        
        return True
    
    # Start DFS from node 0
    if not dfs(0, -1):
        return False
    
    # Check all nodes visited (connected)
    return len(visited) == n


# ============================================================================
# SOLUTION 3: BFS
# ============================================================================
def validTree_bfs(n: int, edges: List[List[int]]) -> bool:
    """
    BFS approach - same logic as DFS.
    
    Time: O(N + E)
    Space: O(N + E)
    """
    if len(edges) != n - 1:
        return False
    
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    
    visited = set([0])
    queue = deque([(0, -1)])  # (node, parent)
    
    while queue:
        node, parent = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor == parent:
                continue
            if neighbor in visited:
                return False  # Cycle
            visited.add(neighbor)
            queue.append((neighbor, node))
    
    return len(visited) == n


# ============================================================================
# SOLUTION 4: Simple Edge Count Check
# ============================================================================
def validTree_simple(n: int, edges: List[List[int]]) -> bool:
    """
    Simplified: If n-1 edges and all nodes connected, it's a tree.
    
    Use Union-Find just to check connectivity (simpler logic).
    
    Time: O(E × α(N))
    Space: O(N)
    """
    if len(edges) != n - 1:
        return False
    
    # With exactly n-1 edges, if connected then must be a tree
    # Just need to verify connectivity
    
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    for a, b in edges:
        parent[find(a)] = find(b)
    
    # Check all nodes have same root
    root = find(0)
    return all(find(i) == root for i in range(n))


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Valid tree
    n1, edges1 = 5, [[0, 1], [0, 2], [0, 3], [1, 4]]
    print(f"n={n1}, edges={edges1}")
    print(f"Valid Tree (Union-Find): {validTree_union_find(n1, edges1)}")
    print(f"Valid Tree (DFS): {validTree_dfs(n1, edges1)}")
    # Expected: True
    print()
    
    # Test Case 2: Has cycle
    n2, edges2 = 5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]
    print(f"n={n2}, edges={edges2}")
    print(f"Valid Tree (Union-Find): {validTree_union_find(n2, edges2)}")
    print(f"Valid Tree (BFS): {validTree_bfs(n2, edges2)}")
    # Expected: False (cycle: 1-2-3-1)
    print()
    
    # Test Case 3: Not connected
    n3, edges3 = 4, [[0, 1], [2, 3]]
    print(f"n={n3}, edges={edges3}")
    print(f"Valid Tree: {validTree_union_find(n3, edges3)}")
    # Expected: False (2 components)
    print()
    
    # Test Case 4: Single node
    n4, edges4 = 1, []
    print(f"n={n4}, edges={edges4}")
    print(f"Valid Tree: {validTree_union_find(n4, edges4)}")
    # Expected: True
    print()
    
    # Test Case 5: Two nodes
    n5, edges5 = 2, [[0, 1]]
    print(f"n={n5}, edges={edges5}")
    print(f"Valid Tree: {validTree_dfs(n5, edges5)}")
    # Expected: True


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. TREE PROPERTIES (IMPORTANT!):
   
   For n nodes, a valid tree has:
   - Exactly n-1 edges
   - No cycles
   - Fully connected
   
   Any TWO of these implies the third!
   
   So: n-1 edges + no cycles → must be connected (tree)
       n-1 edges + connected → must be acyclic (tree)

2. THE QUICK CHECK:
   
   if len(edges) != n - 1:
       return False
   
   With wrong edge count:
   - More edges → cycle exists
   - Fewer edges → not connected

3. UNION-FIND APPROACH:
   
   Process each edge:
   - If nodes already connected → CYCLE
   - Otherwise, union them
   
   After processing: Check component count = 1

4. DFS/BFS CYCLE DETECTION:
   
   Track parent to avoid false cycle detection:
   
   for neighbor in graph[node]:
       if neighbor == parent:
           continue  # Going back to parent is NOT a cycle
       if neighbor in visited:
           return False  # Real cycle!

5. WHY PARENT TRACKING?
   
   In undirected graph:
   A - B
   
   When at B coming from A:
   - A is in visited
   - But A is parent, not a cycle!
   
   Without parent check, we'd incorrectly detect cycles.

6. UNION-FIND VS DFS/BFS:
   
   Union-Find:
   - Natural for connectivity problems
   - Easy cycle detection during union
   - O(E × α(N)) ≈ O(E)
   
   DFS/BFS:
   - Need to build adjacency list first
   - Explicit cycle and connectivity check
   - O(N + E)
   
   Both are good for practice sessions!

7. RELATED PROBLEMS:
   
   - Number of Connected Components (LC 323)
   - Redundant Connection (LC 684)
   - Minimum Spanning Tree

8. COMMON MISTAKES:
   
   ❌ Forgetting parent check in DFS (false cycle detection)
   ❌ Not checking n-1 edges first
   ❌ Checking cycle but not connectivity

9. EDGE CASES:
   
   - Single node (n=1, edges=[]) → True
   - Two nodes, no edge → False (not connected)
   - Self-loop → Not allowed per constraints

10. practice TIP:
    
    "A valid tree has exactly n-1 edges.
    I'll first check edge count - if wrong, return false.
    
    Then I'll use Union-Find: for each edge, if nodes
    are already connected, that's a cycle, return false.
    
    If we process all edges without cycles and have n-1
    edges, the graph must be connected - it's a tree."

================================================================================
"""
