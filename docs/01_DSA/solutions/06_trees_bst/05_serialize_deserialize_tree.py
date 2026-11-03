"""
================================================================================
PROBLEM: Serialize and Deserialize Binary Tree (LeetCode 297)
Difficulty: Hard | Pattern: Tree + Design
================================================================================

PROBLEM STATEMENT:
Design an algorithm to serialize and deserialize a binary tree.

Serialization is the process of converting a data structure or object into a 
sequence of bits so that it can be stored in a file or memory buffer.

Deserialization is the reverse process - constructing the original data structure
from the serialized data.

There is no restriction on how your serialization/deserialization algorithm 
should work. You just need to ensure that a binary tree can be serialized to a 
string and this string can be deserialized to the original tree structure.

EXAMPLES:
    Input: root = [1,2,3,null,null,4,5]
    Output: [1,2,3,null,null,4,5]
    
             1
            / \
           2   3
              / \
             4   5

    Input: root = []
    Output: []

CONSTRAINTS:
- The number of nodes in the tree is in range [0, 10^4]
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
# SOLUTION 1: Preorder DFS (Optimal & Elegant)
# ============================================================================
class Codec:
    """
    Preorder traversal serialization.
    Use 'N' or '#' for null nodes.
    
    Serialize: root, left subtree, right subtree
    Deserialize: Build tree in same order
    
    Time: O(n) for both operations
    Space: O(n) for the string/tree
    """
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string."""
        result = []
        
        def preorder(node: TreeNode) -> None:
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
        
        def build() -> Optional[TreeNode]:
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
# SOLUTION 2: BFS / Level Order (Intuitive)
# ============================================================================
class Codec_BFS:
    """
    Level order serialization (like LeetCode's format).
    Use 'null' for missing nodes.
    
    Time: O(n)
    Space: O(n)
    """
    
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string."""
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
        """Decodes your encoded data to tree."""
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
# SOLUTION 3: Preorder with Iterator (No index tracking)
# ============================================================================
class Codec_Iterator:
    """
    Same preorder approach but using iterator.
    More Pythonic.
    
    Time: O(n)
    Space: O(n)
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
# HELPER FUNCTIONS FOR TESTING
# ============================================================================
def print_tree_level_order(root: Optional[TreeNode]) -> list:
    """Print tree in level order for verification"""
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
    
    # Remove trailing Nones
    while result and result[-1] is None:
        result.pop()
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print("=== Testing Preorder DFS Codec ===")
    codec = Codec()
    
    # Test Case 1: Normal tree
    #      1
    #     / \
    #    2   3
    #       / \
    #      4   5
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(3)
    root1.right.left = TreeNode(4)
    root1.right.right = TreeNode(5)
    
    print(f"Original: {print_tree_level_order(root1)}")
    serialized = codec.serialize(root1)
    print(f"Serialized: {serialized}")
    deserialized = codec.deserialize(serialized)
    print(f"Deserialized: {print_tree_level_order(deserialized)}")
    # Expected: [1, 2, 3, None, None, 4, 5]
    print()
    
    # Test Case 2: Empty tree
    root2 = None
    serialized2 = codec.serialize(root2)
    print(f"Empty tree serialized: '{serialized2}'")
    deserialized2 = codec.deserialize(serialized2)
    print(f"Deserialized: {deserialized2}")
    print()
    
    # Test Case 3: Single node
    root3 = TreeNode(42)
    serialized3 = codec.serialize(root3)
    print(f"Single node [42] serialized: '{serialized3}'")
    deserialized3 = codec.deserialize(serialized3)
    print(f"Deserialized: {print_tree_level_order(deserialized3)}")
    print()
    
    # Test Case 4: BFS Codec
    print("=== Testing BFS Codec ===")
    codec_bfs = Codec_BFS()
    serialized_bfs = codec_bfs.serialize(root1)
    print(f"BFS Serialized: {serialized_bfs}")
    deserialized_bfs = codec_bfs.deserialize(serialized_bfs)
    print(f"Deserialized: {print_tree_level_order(deserialized_bfs)}")


r"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHY PREORDER WORKS:
   
   Preorder visits: Root, Left, Right
   
   With null markers, we can uniquely reconstruct the tree!
   
   Tree:     1
            / \
           2   3
   
   Preorder with nulls: 1, 2, N, N, 3, N, N
   
   Deserialize:
   - 1 is root
   - 2 is left of 1
   - N means 2 has no left child
   - N means 2 has no right child
   - 3 is right of 1 (backtrack)
   - etc.

2. WHY WE NEED NULL MARKERS:
   
   Without nulls: Preorder [1, 2, 3] could be multiple trees:
   
        1       or      1
       / \             /
      2   3           2
                       \
                        3
   
   With nulls: [1, 2, N, N, 3, N, N] is unique!

3. THE INDEX/ITERATOR TRICK:
   
   During deserialization, we process values in same order.
   Use either:
   - self.index (class variable)
   - iter() and next()
   
   Both avoid passing modified index around.

4. BFS VS DFS:
   
   BFS (Level Order):
   - Looks like LeetCode's format
   - May have trailing nulls
   - Intuitive for humans
   
   DFS (Preorder):
   - No trailing nulls issue
   - Slightly more compact
   - Recursive deserialization is elegant

5. HANDLING EDGE CASES:
   
   - Empty tree: Return '' or special marker
   - Single node: Works with standard logic
   - Negative values: Use comma separator, not space

6. DELIMITER CHOICES:
   
   Use ',' or any character not in values.
   Don't use space if values can be negative (e.g., "-10").
   
   -10 → "-10" (no space issue with comma)

7. COMMON MISTAKES:
   
   ❌ Forgetting null markers
   ❌ Not handling empty tree
   ❌ Using space delimiter with negative numbers
   ❌ Modifying index incorrectly in recursion

8. FOLLOW-UP: BST SERIALIZATION
   
   For BST, you don't need null markers!
   Preorder alone is enough because BST property lets you
   determine which values go left vs right.
   
   Serialize: Preorder traversal
   Deserialize: Use min/max bounds

9. HOW TO PRESENT IT:
   
   "I'll use preorder traversal with null markers.
   
   Serialize: Visit root, then left subtree, then right.
   Mark nulls with 'N' or '#'.
   
   Deserialize: Process values in same order.
   Build node, recursively build left, then right.
   
   The null markers let us know when to stop and backtrack."

10. COMPLEXITY ANALYSIS:
    
    Time: O(n) for both serialize and deserialize
    Space: O(n) for the string and O(h) for recursion stack
    
    where n = number of nodes, h = height

================================================================================
"""
