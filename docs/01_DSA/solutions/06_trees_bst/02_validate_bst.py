"""
================================================================================
PROBLEM: Validate Binary Search Tree (LeetCode 98)
Difficulty: Medium | Pattern: BST + DFS
================================================================================

PROBLEM STATEMENT:
Given the root of a binary tree, determine if it is a valid binary search tree.

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys LESS THAN the node.
- The right subtree of a node contains only nodes with keys GREATER THAN the node.
- Both the left and right subtrees must also be binary search trees.

EXAMPLES:
    Input: root = [2,1,3]
    Output: true
    
              2
             / \
            1   3

    Input: root = [5,1,4,null,null,3,6]
    Output: false
    Explanation: Root's right child is 4 but left subtree contains 3 < 5.
    
              5
             / \
            1   4
               / \
              3   6

CONSTRAINTS:
- The number of nodes in the tree is in range [1, 10^4]
- -2^31 <= Node.val <= 2^31 - 1

================================================================================
"""
from typing import Optional
import math


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================================
# SOLUTION 1: Recursive with Range Bounds (Optimal)
# ============================================================================
def isValidBST(root: Optional[TreeNode]) -> bool:
    """
    Each node must be within a valid range.
    Left child: (min, parent.val)
    Right child: (parent.val, max)
    
    Time: O(n) - visit each node once
    Space: O(h) - recursion stack, h = height
    """
    def validate(node: TreeNode, min_val: float, max_val: float) -> bool:
        if not node:
            return True
        
        # Node value must be strictly within bounds
        if node.val <= min_val or node.val >= max_val:
            return False
        
        # Check left subtree (update max to current node)
        # Check right subtree (update min to current node)
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    
    return validate(root, float('-inf'), float('inf'))


# ============================================================================
# SOLUTION 2: Inorder Traversal (BST Property)
# ============================================================================
def isValidBST_inorder(root: Optional[TreeNode]) -> bool:
    """
    BST inorder traversal produces sorted sequence.
    Verify that each value is greater than the previous.
    
    Time: O(n)
    Space: O(h) for recursion
    """
    prev = float('-inf')
    
    def inorder(node: TreeNode) -> bool:
        nonlocal prev
        
        if not node:
            return True
        
        # Check left subtree
        if not inorder(node.left):
            return False
        
        # Check current node against previous
        if node.val <= prev:
            return False
        prev = node.val
        
        # Check right subtree
        return inorder(node.right)
    
    return inorder(root)


# ============================================================================
# SOLUTION 3: Iterative Inorder with Stack
# ============================================================================
def isValidBST_iterative(root: Optional[TreeNode]) -> bool:
    """
    Iterative inorder traversal.
    Check that values are strictly increasing.
    
    Time: O(n)
    Space: O(h)
    """
    stack = []
    prev = float('-inf')
    curr = root
    
    while stack or curr:
        # Go to leftmost
        while curr:
            stack.append(curr)
            curr = curr.left
        
        # Process node
        curr = stack.pop()
        
        if curr.val <= prev:
            return False
        prev = curr.val
        
        # Go right
        curr = curr.right
    
    return True


# ============================================================================
# SOLUTION 4: BFS with Bounds (Level Order)
# ============================================================================
from collections import deque

def isValidBST_bfs(root: Optional[TreeNode]) -> bool:
    """
    BFS approach - track bounds at each node.
    
    Time: O(n)
    Space: O(n)
    """
    if not root:
        return True
    
    # Queue stores (node, min_bound, max_bound)
    queue = deque([(root, float('-inf'), float('inf'))])
    
    while queue:
        node, min_val, max_val = queue.popleft()
        
        if node.val <= min_val or node.val >= max_val:
            return False
        
        if node.left:
            queue.append((node.left, min_val, node.val))
        if node.right:
            queue.append((node.right, node.val, max_val))
    
    return True


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
    # Test Case 1: Valid BST
    root1 = build_tree([2, 1, 3])
    print(f"Tree: [2,1,3]")
    print(f"Valid BST (Range): {isValidBST(root1)}")
    print(f"Valid BST (Inorder): {isValidBST_inorder(root1)}")
    # Expected: True
    print()
    
    # Test Case 2: Invalid BST
    root2 = build_tree([5, 1, 4, None, None, 3, 6])
    print(f"Tree: [5,1,4,null,null,3,6]")
    print(f"Valid BST: {isValidBST(root2)}")
    # Expected: False (3 < 5 but in right subtree)
    print()
    
    # Test Case 3: Tricky case - all left children valid but violates ancestor
    # Tree:     5
    #          / \
    #         4   6
    #        /   / \
    #       3   3   7
    # 6's left child 3 < 5, invalid!
    root3 = build_tree([5, 4, 6, 3, None, 3, 7])
    print(f"Tree: [5,4,6,3,null,3,7]")
    print(f"Valid BST: {isValidBST(root3)}")
    # Expected: False
    print()
    
    # Test Case 4: Single node
    root4 = build_tree([1])
    print(f"Tree: [1]")
    print(f"Valid BST: {isValidBST(root4)}")
    # Expected: True
    print()
    
    # Test Case 5: Equal values (invalid in strict BST)
    root5 = build_tree([2, 2, 2])
    print(f"Tree: [2,2,2]")
    print(f"Valid BST: {isValidBST(root5)}")
    # Expected: False (strict inequality required)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE COMMON MISTAKE:
   
   ❌ Only checking node.left.val < node.val < node.right.val
   
   This misses:
         5
        / \
       1   4     <- 4 > 1, 4 < 5, BUT...
          / \
         3   6   <- 3 is in RIGHT subtree of 5, must be > 5!
   
   ✓ Every node in right subtree must be > root
   ✓ Every node in left subtree must be < root

2. THE RANGE BOUND APPROACH:
   
   Each node has valid range (min, max):
   - Root: (-∞, +∞)
   - Left child of X: (current_min, X.val)
   - Right child of X: (X.val, current_max)
   
   This propagates constraints down the tree.

3. WHY INORDER WORKS:
   
   BST inorder = sorted sequence!
   
   For valid BST [2,1,3]:
   Inorder: 1, 2, 3 → strictly increasing ✓
   
   For invalid [5,1,4,null,null,3,6]:
   Inorder: 1, 5, 3, 4, 6 → 5 > 3, not sorted ✗

4. STRICT INEQUALITY:
   
   "LESS THAN" not "LESS THAN OR EQUAL"
   
   node.val <= min_val → False (not <)
   
   Some BSTs allow duplicates, clarify with interviewer!

5. HANDLING INTEGER OVERFLOW:
   
   Node values can be INT_MIN or INT_MAX.
   Use float('-inf') and float('inf') for bounds.
   
   In other languages, use Long.MIN_VALUE etc.

6. RECURSIVE VS ITERATIVE:
   
   Range approach:
   - Intuitive, easy to explain
   - Handles all cases naturally
   
   Inorder approach:
   - Uses BST property directly
   - Good to mention as alternative

7. COMMON VARIATIONS:
   
   - Find kth smallest (LC 230)
   - Inorder successor (LC 285)
   - Recover BST (LC 99)
   - Convert BST to sorted doubly linked list

8. TIME/SPACE ANALYSIS:
   
   All approaches: O(n) time
   
   Space:
   - Recursive: O(h) where h = height
   - Balanced tree: O(log n)
   - Skewed tree: O(n)

9. DEBUGGING TIP:
   
   Draw the tree and write bounds at each node:
   
         5 (-∞, +∞)
        / \
       1   4
   (-∞,5) (5,+∞)
   
   Check: 4 in range (5, +∞)? No! 4 < 5 → Invalid

10. HOW TO PRESENT IT:
    
    "I'll use the range bound approach because it directly
    captures the BST definition - every node must be within
    bounds set by its ancestors."
    
    Then: "Alternatively, I could use inorder traversal
    since BST inorder is always sorted."
    
    Shows understanding of multiple approaches!

================================================================================
"""
