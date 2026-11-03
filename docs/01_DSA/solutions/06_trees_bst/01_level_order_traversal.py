"""
================================================================================
PROBLEM: Binary Tree Level Order Traversal (LeetCode 102)
Difficulty: Medium | Pattern: BFS + Tree
================================================================================

PROBLEM STATEMENT:
Given the root of a binary tree, return the level order traversal of its nodes' 
values. (i.e., from left to right, level by level).

EXAMPLES:
    Input: root = [3,9,20,null,null,15,7]
    Output: [[3],[9,20],[15,7]]
    
              3
             / \
            9  20
              /  \
             15   7

    Input: root = [1]
    Output: [[1]]

    Input: root = []
    Output: []

CONSTRAINTS:
- The number of nodes in the tree is in range [0, 2000]
- -1000 <= Node.val <= 1000

================================================================================
"""
from typing import Optional, List
from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================================
# SOLUTION 1: BFS with Queue (Optimal - Standard Approach)
# ============================================================================
def levelOrder(root: Optional[TreeNode]) -> List[List[int]]:
    """
    BFS using queue. Process level by level.
    
    Key: Process all nodes at current level before moving to next.
    
    Time: O(n) - visit each node once
    Space: O(n) - queue holds at most one level (up to n/2 nodes)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)  # Number of nodes at current level
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result


# ============================================================================
# SOLUTION 2: DFS with Level Tracking
# ============================================================================
def levelOrder_dfs(root: Optional[TreeNode]) -> List[List[int]]:
    """
    DFS approach - track level and add to appropriate list.
    
    Time: O(n)
    Space: O(h) for recursion stack, where h = height
    """
    result = []
    
    def dfs(node: TreeNode, level: int) -> None:
        if not node:
            return
        
        # If this is a new level, add empty list
        if level == len(result):
            result.append([])
        
        result[level].append(node.val)
        
        dfs(node.left, level + 1)
        dfs(node.right, level + 1)
    
    dfs(root, 0)
    return result


# ============================================================================
# SOLUTION 3: BFS using Two Lists (No queue)
# ============================================================================
def levelOrder_two_lists(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Use two lists: current level and next level.
    
    Time: O(n)
    Space: O(n)
    """
    if not root:
        return []
    
    result = []
    current_level = [root]
    
    while current_level:
        level_vals = []
        next_level = []
        
        for node in current_level:
            level_vals.append(node.val)
            if node.left:
                next_level.append(node.left)
            if node.right:
                next_level.append(node.right)
        
        result.append(level_vals)
        current_level = next_level
    
    return result


# ============================================================================
# HELPER FUNCTIONS FOR TESTING
# ============================================================================
def build_tree(values: List) -> Optional[TreeNode]:
    """Build tree from level-order list representation"""
    if not values:
        return None
    
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(values):
        node = queue.popleft()
        
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard tree
    root1 = build_tree([3, 9, 20, None, None, 15, 7])
    print(f"Tree: [3,9,20,null,null,15,7]")
    print(f"Level Order (BFS): {levelOrder(root1)}")
    print(f"Level Order (DFS): {levelOrder_dfs(root1)}")
    # Expected: [[3], [9, 20], [15, 7]]
    print()
    
    # Test Case 2: Single node
    root2 = build_tree([1])
    print(f"Tree: [1]")
    print(f"Level Order: {levelOrder(root2)}")
    # Expected: [[1]]
    print()
    
    # Test Case 3: Empty tree
    root3 = build_tree([])
    print(f"Tree: []")
    print(f"Level Order: {levelOrder(root3)}")
    # Expected: []
    print()
    
    # Test Case 4: Skewed tree
    root4 = build_tree([1, 2, None, 3, None, 4])
    print(f"Tree: [1,2,null,3,null,4] (left skewed)")
    print(f"Level Order: {levelOrder(root4)}")
    # Expected: [[1], [2], [3], [4]]
    print()
    
    # Test Case 5: Complete binary tree
    root5 = build_tree([1, 2, 3, 4, 5, 6, 7])
    print(f"Tree: [1,2,3,4,5,6,7]")
    print(f"Level Order: {levelOrder(root5)}")
    # Expected: [[1], [2, 3], [4, 5, 6, 7]]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE BFS TEMPLATE:
   
   queue = deque([root])
   while queue:
       level_size = len(queue)  # CRUCIAL: fix size before loop
       for _ in range(level_size):
           node = queue.popleft()
           # process node
           # add children to queue
   
   This template is used for MANY tree problems!

2. WHY FIX LEVEL SIZE?
   
   We add children WHILE iterating.
   If we don't fix level_size, we'll process next level too.
   
   level_size = len(queue) captures current level count
   BEFORE we add children.

3. BFS VS DFS FOR LEVEL ORDER:
   
   BFS (Queue):
   - Natural level-by-level processing
   - Intuitive for this problem
   - O(n) space for queue
   
   DFS (Recursion):
   - Less intuitive but works
   - Track level number
   - O(h) space for recursion (h = height)
   - Better space for balanced trees (h = log n)

4. VARIATIONS - KNOW THESE:
   
   - Level Order Traversal II (LC 107): Bottom-up → just reverse
   - Zigzag Level Order (LC 103): Alternate direction each level
   - Right Side View (LC 199): Last node of each level
   - Average of Levels (LC 637): Average instead of values

5. THE "PROCESS LEVEL" PATTERN:
   
   This pattern applies to:
   - BFS on trees
   - BFS on graphs (tracking distance)
   - Multi-source BFS
   
   Always useful when you need level/distance info.

6. ZIGZAG VARIATION:
   
   Same template, but:
   - Track direction (left_to_right = True/False)
   - Alternate each level
   - Either reverse level list OR use deque's appendleft

7. SPACE ANALYSIS:
   
   Queue holds at most one level.
   Maximum nodes at a level = n/2 (for complete binary tree)
   
   Result list holds all nodes = O(n)
   
   Total space: O(n)

8. COMMON MISTAKES:
   
   ❌ Not fixing level_size before inner loop
   ❌ Forgetting to check if root is None
   ❌ Using list instead of deque (O(n) popleft)

9. HOW TO EXPLAIN IT:
   
   Start with BFS approach (more intuitive).
   Mention: "I can also solve with DFS by tracking level"
   
   This shows versatility!

10. FOLLOW-UP: BINARY TREE RIGHT SIDE VIEW
    
    Same BFS, but only add LAST node of each level:
    
    for i in range(level_size):
        node = queue.popleft()
        if i == level_size - 1:  # Last node in level
            result.append(node.val)
        # add children...

================================================================================
"""
