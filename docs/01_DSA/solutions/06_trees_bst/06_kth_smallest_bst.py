"""
================================================================================
PROBLEM: Kth Smallest Element in a BST (LeetCode 230)
Difficulty: Medium | Pattern: BST + Inorder
================================================================================

PROBLEM STATEMENT:
Given the root of a binary search tree, and an integer k, return the kth 
smallest value (1-indexed) of all the values of the nodes in the tree.

EXAMPLES:
    Input: root = [3,1,4,null,2], k = 1
    Output: 1
    
          3
         / \
        1   4
         \
          2
    
    Inorder: [1, 2, 3, 4] → 1st smallest = 1

    Input: root = [5,3,6,2,4,null,null,1], k = 3
    Output: 3
    
            5
           / \
          3   6
         / \
        2   4
       /
      1
    
    Inorder: [1, 2, 3, 4, 5, 6] → 3rd smallest = 3

CONSTRAINTS:
- The number of nodes in the tree is n
- 1 <= k <= n <= 10^4
- 0 <= Node.val <= 10^4

FOLLOW-UP:
If the BST is modified often (insert/delete) and you need to find kth smallest 
frequently, how would you optimize?

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
# SOLUTION 1: Iterative Inorder (Optimal - Early Exit)
# ============================================================================
def kthSmallest(root: Optional[TreeNode], k: int) -> int:
    """
    Iterative inorder traversal.
    Stop as soon as we find kth element.
    
    BST inorder = sorted order!
    
    Time: O(H + k) where H = height
    Space: O(H) for stack
    """
    stack = []
    curr = root
    count = 0
    
    while stack or curr:
        # Go to leftmost
        while curr:
            stack.append(curr)
            curr = curr.left
        
        # Process node
        curr = stack.pop()
        count += 1
        
        if count == k:
            return curr.val
        
        # Go right
        curr = curr.right
    
    return -1  # Should never reach if k is valid


# ============================================================================
# SOLUTION 2: Recursive Inorder
# ============================================================================
def kthSmallest_recursive(root: Optional[TreeNode], k: int) -> int:
    """
    Recursive inorder with early exit using nonlocal counter.
    
    Time: O(H + k)
    Space: O(H) for recursion stack
    """
    result = None
    count = 0
    
    def inorder(node: TreeNode) -> None:
        nonlocal result, count
        
        if not node or result is not None:
            return
        
        # Left
        inorder(node.left)
        
        # Process
        count += 1
        if count == k:
            result = node.val
            return
        
        # Right
        inorder(node.right)
    
    inorder(root)
    return result


# ============================================================================
# SOLUTION 3: Build Sorted Array (Simple but O(n) space)
# ============================================================================
def kthSmallest_array(root: Optional[TreeNode], k: int) -> int:
    """
    Build complete inorder array, then return k-1 index.
    
    Time: O(n)
    Space: O(n)
    """
    def inorder(node):
        if not node:
            return []
        return inorder(node.left) + [node.val] + inorder(node.right)
    
    return inorder(root)[k - 1]


# ============================================================================
# SOLUTION 4: Augmented BST (For Follow-up - Frequent Queries)
# ============================================================================
class AugmentedTreeNode:
    """Each node stores count of nodes in left subtree"""
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
        self.left_count = 0  # Number of nodes in left subtree


def kthSmallest_augmented(root: AugmentedTreeNode, k: int) -> int:
    """
    If BST is augmented with left_count at each node:
    
    At each node:
    - If k == left_count + 1: current node is answer
    - If k <= left_count: go left
    - Else: go right with k = k - left_count - 1
    
    Time: O(H) - no need to visit all nodes!
    Space: O(1) iterative, O(H) recursive
    """
    while root:
        left_count = root.left_count
        
        if k == left_count + 1:
            return root.val
        elif k <= left_count:
            root = root.left
        else:
            k = k - left_count - 1
            root = root.right
    
    return -1


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
    # Test Case 1: Small tree
    root1 = build_tree([3, 1, 4, None, 2])
    print(f"Tree: [3,1,4,null,2]")
    print(f"k=1 (Iterative): {kthSmallest(root1, 1)}")  # Expected: 1
    print(f"k=2 (Recursive): {kthSmallest_recursive(root1, 2)}")  # Expected: 2
    print(f"k=3 (Array): {kthSmallest_array(root1, 3)}")  # Expected: 3
    print()
    
    # Test Case 2: Larger tree
    root2 = build_tree([5, 3, 6, 2, 4, None, None, 1])
    print(f"Tree: [5,3,6,2,4,null,null,1]")
    print(f"k=3: {kthSmallest(root2, 3)}")  # Expected: 3
    print(f"k=5: {kthSmallest(root2, 5)}")  # Expected: 5
    print()
    
    # Test Case 3: Single node
    root3 = build_tree([1])
    print(f"Tree: [1]")
    print(f"k=1: {kthSmallest(root3, 1)}")  # Expected: 1
    print()
    
    # Test Case 4: Linear tree (like linked list)
    root4 = build_tree([3, 2, None, 1])
    print(f"Tree: [3,2,null,1] (left skewed)")
    print(f"k=2: {kthSmallest(root4, 2)}")  # Expected: 2


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE BST PROPERTY:
   
   BST Inorder traversal = Sorted order!
   
   So kth smallest = k-th element in inorder traversal.
   
   This is the KEY insight for BST problems.

2. ITERATIVE VS RECURSIVE:
   
   Both work, but iterative has advantage:
   - Can exit early when k is found
   - No recursion overhead
   
   Time is O(H + k), not O(n)!
   For k=1, we only visit H nodes (leftmost path).

3. THE ITERATIVE INORDER TEMPLATE:
   
   stack = []
   curr = root
   while stack or curr:
       while curr:
           stack.append(curr)
           curr = curr.left
       curr = stack.pop()
       # PROCESS curr
       curr = curr.right
   
   This template is ESSENTIAL for BST problems!

4. FOLLOW-UP: FREQUENT MODIFICATIONS
   
   If tree changes often and kth query is frequent:
   
   Option 1: Augmented BST
   - Store left_count at each node
   - Update on insert/delete
   - Query in O(H) without full traversal
   
   Option 2: Order Statistics Tree
   - Self-balancing BST (like Red-Black)
   - With size tracking
   
   This shows system design thinking!

5. AUGMENTED BST LOGIC:
   
   At node with left_count = L:
   - k == L+1: This node is answer (L smaller + this one)
   - k <= L: Go left (answer in left subtree)
   - k > L+1: Go right, looking for (k-L-1)th

6. COMMON MISTAKE:
   
   ❌ Building full sorted array when only kth needed
   
   This is O(n) space and O(n) time.
   Early exit is O(H + k) time, O(H) space.

7. RELATED PROBLEMS:
   
   - Inorder Successor in BST (LC 285)
   - Validate BST (LC 98) - same inorder property
   - Convert Sorted Array to BST (LC 108)

8. TIME COMPLEXITY ANALYSIS:
   
   Iterative/Recursive with early exit:
   - Best case (k=1): O(H) - just go left
   - Worst case (k=n): O(n) - visit all
   - Average: O(H + k)
   
   Augmented BST:
   - Always O(H) for any k!

9. practice CLARIFICATIONS:
   
   Ask: "Can the tree be modified?"
   Ask: "How frequent are the queries?"
   
   These determine if augmented BST is needed.

10. practice TIP:
    
    Start with basic inorder solution.
    Then optimize with early exit.
    If asked about frequent queries, mention augmented BST:
    
    "If we need frequent kth smallest queries with modifications,
    I'd augment each node with left subtree count. This gives O(H)
    query time instead of O(H + k)."

================================================================================
"""
