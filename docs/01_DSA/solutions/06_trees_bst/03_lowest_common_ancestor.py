"""
================================================================================
PROBLEM: Lowest Common Ancestor of a Binary Tree (LeetCode 236)
Difficulty: Medium | Pattern: Tree DFS
================================================================================

PROBLEM STATEMENT:
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes.

The lowest common ancestor is defined as the lowest node in the tree that has 
both p and q as descendants (where we allow a node to be a descendant of itself).

EXAMPLES:
    Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
    Output: 3
    
                  3
                /   \
               5     1
              / \   / \
             6   2 0   8
                / \
               7   4
    
    Explanation: LCA of nodes 5 and 1 is 3.

    Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
    Output: 5
    Explanation: LCA of 5 and 4 is 5 (node can be descendant of itself)

    Input: root = [1,2], p = 1, q = 2
    Output: 1

CONSTRAINTS:
- The number of nodes in the tree is in range [2, 10^5]
- -10^9 <= Node.val <= 10^9
- All Node.val are unique
- p != q
- p and q will exist in the tree

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
# SOLUTION 1: Recursive DFS (Optimal)
# ============================================================================
def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Recursively find p and q. LCA is where paths diverge.
    
    Three cases:
    1. p and q both in left subtree → LCA in left
    2. p and q both in right subtree → LCA in right
    3. p and q in different subtrees OR current node is p/q → current is LCA
    
    Time: O(n) - visit each node once
    Space: O(h) - recursion stack
    """
    # Base case
    if not root or root == p or root == q:
        return root
    
    # Search in both subtrees
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    
    # If both subtrees return non-null, current node is LCA
    if left and right:
        return root
    
    # Otherwise, return the non-null one (or null if both null)
    return left if left else right


# ============================================================================
# SOLUTION 2: Using Parent Pointers (Build Path)
# ============================================================================
def lowestCommonAncestor_parent(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Build parent map, then trace paths from p and q.
    Find where paths intersect.
    
    Time: O(n)
    Space: O(n) for parent map and ancestors set
    """
    # Build parent map using BFS
    parent = {root: None}
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        if node.left:
            parent[node.left] = node
            queue.append(node.left)
        if node.right:
            parent[node.right] = node
            queue.append(node.right)
    
    # Collect all ancestors of p
    ancestors = set()
    while p:
        ancestors.add(p)
        p = parent[p]
    
    # Find first ancestor of q that's also ancestor of p
    while q not in ancestors:
        q = parent[q]
    
    return q


# ============================================================================
# SOLUTION 3: Iterative with Stack (Postorder-like)
# ============================================================================
def lowestCommonAncestor_iterative(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Iterative approach using stack.
    Track state with (node, visited_children_count)
    
    Time: O(n)
    Space: O(h)
    """
    # This is more complex - showing parent pointer method is cleaner
    # Using the parent pointer approach is generally preferred for iterative
    
    parent = {root: None}
    stack = [root]
    
    # Find both p and q and build parent map
    while p not in parent or q not in parent:
        node = stack.pop()
        if node.left:
            parent[node.left] = node
            stack.append(node.left)
        if node.right:
            parent[node.right] = node
            stack.append(node.right)
    
    # Find ancestors of p
    ancestors = set()
    while p:
        ancestors.add(p)
        p = parent[p]
    
    # First ancestor of q in p's ancestors
    while q not in ancestors:
        q = parent[q]
    
    return q


# ============================================================================
# BONUS: LCA of Binary Search Tree (LeetCode 235)
# ============================================================================
def lowestCommonAncestor_BST(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    For BST, we can use values to guide the search.
    
    - Both smaller → go left
    - Both larger → go right
    - Split (one each side) → current is LCA
    
    Time: O(h) - much better for BST!
    Space: O(1) for iterative
    """
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    
    return None


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


def find_node(root: TreeNode, val: int) -> Optional[TreeNode]:
    """Find node with given value"""
    if not root:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: LCA is root
    root1 = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p1, q1 = find_node(root1, 5), find_node(root1, 1)
    print(f"Tree: [3,5,1,6,2,0,8,null,null,7,4]")
    print(f"LCA of 5 and 1 (Recursive): {lowestCommonAncestor(root1, p1, q1).val}")
    # Expected: 3
    print()
    
    # Test Case 2: One node is ancestor of another
    root2 = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p2, q2 = find_node(root2, 5), find_node(root2, 4)
    print(f"LCA of 5 and 4: {lowestCommonAncestor(root2, p2, q2).val}")
    # Expected: 5 (5 is ancestor of 4)
    print()
    
    # Test Case 3: Using parent pointer approach
    root3 = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p3, q3 = find_node(root3, 7), find_node(root3, 4)
    print(f"LCA of 7 and 4 (Parent): {lowestCommonAncestor_parent(root3, p3, q3).val}")
    # Expected: 2
    print()
    
    # Test Case 4: BST LCA
    bst = build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    p4, q4 = find_node(bst, 2), find_node(bst, 8)
    print(f"BST Tree: [6,2,8,0,4,7,9,null,null,3,5]")
    print(f"LCA of 2 and 8 (BST): {lowestCommonAncestor_BST(bst, p4, q4).val}")
    # Expected: 6
    print()
    
    # Test Case 5: Simple tree
    root5 = build_tree([1, 2])
    p5, q5 = find_node(root5, 1), find_node(root5, 2)
    print(f"LCA of 1 and 2: {lowestCommonAncestor(root5, p5, q5).val}")
    # Expected: 1


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE ELEGANT RECURSIVE SOLUTION:
   
   Key insight: When searching for p and q...
   
   - If we find p or q, return it
   - If both left and right return non-null → current is LCA
   - Otherwise, return whichever is non-null
   
   The magic: When left and right both return values,
   it means p is in one subtree and q is in other!

2. VISUAL WALKTHROUGH:
   
         3 (returns 3 = LCA)
        / \
       5   1
      
   Finding LCA(5, 1):
   - At 3: search left for 5, search right for 1
   - Left returns 5 (found)
   - Right returns 1 (found)
   - Both non-null → 3 is LCA!

3. WHEN ONE IS ANCESTOR OF OTHER:
   
   LCA(5, 4) where 4 is descendant of 5:
   
   - At 3: search left
   - At 5: root == p, return 5 immediately
   - Right subtree never searched (optimization!)
   - LCA = 5

4. BST VS BINARY TREE:
   
   Binary Tree (LC 236):
   - Must search both subtrees
   - O(n) time
   
   BST (LC 235):
   - Use values to guide search
   - O(h) time - much better!
   - Go left/right based on values

5. PARENT POINTER APPROACH:
   
   When to use:
   - When you need to trace actual paths
   - When tree structure doesn't help (like binary tree vs BST)
   
   Steps:
   1. Build parent map
   2. Collect p's ancestors
   3. Find first of q's ancestors in p's set

6. COMMON VARIATIONS:
   
   - LCA with parent pointers given (LC 1650)
   - LCA of deepest leaves (LC 1123)
   - LCA of multiple nodes
   - LCA in n-ary tree

7. COMMON MISTAKES:
   
   ❌ Stopping search too early
   ❌ Not handling case where p or q is root
   ❌ For BST, not recognizing you can use values

8. TIME COMPLEXITY ANALYSIS:
   
   Binary tree: O(n) - might visit all nodes
   BST: O(h) - at most visit one path
   
   This is a key difference!

9. practice CLARIFICATIONS:
   
   Ask:
   - "Is this a BST or general binary tree?"
   - "Are p and q guaranteed to exist?"
   - "Can p equal q?"
   
   These affect solution choice!

10. practice TIP:
    
    Start with recursive approach - it's elegant and shows
    good understanding.
    
    Then mention: "For BST, I could optimize to O(h) by
    using node values to guide the search."
    
    And: "If I needed actual paths, I'd use parent pointers."

================================================================================
"""
