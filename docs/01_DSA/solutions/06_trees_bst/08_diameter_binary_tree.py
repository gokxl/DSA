"""
================================================================================
PROBLEM: Diameter of Binary Tree (LeetCode 543)
Difficulty: Easy | Pattern: Tree DFS
================================================================================

PROBLEM STATEMENT:
Given the root of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any 
two nodes in a tree. This path may or may not pass through the root.

The length of a path between two nodes is represented by the number of EDGES 
between them.

EXAMPLES:
    Input: root = [1,2,3,4,5]
    Output: 3
    
          1
         / \
        2   3
       / \
      4   5
    
    Explanation: Longest path is 4 -> 2 -> 1 -> 3 or 5 -> 2 -> 1 -> 3 (3 edges)

    Input: root = [1,2]
    Output: 1
    
    Explanation: Path is 2 -> 1 (1 edge)

CONSTRAINTS:
- The number of nodes in the tree is in range [1, 10^4]
- -100 <= Node.val <= 100

================================================================================
"""
from typing import Optional
from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================================
# SOLUTION 1: DFS with Global Max (Optimal)
# ============================================================================
def diameterOfBinaryTree(root: Optional[TreeNode]) -> int:
    """
    At each node:
    - Diameter through this node = left_height + right_height
    - Return height to parent = 1 + max(left, right)
    
    Similar pattern to Binary Tree Maximum Path Sum!
    
    Time: O(n) - visit each node once
    Space: O(h) - recursion stack
    """
    diameter = 0
    
    def height(node: TreeNode) -> int:
        """Returns height (number of edges to deepest leaf)"""
        nonlocal diameter
        
        if not node:
            return 0
        
        # Height of left and right subtrees
        left_h = height(node.left)
        right_h = height(node.right)
        
        # Diameter through this node = left_height + right_height
        diameter = max(diameter, left_h + right_h)
        
        # Return height of this subtree
        return 1 + max(left_h, right_h)
    
    height(root)
    return diameter


# ============================================================================
# SOLUTION 2: Without Global Variable (Tuple return)
# ============================================================================
def diameterOfBinaryTree_tuple(root: Optional[TreeNode]) -> int:
    """
    Return both (diameter_so_far, height) to avoid global variable.
    
    Time: O(n)
    Space: O(h)
    """
    def helper(node: TreeNode) -> tuple:
        """Returns (max_diameter_in_subtree, height)"""
        if not node:
            return 0, 0
        
        left_diam, left_h = helper(node.left)
        right_diam, right_h = helper(node.right)
        
        # Diameter through this node
        through_node = left_h + right_h
        
        # Best diameter so far
        best_diameter = max(left_diam, right_diam, through_node)
        
        # Height of this subtree
        height = 1 + max(left_h, right_h)
        
        return best_diameter, height
    
    return helper(root)[0]


# ============================================================================
# SOLUTION 3: Iterative Postorder (More complex)
# ============================================================================
def diameterOfBinaryTree_iterative(root: Optional[TreeNode]) -> int:
    """
    Iterative postorder: process children before parent.
    Store heights in dictionary.
    
    Time: O(n)
    Space: O(n)
    """
    if not root:
        return 0
    
    diameter = 0
    heights = {None: 0}
    stack = [(root, False)]
    
    while stack:
        node, processed = stack.pop()
        
        if processed:
            # Children already processed
            left_h = heights.get(node.left, 0)
            right_h = heights.get(node.right, 0)
            
            diameter = max(diameter, left_h + right_h)
            heights[node] = 1 + max(left_h, right_h)
        else:
            # First visit - process children first
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
    
    return diameter


# ============================================================================
# HELPER FUNCTIONS FOR TESTING
# ============================================================================
def build_tree(values) -> Optional[TreeNode]:
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
    root1 = build_tree([1, 2, 3, 4, 5])
    print(f"Tree: [1,2,3,4,5]")
    print(f"Diameter (Global): {diameterOfBinaryTree(root1)}")
    print(f"Diameter (Tuple): {diameterOfBinaryTree_tuple(root1)}")
    # Expected: 3 (path: 4->2->1->3 or 5->2->1->3)
    print()
    
    # Test Case 2: Two nodes
    root2 = build_tree([1, 2])
    print(f"Tree: [1,2]")
    print(f"Diameter: {diameterOfBinaryTree(root2)}")
    # Expected: 1
    print()
    
    # Test Case 3: Single node
    root3 = build_tree([1])
    print(f"Tree: [1]")
    print(f"Diameter: {diameterOfBinaryTree(root3)}")
    # Expected: 0
    print()
    
    # Test Case 4: Longest path doesn't go through root
    #        1
    #       /
    #      2
    #     / \
    #    3   4
    #   /     \
    #  5       6
    root4 = build_tree([1, 2, None, 3, 4, 5, None, None, 6])
    print(f"Tree: [1,2,null,3,4,5,null,null,6]")
    print(f"Diameter: {diameterOfBinaryTree(root4)}")
    # Expected: 4 (path: 5->3->2->4->6)
    print()
    
    # Test Case 5: Iterative method
    root5 = build_tree([1, 2, 3, 4, 5])
    print(f"Diameter (Iterative): {diameterOfBinaryTree_iterative(root5)}")
    # Expected: 3


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE KEY INSIGHT - TWO CONCEPTS:
   
   At each node, we calculate:
   
   a) DIAMETER through node = left_height + right_height
      (This contributes to our answer)
   
   b) HEIGHT of subtree = 1 + max(left_height, right_height)
      (This is what we return to parent)
   
   Same pattern as Binary Tree Maximum Path Sum!

2. WHY DIAMETER = left_h + right_h:
   
   Diameter through node = longest path that "turns" at this node
   
          1
         / \
        2   3
       /
      4
   
   At node 2: left_h=1 (to 4), right_h=0
   Diameter through 2 = 1 + 0 = 1
   
   At node 1: left_h=2 (to 4), right_h=1 (to 3)
   Diameter through 1 = 2 + 1 = 3 ← Max!

3. EDGES VS NODES:
   
   Problem asks for EDGES, not nodes.
   
   Path 4 -> 2 -> 1 -> 3 has:
   - 4 nodes
   - 3 edges ← This is the answer
   
   That's why diameter = left_h + right_h (not +1)

4. PATH DOESN'T HAVE TO GO THROUGH ROOT:
   
   Example:
          1
         /
        2
       / \
      3   4
   
   Diameter = 2 (path: 3 -> 2 -> 4)
   This doesn't go through root!

5. SIMILARITY TO MAX PATH SUM:
   
   Both problems:
   - Track global max during DFS
   - Calculate "through node" value for global
   - Return "one-sided" value to parent
   
   This is a COMMON PATTERN!

6. COMMON MISTAKES:
   
   ❌ Only considering paths through root
   ❌ Counting nodes instead of edges
   ❌ Not updating global max at each node

7. HEIGHT DEFINITION:
   
   Height = number of edges to deepest leaf
   
   Leaf: height = 0 (returns 0)
   One above leaf: height = 1
   
   Note: Some define height as nodes, adjust accordingly!

8. FOLLOW-UP: FIND THE ACTUAL PATH
   
   Store parent pointers or track the nodes that form
   the diameter path. More complex but same core logic.

9. RELATED PROBLEMS:
   
   - Binary Tree Maximum Path Sum (LC 124) - Same pattern!
   - Longest Univalue Path (LC 687)
   - Maximum Depth of Binary Tree (LC 104)

10. HOW TO EXPLAIN IT:
    
    "This is similar to Max Path Sum - at each node I track
    two things: the diameter through this node (for global max)
    and the height (for parent's calculation).
    
    Diameter = left_height + right_height (edges to each side)
    Height to return = 1 + max(left, right)"
    
    Show the connection to other problems!

================================================================================
"""
