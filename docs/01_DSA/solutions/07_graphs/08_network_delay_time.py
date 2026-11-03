"""
================================================================================
PROBLEM: Network Delay Time (LeetCode 743)
Difficulty: Medium | Pattern: Dijkstra's Algorithm
================================================================================

PROBLEM STATEMENT:
You are given a network of n nodes, labeled from 1 to n. You are also given 
times, a list of travel times as directed edges times[i] = (ui, vi, wi), where 
ui is the source node, vi is the target node, and wi is the time it takes for 
a signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes 
for all the n nodes to receive the signal. If it is impossible for all the n 
nodes to receive the signal, return -1.

EXAMPLES:
    Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
    Output: 2
    
    From node 2:
    - Node 1: 1 time (direct)
    - Node 3: 1 time (direct)
    - Node 4: 2 time (via node 3)
    
    All nodes reached in time 2.

    Input: times = [[1,2,1]], n = 2, k = 1
    Output: 1

    Input: times = [[1,2,1]], n = 2, k = 2
    Output: -1
    Explanation: Node 1 can't be reached from node 2.

CONSTRAINTS:
- 1 <= k <= n <= 100
- 1 <= times.length <= 6000
- times[i].length == 3
- 1 <= ui, vi <= n
- ui != vi
- 0 <= wi <= 100
- All pairs (ui, vi) are unique

================================================================================
"""
from typing import List
import heapq
from collections import defaultdict


# ============================================================================
# SOLUTION 1: Dijkstra's Algorithm (Optimal)
# ============================================================================
def networkDelayTime(times: List[List[int]], n: int, k: int) -> int:
    """
    Dijkstra's algorithm to find shortest path to all nodes.
    Answer is the maximum of all shortest paths.
    
    Time: O(E log V) where E = edges, V = nodes
    Space: O(V + E)
    """
    # Build adjacency list
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    # Min-heap: (distance, node)
    min_heap = [(0, k)]
    dist = {}  # node -> shortest distance from k
    
    while min_heap:
        d, node = heapq.heappop(min_heap)
        
        if node in dist:
            continue  # Already found shorter path
        
        dist[node] = d
        
        for neighbor, weight in graph[node]:
            if neighbor not in dist:
                heapq.heappush(min_heap, (d + weight, neighbor))
    
    # Check if all nodes reachable
    if len(dist) != n:
        return -1
    
    return max(dist.values())


# ============================================================================
# SOLUTION 2: Bellman-Ford Algorithm
# ============================================================================
def networkDelayTime_bellman_ford(times: List[List[int]], n: int, k: int) -> int:
    """
    Bellman-Ford algorithm - handles negative weights (not needed here).
    Relax all edges n-1 times.
    
    Time: O(V × E)
    Space: O(V)
    """
    dist = [float('inf')] * (n + 1)
    dist[k] = 0
    
    # Relax all edges n-1 times
    for _ in range(n - 1):
        for u, v, w in times:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    
    # Find maximum distance
    max_dist = max(dist[1:n+1])  # Nodes are 1-indexed
    
    return max_dist if max_dist != float('inf') else -1


# ============================================================================
# SOLUTION 3: BFS/SPFA (Shortest Path Faster Algorithm)
# ============================================================================
from collections import deque

def networkDelayTime_spfa(times: List[List[int]], n: int, k: int) -> int:
    """
    SPFA - optimized Bellman-Ford using queue.
    Only relax nodes that were updated.
    
    Time: O(V × E) worst case, often faster
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    dist = [float('inf')] * (n + 1)
    dist[k] = 0
    
    queue = deque([k])
    in_queue = [False] * (n + 1)
    in_queue[k] = True
    
    while queue:
        node = queue.popleft()
        in_queue[node] = False
        
        for neighbor, weight in graph[node]:
            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                
                if not in_queue[neighbor]:
                    queue.append(neighbor)
                    in_queue[neighbor] = True
    
    max_dist = max(dist[1:n+1])
    return max_dist if max_dist != float('inf') else -1


# ============================================================================
# SOLUTION 4: Floyd-Warshall (For reference - all pairs shortest path)
# ============================================================================
def networkDelayTime_floyd(times: List[List[int]], n: int, k: int) -> int:
    """
    Floyd-Warshall - finds shortest paths between ALL pairs.
    Overkill for this problem but good to know.
    
    Time: O(V³)
    Space: O(V²)
    """
    # Initialize distance matrix
    dist = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        dist[i][i] = 0
    
    for u, v, w in times:
        dist[u][v] = w
    
    # Floyd-Warshall
    for mid in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if dist[i][mid] + dist[mid][j] < dist[i][j]:
                    dist[i][j] = dist[i][mid] + dist[mid][j]
    
    max_dist = max(dist[k][1:n+1])
    return max_dist if max_dist != float('inf') else -1


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    times1 = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    n1, k1 = 4, 2
    print(f"Times: {times1}, n={n1}, k={k1}")
    print(f"Dijkstra: {networkDelayTime(times1, n1, k1)}")
    print(f"Bellman-Ford: {networkDelayTime_bellman_ford(times1, n1, k1)}")
    # Expected: 2
    print()
    
    # Test Case 2: Direct connection
    times2 = [[1, 2, 1]]
    n2, k2 = 2, 1
    print(f"Times: {times2}, n={n2}, k={k2}")
    print(f"Result: {networkDelayTime(times2, n2, k2)}")
    # Expected: 1
    print()
    
    # Test Case 3: Unreachable node
    times3 = [[1, 2, 1]]
    n3, k3 = 2, 2
    print(f"Times: {times3}, n={n3}, k={k3}")
    print(f"Result: {networkDelayTime(times3, n3, k3)}")
    # Expected: -1
    print()
    
    # Test Case 4: Complex network
    times4 = [[1, 2, 1], [2, 3, 2], [1, 3, 4]]
    n4, k4 = 3, 1
    print(f"Times: {times4}, n={n4}, k={k4}")
    print(f"Result: {networkDelayTime(times4, n4, k4)}")
    # Expected: 3 (1->2->3 = 3 is shorter than 1->3 = 4)
    print()
    
    # Test Case 5: Using SPFA
    times5 = [[1, 2, 1], [2, 1, 3]]
    n5, k5 = 2, 2
    print(f"SPFA: {networkDelayTime_spfa(times5, n5, k5)}")
    # Expected: 3


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THIS IS DIJKSTRA'S ALGORITHM:
   
   Single-source shortest path with non-negative weights.
   
   Use min-heap to always process closest unvisited node.
   Greedily expand from source to find shortest paths.

2. WHY THE ANSWER IS MAX(DISTANCES)?
   
   "Minimum time for ALL nodes to receive signal"
   = Time when the LAST node receives it
   = Maximum shortest path distance
   
   All nodes must be reached simultaneously for the slowest.

3. DIJKSTRA'S TEMPLATE:
   
   heap = [(0, source)]
   dist = {}
   
   while heap:
       d, node = heappop(heap)
       if node in dist: continue
       dist[node] = d
       
       for neighbor, weight in graph[node]:
           if neighbor not in dist:
               heappush(heap, (d + weight, neighbor))

4. TIME COMPLEXITY COMPARISON:
   
   Dijkstra: O(E log V) - optimal for sparse graphs
   Bellman-Ford: O(V × E) - handles negative weights
   Floyd-Warshall: O(V³) - all pairs shortest path
   
   For this problem, Dijkstra is best.

5. WHEN TO USE EACH ALGORITHM:
   
   Dijkstra: Non-negative weights, single source
   Bellman-Ford: Can have negative weights, detect negative cycles
   Floyd-Warshall: Need all pairs shortest paths
   BFS: Unweighted graphs

6. DIJKSTRA GOTCHA:
   
   DON'T update dist immediately when pushing to heap.
   A node might be added multiple times with different distances.
   Only update dist when POPPING (first pop = shortest).

7. 1-INDEXED NODES:
   
   Nodes are labeled 1 to n, not 0 to n-1.
   Be careful with array indexing!

8. COMMON MISTAKES:
   
   ❌ Updating distance when pushing (not popping)
   ❌ Not checking if all nodes reachable
   ❌ Returning total distance instead of max

9. RELATED PROBLEMS:
   
   - Cheapest Flights Within K Stops (LC 787) - modified Dijkstra
   - Path With Minimum Effort (LC 1631) - binary search + BFS
   - Swim in Rising Water (LC 778) - binary search or Dijkstra

10. HOW TO EXPLAIN IT:
    
    "This is shortest path from single source - classic Dijkstra.
    
    I use a min-heap to always process the closest unvisited node.
    The answer is the maximum shortest path since we need all
    nodes to receive the signal.
    
    Time is O(E log V) with heap-based Dijkstra."
    
    Know Bellman-Ford as follow-up for negative weights!

================================================================================
"""
