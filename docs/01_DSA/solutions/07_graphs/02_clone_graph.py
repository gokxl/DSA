"""
================================================================================
PROBLEM: Clone Graph (LeetCode 133)
Difficulty: Medium | Pattern: Graph DFS/BFS
================================================================================

PROBLEM STATEMENT:
Given a reference of a node in a connected undirected graph, return a deep copy 
(clone) of the graph.

Each node in the graph contains a value (int) and a list (List[Node]) of its 
neighbors.

class Node {
    public int val;
    public List<Node> neighbors;
}

EXAMPLES:
    Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
    Output: [[2,4],[1,3],[2,4],[1,3]]
    
    Node 1 connects to 2 and 4
    Node 2 connects to 1 and 3
    Node 3 connects to 2 and 4
    Node 4 connects to 1 and 3
    
        1 --- 2
        |     |
        4 --- 3

    Input: adjList = [[]]
    Output: [[]]
    Explanation: Graph has one node with value 1 and no neighbors.

    Input: adjList = []
    Output: []
    Explanation: Empty graph.

CONSTRAINTS:
- The number of nodes in the graph is in range [0, 100]
- 1 <= Node.val <= 100
- Node.val is unique for each node
- There are no repeated edges and no self-loops
- The Graph is connected and all nodes can be visited from the given node

================================================================================
"""
from typing import Optional, Dict
from collections import deque


# Definition for a Node.
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


# ============================================================================
# SOLUTION 1: DFS with HashMap (Optimal)
# ============================================================================
def cloneGraph(node: Optional['Node']) -> Optional['Node']:
    """
    DFS approach using HashMap to track cloned nodes.
    
    HashMap: original node -> cloned node
    
    Time: O(N + E) where N = nodes, E = edges
    Space: O(N) for HashMap and recursion stack
    """
    if not node:
        return None
    
    # Map original node to its clone
    cloned = {}
    
    def dfs(original: Node) -> Node:
        # If already cloned, return the clone
        if original in cloned:
            return cloned[original]
        
        # Create clone
        clone = Node(original.val)
        cloned[original] = clone
        
        # Clone neighbors recursively
        for neighbor in original.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)


# ============================================================================
# SOLUTION 2: BFS with HashMap
# ============================================================================
def cloneGraph_bfs(node: Optional['Node']) -> Optional['Node']:
    """
    BFS approach - clone level by level.
    
    Time: O(N + E)
    Space: O(N)
    """
    if not node:
        return None
    
    # Map original node to its clone
    cloned = {node: Node(node.val)}
    queue = deque([node])
    
    while queue:
        original = queue.popleft()
        
        for neighbor in original.neighbors:
            if neighbor not in cloned:
                # Clone the neighbor
                cloned[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            
            # Add cloned neighbor to current clone's neighbors
            cloned[original].neighbors.append(cloned[neighbor])
    
    return cloned[node]


# ============================================================================
# SOLUTION 3: DFS without explicit HashMap (Using node.val as key)
# ============================================================================
def cloneGraph_val_map(node: Optional['Node']) -> Optional['Node']:
    """
    Since node.val is unique, we can use it as key.
    
    Time: O(N + E)
    Space: O(N)
    """
    if not node:
        return None
    
    val_to_clone = {}
    
    def dfs(original: Node) -> Node:
        if original.val in val_to_clone:
            return val_to_clone[original.val]
        
        clone = Node(original.val)
        val_to_clone[original.val] = clone
        
        for neighbor in original.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)


# ============================================================================
# HELPER FUNCTIONS FOR TESTING
# ============================================================================
def build_graph(adj_list: list) -> Optional[Node]:
    """Build graph from adjacency list"""
    if not adj_list:
        return None
    
    nodes = {i: Node(i) for i in range(1, len(adj_list) + 1)}
    
    for i, neighbors in enumerate(adj_list, 1):
        nodes[i].neighbors = [nodes[n] for n in neighbors]
    
    return nodes[1]


def graph_to_adj_list(node: Optional[Node]) -> list:
    """Convert graph to adjacency list for verification"""
    if not node:
        return []
    
    visited = {}
    queue = deque([node])
    visited[node.val] = node
    
    while queue:
        curr = queue.popleft()
        for neighbor in curr.neighbors:
            if neighbor.val not in visited:
                visited[neighbor.val] = neighbor
                queue.append(neighbor)
    
    result = []
    for i in range(1, len(visited) + 1):
        result.append([n.val for n in visited[i].neighbors])
    
    return result


def verify_clone(original: Node, clone: Node) -> bool:
    """Verify that clone is a deep copy"""
    if not original and not clone:
        return True
    if not original or not clone:
        return False
    
    visited = set()
    queue = deque([(original, clone)])
    
    while queue:
        orig, cln = queue.popleft()
        
        if id(orig) in visited:
            continue
        visited.add(id(orig))
        
        # Value should match but objects should be different
        if orig.val != cln.val:
            return False
        if orig is cln:  # Should be different objects!
            return False
        if len(orig.neighbors) != len(cln.neighbors):
            return False
        
        for o_neighbor, c_neighbor in zip(orig.neighbors, cln.neighbors):
            queue.append((o_neighbor, c_neighbor))
    
    return True


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard graph (4 nodes in cycle)
    adj_list1 = [[2, 4], [1, 3], [2, 4], [1, 3]]
    print(f"Original: {adj_list1}")
    graph1 = build_graph(adj_list1)
    clone1 = cloneGraph(graph1)
    print(f"Clone (DFS): {graph_to_adj_list(clone1)}")
    print(f"Is valid deep copy: {verify_clone(graph1, clone1)}")
    print()
    
    # Test Case 2: Single node with no neighbors
    adj_list2 = [[]]
    print(f"Original: {adj_list2}")
    graph2 = build_graph(adj_list2)
    clone2 = cloneGraph_bfs(graph2)
    print(f"Clone (BFS): {graph_to_adj_list(clone2)}")
    print()
    
    # Test Case 3: Empty graph
    print(f"Empty graph: {cloneGraph(None)}")
    # Expected: None
    print()
    
    # Test Case 4: Two connected nodes
    adj_list4 = [[2], [1]]
    print(f"Original: {adj_list4}")
    graph4 = build_graph(adj_list4)
    clone4 = cloneGraph(graph4)
    print(f"Clone: {graph_to_adj_list(clone4)}")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHY WE NEED A HASHMAP:
   
   Graph has cycles! Without tracking visited/cloned nodes:
   - We'd create infinite clones
   - Or infinite recursion
   
   HashMap: original node -> cloned node
   - Prevents revisiting
   - Allows connecting to already-cloned nodes

2. THE DFS PATTERN:
   
   def clone(node):
       if node in cloned:
           return cloned[node]  # Already cloned
       
       clone = Node(node.val)
       cloned[node] = clone     # Map BEFORE recursing!
       
       for neighbor in node.neighbors:
           clone.neighbors.append(clone(neighbor))
       
       return clone

3. CRITICAL: MAP BEFORE RECURSING!
   
   cloned[node] = clone  # Do this FIRST
   
   Why? When we recurse into neighbors, they might
   point back to this node. We need the clone to exist!

4. BFS VS DFS:
   
   Both work well here. DFS is often cleaner.
   
   DFS: Clone node, then clone its neighbors recursively
   BFS: Clone layer by layer, connect neighbors as we go

5. WHAT IS "DEEP COPY"?
   
   - New Node objects (different memory addresses)
   - Same values and structure
   - No references to original graph
   
   Verify: original_node is not cloned_node

6. USING NODE.VAL AS KEY:
   
   Since vals are unique (per constraints), we can use:
   val_to_clone[node.val] instead of cloned[node]
   
   But using node itself is more robust.

7. RELATED PROBLEMS:
   
   - Copy List with Random Pointer (LC 138)
   - Clone Binary Tree with Random Pointer (LC 1485)
   - Deep Copy of HashMap with Linked List Values

8. COMMON MISTAKES:
   
   ❌ Not mapping before recursing (infinite loop)
   ❌ Mapping value instead of node object
   ❌ Returning original node instead of clone

9. QUESTIONS TO CLARIFY:
   
   Ask: "Is the graph connected?" (Usually yes)
   Ask: "Are node values unique?" (Usually yes)
   Ask: "Can there be self-loops?" (Usually no)

10. HOW TO EXPLAIN IT:
    
    Explain the HashMap role clearly:
    
    "The HashMap serves two purposes:
    1. Track visited nodes (avoid infinite loops in cycles)
    2. Map original to clone (so neighbors can find clones)
    
    I add to the map BEFORE recursing to handle back-edges."

================================================================================
"""
