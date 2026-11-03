"""
================================================================================
PROBLEM: Serialize and Deserialize Binary Tree (LeetCode 297)
Difficulty: Hard | Pattern: Design (Tree)
================================================================================

PROBLEM STATEMENT:
Serialization is the process of converting a data structure or object into a 
sequence of bits so that it can be stored in a file or memory buffer, or 
transmitted across a network connection link to be reconstructed later in the 
same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no 
restriction on how your serialization/deserialization algorithm should work. 
You just need to ensure that a binary tree can be serialized to a string and 
this string can be deserialized to the original tree structure.

EXAMPLES:
    Input: root = [1,2,3,null,null,4,5]
    Output: [1,2,3,null,null,4,5]

    Input: root = []
    Output: []

CONSTRAINTS:
- The number of nodes in the tree is in the range [0, 10^4]
- -1000 <= Node.val <= 1000

================================================================================
"""
from typing import Optional, List
from collections import deque


# Definition for a binary tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================================
# SOLUTION 1: Preorder Traversal (DFS)
# ============================================================================
class Codec:
    """
    Use preorder traversal with null markers.
    
    Serialize: Preorder with 'N' for null nodes.
    Deserialize: Rebuild using preorder order.
    
    Time: O(n) for both
    Space: O(n)
    """
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string."""
        result = []
        
        def preorder(node):
            if not node:
                result.append('N')
                return
            
            result.append(str(node.val))
            preorder(node.left)
            preorder(node.right)
        
        preorder(root)
        return ','.join(result)
    
    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes your encoded data to tree."""
        values = data.split(',')
        self.index = 0
        
        def build():
            if self.index >= len(values):
                return None
            
            val = values[self.index]
            self.index += 1
            
            if val == 'N':
                return None
            
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node
        
        return build()


# ============================================================================
# SOLUTION 2: Level Order Traversal (BFS)
# ============================================================================
class Codec_BFS:
    """
    Use level-order (BFS) traversal.
    More intuitive and matches LeetCode's format.
    
    Time: O(n)
    Space: O(n)
    """
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        if not root:
            return ''
        
        result = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append('N')
        
        # Remove trailing nulls
        while result and result[-1] == 'N':
            result.pop()
        
        return ','.join(result)
    
    def deserialize(self, data: str) -> Optional[TreeNode]:
        if not data:
            return None
        
        values = data.split(',')
        root = TreeNode(int(values[0]))
        queue = deque([root])
        i = 1
        
        while queue and i < len(values):
            node = queue.popleft()
            
            # Left child
            if i < len(values) and values[i] != 'N':
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1
            
            # Right child
            if i < len(values) and values[i] != 'N':
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i += 1
        
        return root


# ============================================================================
# SOLUTION 3: Preorder with Iterator
# ============================================================================
class Codec_Iterator:
    """
    Preorder with iterator instead of index tracking.
    Cleaner implementation.
    """
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        def preorder(node):
            if not node:
                yield 'N'
            else:
                yield str(node.val)
                yield from preorder(node.left)
                yield from preorder(node.right)
        
        return ','.join(preorder(root))
    
    def deserialize(self, data: str) -> Optional[TreeNode]:
        def build(values):
            val = next(values)
            if val == 'N':
                return None
            
            node = TreeNode(int(val))
            node.left = build(values)
            node.right = build(values)
            return node
        
        return build(iter(data.split(',')))


# ============================================================================
# SOLUTION 4: Postorder Traversal
# ============================================================================
class Codec_Postorder:
    """
    Use postorder traversal.
    Build tree from back to front.
    """
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        result = []
        
        def postorder(node):
            if not node:
                result.append('N')
                return
            
            postorder(node.left)
            postorder(node.right)
            result.append(str(node.val))
        
        postorder(root)
        return ','.join(result)
    
    def deserialize(self, data: str) -> Optional[TreeNode]:
        values = data.split(',')
        
        def build():
            val = values.pop()
            if val == 'N':
                return None
            
            node = TreeNode(int(val))
            # Reverse order: right first, then left
            node.right = build()
            node.left = build()
            return node
        
        return build()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def tree_to_list(root: Optional[TreeNode]) -> List:
    """Convert tree to list (for printing)."""
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


def list_to_tree(values: List) -> Optional[TreeNode]:
    """Convert list to tree."""
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
    # Test Case 1: DFS approach
    print("=== Test 1: DFS (Preorder) ===")
    codec = Codec()
    root1 = list_to_tree([1, 2, 3, None, None, 4, 5])
    serialized = codec.serialize(root1)
    print(f"Serialized: {serialized}")
    deserialized = codec.deserialize(serialized)
    print(f"Deserialized: {tree_to_list(deserialized)}")
    print()
    
    # Test Case 2: BFS approach
    print("=== Test 2: BFS (Level Order) ===")
    codec2 = Codec_BFS()
    root2 = list_to_tree([1, 2, 3, None, None, 4, 5])
    serialized2 = codec2.serialize(root2)
    print(f"Serialized: {serialized2}")
    deserialized2 = codec2.deserialize(serialized2)
    print(f"Deserialized: {tree_to_list(deserialized2)}")
    print()
    
    # Test Case 3: Empty tree
    print("=== Test 3: Empty Tree ===")
    codec3 = Codec()
    serialized3 = codec3.serialize(None)
    print(f"Serialized empty: '{serialized3}'")
    deserialized3 = codec3.deserialize(serialized3)
    print(f"Deserialized: {tree_to_list(deserialized3)}")
    print()
    
    # Test Case 4: Iterator approach
    print("=== Test 4: Iterator ===")
    codec4 = Codec_Iterator()
    root4 = list_to_tree([1, 2, 3])
    serialized4 = codec4.serialize(root4)
    print(f"Serialized: {serialized4}")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHY NEED NULL MARKERS?
   
   Without nulls, preorder [1,2,3] could be:
     1          1
    /   or      \
   2             2
    \             \
     3             3
   
   Null markers make structure unambiguous!

2. PREORDER VS LEVEL ORDER:
   
   Preorder (DFS):
   - Recursive, easy to implement
   - Less intuitive format
   
   Level Order (BFS):
   - Matches LeetCode's tree format
   - More intuitive for debugging

3. DELIMITER CHOICE:
   
   Use ',' to separate values.
   'N' or 'null' for null nodes.
   
   Avoid delimiter that could appear in values!

4. RECONSTRUCTION:
   
   Preorder: Root first, then recursively build left, right.
   Level order: Use queue, fill left then right for each node.

5. HANDLING NEGATIVES:
   
   Values can be negative (-1000 to 1000).
   split(',') handles this correctly.
   
   Don't use single character encoding!

6. EDGE CASES:
   
   - Empty tree: return empty string
   - Single node: just the value
   - Skewed tree: many nulls

7. SPACE OPTIMIZATION:
   
   Level order can skip trailing nulls.
   Preorder with null markers uses more space for dense trees.

8. TIME/SPACE:
   
   Both: O(n) time, O(n) space
   
   O(n) space for result string and recursion/queue.

9. RELATED PROBLEMS:
   
   - Serialize BST (LC 449) - no null markers needed
   - Construct from Preorder/Inorder (LC 105)
   - Flatten to Linked List (LC 114)

10. practice TIP:
    
    "I'll use preorder traversal with null markers. This makes
    the tree structure unambiguous.
    
    Serialize: DFS, append value or 'N' for null.
    Deserialize: Split string, rebuild tree using preorder order.
    
    The key insight is that null markers tell us exactly where
    children don't exist, so we can reconstruct perfectly."
    
    Draw an example to show how nulls capture structure!

================================================================================
"""
