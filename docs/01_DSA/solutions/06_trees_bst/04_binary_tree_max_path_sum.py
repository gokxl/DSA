"""
================================================================================
PROBLEM: Binary Tree Maximum Path Sum (LeetCode 124)
Difficulty: Hard | Pattern: Tree DFS
================================================================================

PROBLEM STATEMENT:
A path in a binary tree is a sequence of nodes where each pair of adjacent 
nodes in the sequence has an edge connecting them. A node can only appear in 
the sequence at most once. Note that the path does not need to pass through 
the root.

The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any non-empty 
path.

EXAMPLES:
    Input: root = [1,2,3]
    Output: 6
    Explanation: The optimal path is 2 -> 1 -> 3 with sum = 2 + 1 + 3 = 6.
    
          1
         / \
        2   3

    Input: root = [-10,9,20,null,null,15,7]
    Output: 42
    Explanation: The optimal path is 15 -> 20 -> 7 with sum = 42.
    
         -10
         / \
        9  20
          /  \
         15   7

CONSTRAINTS:
- The number of nodes in the tree is in range [1, 3 * 10^4]
- -1000 <= Node.val <= 1000

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
def maxPathSum(root: Optional[TreeNode]) -> int:
    """
    At each node, calculate:
    1. Max path through this node (left + node + right) - for global max
    2. Max path starting from this node going down - for parent's calculation
    
    Key insight: Path through node can "turn" at node (use both children)
    but path TO parent can only go one way.
    
    Time: O(n) - visit each node once
    Space: O(h) - recursion stack
    """
    max_sum = float('-inf')
    
    def max_gain(node: TreeNode) -> int:
        """
        Returns max sum of path starting at this node going DOWN.
        Also updates global max considering paths that "turn" at this node.
        """
        nonlocal max_sum
        
        if not node:
            return 0
        
        # Max sum from left and right children
        # Use max(0, ...) to handle negative sums - we can choose not to extend
        left_gain = max(0, max_gain(node.left))
        right_gain = max(0, max_gain(node.right))
        
        # Path that turns at this node: left_child <- node -> right_child
        path_through_node = node.val + left_gain + right_gain
        
        # Update global maximum
        max_sum = max(max_sum, path_through_node)
        
        # Return max path starting at node going to ONE side only
        # (because parent can only connect to one path)
        return node.val + max(left_gain, right_gain)
    
    max_gain(root)
    return max_sum


# ============================================================================
# SOLUTION 2: Without Global Variable (Using tuple)
# ============================================================================
def maxPathSum_tuple(root: Optional[TreeNode]) -> int:
    """
    Same logic, but avoid global variable by returning tuple.
    Returns (max_sum_so_far, max_gain_starting_here)
    
    Time: O(n)
    Space: O(h)
    """
    def helper(node: TreeNode) -> tuple:
        """Returns (global_max, max_starting_from_node)"""
        if not node:
            return float('-inf'), 0
        
        # Get results from children
        left_max, left_gain = helper(node.left)
        right_max, right_gain = helper(node.right)
        
        # Don't extend if negative
        left_gain = max(0, left_gain)
        right_gain = max(0, right_gain)
        
        # Path through this node
        path_through_node = node.val + left_gain + right_gain
        
        # Global max is best of: left subtree, right subtree, or through this node
        current_max = max(left_max, right_max, path_through_node)
        
        # Max path starting from this node
        max_starting_here = node.val + max(left_gain, right_gain)
        
        return current_max, max_starting_here
    
    return helper(root)[0]


# ============================================================================
# SOLUTION 3: Iterative Postorder (More complex)
# ============================================================================
def maxPathSum_iterative(root: Optional[TreeNode]) -> int:
    """
    Iterative postorder traversal.
    Process children before parent.
    
    Time: O(n)
    Space: O(n) for hash map
    """
    if not root:
        return 0
    
    max_sum = float('-inf')
    gains = {None: 0}  # Map node -> max gain starting from node
    
    stack = [(root, False)]  # (node, is_processed)
    
    while stack:
        node, processed = stack.pop()
        
        if processed:
            # Children have been processed
            left_gain = max(0, gains.get(node.left, 0))
            right_gain = max(0, gains.get(node.right, 0))
            
            # Update global max
            max_sum = max(max_sum, node.val + left_gain + right_gain)
            
            # Store gain for this node
            gains[node] = node.val + max(left_gain, right_gain)
        else:
            # First visit - add children first (postorder)
            stack.append((node, True))
            if node.right:
                stack.append((node.right, False))
            if node.left:
                stack.append((node.left, False))
    
    return max_sum


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
    # Test Case 1: Simple tree
    root1 = build_tree([1, 2, 3])
    print(f"Tree: [1,2,3]")
    print(f"Max Path Sum: {maxPathSum(root1)}")
    # Expected: 6 (path: 2 -> 1 -> 3)
    print()
    
    # Test Case 2: Negative root
    root2 = build_tree([-10, 9, 20, None, None, 15, 7])
    print(f"Tree: [-10,9,20,null,null,15,7]")
    print(f"Max Path Sum: {maxPathSum(root2)}")
    # Expected: 42 (path: 15 -> 20 -> 7)
    print()
    
    # Test Case 3: All negative
    root3 = build_tree([-3])
    print(f"Tree: [-3]")
    print(f"Max Path Sum: {maxPathSum(root3)}")
    # Expected: -3 (must include at least one node)
    print()
    
    # Test Case 4: Mixed values
    root4 = build_tree([2, -1, -2])
    print(f"Tree: [2,-1,-2]")
    print(f"Max Path Sum: {maxPathSum(root4)}")
    # Expected: 2 (just the root)
    print()
    
    # Test Case 5: Using tuple approach
    root5 = build_tree([1, 2, 3])
    print(f"Max Path Sum (Tuple): {maxPathSum_tuple(root5)}")
    # Expected: 6


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. TWO TYPES OF PATHS TO CONSIDER:
   
   At each node, calculate TWO things:
   
   a) Path THROUGH node (left -> node -> right)
      - Can use both children
      - Contributes to global max
      - Path "turns" at this node
   
   b) Path FROM node going DOWN
      - Can only use ONE child (left OR right)
      - This is what we return to parent
      - Parent can extend this path

2. THE KEY INSIGHT:
   
   For parent:
       parent
         |
       node
       /  \
     left  right
   
   Parent can only extend path through ONE branch from node.
   Can't go: parent -> node -> left AND parent -> node -> right
   
   But for global max, we CAN have: left -> node -> right

3. HANDLING NEGATIVE VALUES:
   
   left_gain = max(0, max_gain(node.left))
   
   If child's max gain is negative, don't extend!
   We can just use the node alone.
   
   This is like Kadane's algorithm concept.

4. VISUAL EXAMPLE:
   
        -10
        / \
       9  20
         /  \
        15   7
   
   At node 20:
   - left_gain = 15, right_gain = 7
   - path_through = 20 + 15 + 7 = 42 ← global max!
   - return to parent: 20 + max(15, 7) = 35
   
   At node -10:
   - left_gain = 9, right_gain = 35
   - path_through = -10 + 9 + 35 = 34 (not max)
   - Best is still 42

5. WHY WE USE max(0, gain):
   
   If subtree has negative max gain, better to not include it.
   
   Tree: [2, -1]
   At 2: left_gain = max(0, -1) = 0
   path_through = 2 + 0 = 2
   
   Better than 2 + (-1) = 1

6. COMPARISON TO SIMILAR PROBLEMS:
   
   - Maximum Subarray (Kadane's): Similar max(0, prev) logic
   - Diameter of Binary Tree: Same two-path concept
   - Path Sum problems: Path tracking

7. COMMON MISTAKES:
   
   ❌ Returning path_through_node instead of one-sided gain
   ❌ Not handling negative values with max(0, ...)
   ❌ Confusing global max vs return value

8. ITERATIVE APPROACH:
   
   Requires postorder (process children before parent).
   More complex - use hash map to store gains.
   Recursive is cleaner for practice sessions.

9. EDGE CASES:
   
   - Single node (answer is that node's value)
   - All negative values (must include at least one node)
   - Root is optimal path

10. practice TIP:
    
    Explain the two concepts clearly:
    "At each node, I track two things:
    1. The max path that turns here (for global answer)
    2. The max path going down (for parent's use)
    
    The key insight is that a path can turn at most once,
    so for parent I can only offer one direction."
    
    Draw a small tree and trace through values!

================================================================================
"""
