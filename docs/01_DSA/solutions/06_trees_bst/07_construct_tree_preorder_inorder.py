"""
================================================================================
PROBLEM: Construct Binary Tree from Preorder and Inorder Traversal (LeetCode 105)
Difficulty: Medium | Pattern: Tree Construction
================================================================================

PROBLEM STATEMENT:
Given two integer arrays preorder and inorder where preorder is the preorder 
traversal of a binary tree and inorder is the inorder traversal of the same tree,
construct and return the binary tree.

EXAMPLES:
    Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
    Output: [3,9,20,null,null,15,7]
    
          3
         / \
        9  20
          /  \
         15   7

    Input: preorder = [-1], inorder = [-1]
    Output: [-1]

CONSTRAINTS:
- 1 <= preorder.length <= 3000
- inorder.length == preorder.length
- -3000 <= preorder[i], inorder[i] <= 3000
- preorder and inorder consist of unique values
- Each value of inorder also appears in preorder
- preorder is guaranteed to be the preorder traversal of the tree
- inorder is guaranteed to be the inorder traversal of the tree

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
# SOLUTION 1: Recursive with HashMap (Optimal)
# ============================================================================
def buildTree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    Key insight:
    - Preorder first element is root
    - In inorder, elements left of root = left subtree
    - In inorder, elements right of root = right subtree
    
    Use HashMap for O(1) lookup of root position in inorder.
    
    Time: O(n)
    Space: O(n) for HashMap and recursion
    """
    # Map value to index in inorder for O(1) lookup
    inorder_idx = {val: idx for idx, val in enumerate(inorder)}
    preorder_idx = [0]  # Use list to maintain state across recursions
    
    def build(left: int, right: int) -> Optional[TreeNode]:
        """Build tree for inorder[left:right+1]"""
        if left > right:
            return None
        
        # Root is next element in preorder
        root_val = preorder[preorder_idx[0]]
        preorder_idx[0] += 1
        
        root = TreeNode(root_val)
        
        # Find root position in inorder
        mid = inorder_idx[root_val]
        
        # Build subtrees
        # IMPORTANT: Build left first! (matches preorder traversal)
        root.left = build(left, mid - 1)
        root.right = build(mid + 1, right)
        
        return root
    
    return build(0, len(inorder) - 1)


# ============================================================================
# SOLUTION 2: Recursive with Slicing (Simpler but slower)
# ============================================================================
def buildTree_slicing(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    Same logic but with array slicing.
    Easier to understand but O(n) for each slice.
    
    Time: O(n²) due to slicing
    Space: O(n²) due to slice copies
    """
    if not preorder or not inorder:
        return None
    
    # First element of preorder is root
    root_val = preorder[0]
    root = TreeNode(root_val)
    
    # Find root in inorder
    mid = inorder.index(root_val)
    
    # Left subtree: elements before root in inorder
    # Right subtree: elements after root in inorder
    root.left = buildTree_slicing(preorder[1:mid+1], inorder[:mid])
    root.right = buildTree_slicing(preorder[mid+1:], inorder[mid+1:])
    
    return root


# ============================================================================
# SOLUTION 3: Iterative with Stack
# ============================================================================
def buildTree_iterative(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    Iterative approach using stack.
    More complex but avoids recursion.
    
    Time: O(n)
    Space: O(n)
    """
    if not preorder:
        return None
    
    root = TreeNode(preorder[0])
    stack = [root]
    inorder_idx = 0
    
    for i in range(1, len(preorder)):
        node = TreeNode(preorder[i])
        
        if stack[-1].val != inorder[inorder_idx]:
            # No left children exhausted yet, go left
            stack[-1].left = node
        else:
            # Some left subtrees are complete
            parent = None
            while stack and stack[-1].val == inorder[inorder_idx]:
                parent = stack.pop()
                inorder_idx += 1
            parent.right = node
        
        stack.append(node)
    
    return root


# ============================================================================
# BONUS: Build from Inorder and Postorder (LeetCode 106)
# ============================================================================
def buildTree_postorder(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    """
    Similar approach but:
    - Root is LAST element of postorder
    - Process right subtree before left (reverse of postorder)
    
    Time: O(n)
    Space: O(n)
    """
    inorder_idx = {val: idx for idx, val in enumerate(inorder)}
    postorder_idx = [len(postorder) - 1]
    
    def build(left: int, right: int) -> Optional[TreeNode]:
        if left > right:
            return None
        
        root_val = postorder[postorder_idx[0]]
        postorder_idx[0] -= 1
        
        root = TreeNode(root_val)
        mid = inorder_idx[root_val]
        
        # IMPORTANT: Build RIGHT first! (matches postorder reverse)
        root.right = build(mid + 1, right)
        root.left = build(left, mid - 1)
        
        return root
    
    return build(0, len(inorder) - 1)


# ============================================================================
# HELPER FUNCTIONS FOR TESTING
# ============================================================================
def tree_to_level_order(root: Optional[TreeNode]) -> List:
    """Convert tree to level-order list"""
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    
    while result and result[-1] is None:
        result.pop()
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Normal tree
    preorder1 = [3, 9, 20, 15, 7]
    inorder1 = [9, 3, 15, 20, 7]
    print(f"Preorder: {preorder1}")
    print(f"Inorder:  {inorder1}")
    root1 = buildTree(preorder1, inorder1)
    print(f"Built tree: {tree_to_level_order(root1)}")
    # Expected: [3, 9, 20, None, None, 15, 7]
    print()
    
    # Test Case 2: Single node
    preorder2 = [-1]
    inorder2 = [-1]
    root2 = buildTree(preorder2, inorder2)
    print(f"Single node: {tree_to_level_order(root2)}")
    # Expected: [-1]
    print()
    
    # Test Case 3: Left-skewed tree
    preorder3 = [1, 2, 3]
    inorder3 = [3, 2, 1]
    root3 = buildTree(preorder3, inorder3)
    print(f"Left-skewed: {tree_to_level_order(root3)}")
    # Expected: [1, 2, None, 3]
    print()
    
    # Test Case 4: Using slicing method
    root4 = buildTree_slicing(preorder1, inorder1)
    print(f"Slicing method: {tree_to_level_order(root4)}")
    print()
    
    # Test Case 5: Postorder + Inorder
    inorder5 = [9, 3, 15, 20, 7]
    postorder5 = [9, 15, 7, 20, 3]
    root5 = buildTree_postorder(inorder5, postorder5)
    print(f"From postorder: {tree_to_level_order(root5)}")
    # Expected: [3, 9, 20, None, None, 15, 7]


r"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE CORE INSIGHT:
   
   Preorder: [ROOT] [LEFT subtree] [RIGHT subtree]
   Inorder:  [LEFT subtree] [ROOT] [RIGHT subtree]
   
   First element of preorder = ROOT
   Find root in inorder → divides left/right subtrees

2. VISUAL EXAMPLE:
   
   Preorder: [3, 9, 20, 15, 7]
   Inorder:  [9, 3, 15, 20, 7]
   
   Root = 3 (first in preorder)
   In inorder, 3 is at index 1
   
   Left subtree:  inorder[0:1] = [9]
   Right subtree: inorder[2:5] = [15, 20, 7]
   
   Preorder of left:  [9]      (next 1 element)
   Preorder of right: [20, 15, 7] (remaining)

3. WHY HASHMAP?
   
   Finding root in inorder: O(n) with index()
   With HashMap: O(1)
   
   Total time: O(n²) → O(n)

4. ORDER OF BUILDING SUBTREES:
   
   CRITICAL: For preorder, build LEFT first!
   
   Preorder processes: root → left → right
   So preorder_idx advances through left before right.
   
   For postorder: build RIGHT first!
   Postorder processes: left → right → root (reverse = root → right → left)

5. INDEX MANAGEMENT:
   
   Use list [0] or class variable to track current preorder index.
   Can't use simple variable in nested function (scope issue).
   
   preorder_idx = [0]
   preorder_idx[0] += 1  # This works

6. SLICING VS INDICES:
   
   Slicing: Simpler code, but O(n²) time and space
   Indices: More complex, but O(n) optimal
   
   Start with slicing for clarity, then optimize.

7. RELATED PROBLEMS:
   
   - Build from Inorder + Postorder (LC 106)
   - Build from Preorder of BST (LC 1008) - no inorder needed!
   - Serialize/Deserialize Tree (LC 297)

8. WHY INORDER IS ESSENTIAL:
   
   Preorder alone can't determine structure.
   [1, 2, 3] could be:
   
        1           1
       /     or      \
      2               2
       \               \
        3               3
   
   Inorder tells us which side each node belongs to.

9. COMMON MISTAKES:
   
   ❌ Building right subtree before left (for preorder)
   ❌ Not using HashMap (O(n²) instead of O(n))
   ❌ Wrong index calculations for subtree ranges

10. RECOMMENDED APPROACH:
    
    1. Explain the insight: "First of preorder is root"
    2. Show how to divide inorder
    3. Start with slicing solution
    4. Optimize with HashMap if time permits
    
    "I'll use a HashMap for O(1) lookup of root position
    in inorder, bringing total time from O(n²) to O(n)."

================================================================================
"""
