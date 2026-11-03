"""
================================================================================
PROBLEM: LRU Cache (LeetCode 146)
Difficulty: Medium | Pattern: Design (HashMap + Doubly Linked List)
================================================================================

PROBLEM STATEMENT:
Design a data structure that follows the constraints of a Least Recently Used 
(LRU) cache.

Implement the LRUCache class:
- LRUCache(int capacity): Initialize the LRU cache with positive size capacity.
- int get(int key): Return the value of the key if the key exists, otherwise -1.
- void put(int key, int value): Update the value if the key exists. Otherwise, 
  add the key-value pair. If the number of keys exceeds capacity, evict the 
  least recently used key.

The functions get and put must each run in O(1) average time complexity.

EXAMPLES:
    Input: ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
           [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
    Output: [null, null, null, 1, null, -1, null, -1, 3, 4]

CONSTRAINTS:
- 1 <= capacity <= 3000
- 0 <= key <= 10^4
- 0 <= value <= 10^5
- At most 2 * 10^5 calls will be made to get and put

================================================================================
"""


# ============================================================================
# SOLUTION 1: HashMap + Doubly Linked List (Standard Approach)
# ============================================================================
class ListNode:
    """Doubly linked list node."""
    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    """
    HashMap for O(1) lookup.
    Doubly linked list for O(1) insertion/removal.
    
    Most recently used at head, least recently used at tail.
    
    Time: O(1) for get and put
    Space: O(capacity)
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> ListNode
        
        # Dummy head and tail for easy operations
        self.head = ListNode()  # Most recently used
        self.tail = ListNode()  # Least recently used
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node: ListNode) -> None:
        """Remove node from linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _add_to_head(self, node: ListNode) -> None:
        """Add node right after head (most recently used)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _move_to_head(self, node: ListNode) -> None:
        """Move existing node to head (mark as recently used)."""
        self._remove(node)
        self._add_to_head(node)
    
    def _pop_tail(self) -> ListNode:
        """Remove and return node before tail (least recently used)."""
        lru = self.tail.prev
        self._remove(lru)
        return lru
    
    def get(self, key: int) -> int:
        """Get value and mark as recently used."""
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node)
        return node.val
    
    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair."""
        if key in self.cache:
            # Update existing
            node = self.cache[key]
            node.val = value
            self._move_to_head(node)
        else:
            # Insert new
            node = ListNode(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            
            # Evict if over capacity
            if len(self.cache) > self.capacity:
                lru = self._pop_tail()
                del self.cache[lru.key]


# ============================================================================
# SOLUTION 2: Using OrderedDict (Python shortcut)
# ============================================================================
from collections import OrderedDict

class LRUCache_OrderedDict:
    """
    OrderedDict maintains insertion order.
    Move to end on access, pop first when evicting.
    
    Time: O(1) average
    Space: O(capacity)
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        
        self.cache[key] = value
        
        if len(self.cache) > self.capacity:
            # Pop first item (least recently used)
            self.cache.popitem(last=False)


# ============================================================================
# SOLUTION 3: Clean implementation with separate methods
# ============================================================================
class LRUCache_Clean:
    """Clean implementation with verbose comments."""
    
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        
        # Doubly linked list with dummy nodes
        self.left = ListNode(0, 0)   # LRU
        self.right = ListNode(0, 0)  # MRU
        self.left.next = self.right
        self.right.prev = self.left
    
    def remove(self, node: ListNode) -> None:
        """Remove node from doubly linked list."""
        prv, nxt = node.prev, node.next
        prv.next, nxt.prev = nxt, prv
    
    def insert(self, node: ListNode) -> None:
        """Insert node at right (most recently used)."""
        prv = self.right.prev
        prv.next = node
        node.prev = prv
        node.next = self.right
        self.right.prev = node
    
    def get(self, key: int) -> int:
        if key in self.cache:
            # Update to most recently used
            self.remove(self.cache[key])
            self.insert(self.cache[key])
            return self.cache[key].val
        return -1
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.remove(self.cache[key])
        
        self.cache[key] = ListNode(key, value)
        self.insert(self.cache[key])
        
        if len(self.cache) > self.cap:
            # Remove LRU (left.next)
            lru = self.left.next
            self.remove(lru)
            del self.cache[lru.key]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Basic operations
    print("=== Test 1: Basic Operations ===")
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(f"get(1): {cache.get(1)}")  # 1
    cache.put(3, 3)  # Evicts key 2
    print(f"get(2): {cache.get(2)}")  # -1
    cache.put(4, 4)  # Evicts key 1
    print(f"get(1): {cache.get(1)}")  # -1
    print(f"get(3): {cache.get(3)}")  # 3
    print(f"get(4): {cache.get(4)}")  # 4
    print()
    
    # Test Case 2: Update existing
    print("=== Test 2: Update Existing ===")
    cache2 = LRUCache(2)
    cache2.put(1, 1)
    cache2.put(2, 2)
    cache2.put(1, 10)  # Update, not new
    print(f"get(1): {cache2.get(1)}")  # 10
    cache2.put(3, 3)  # Evicts key 2 (not 1 since 1 was recently updated)
    print(f"get(2): {cache2.get(2)}")  # -1
    print()
    
    # Test Case 3: OrderedDict version
    print("=== Test 3: OrderedDict Version ===")
    cache3 = LRUCache_OrderedDict(2)
    cache3.put(1, 1)
    cache3.put(2, 2)
    print(f"get(1): {cache3.get(1)}")  # 1
    cache3.put(3, 3)
    print(f"get(2): {cache3.get(2)}")  # -1


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. DATA STRUCTURE CHOICE:
   
   Need: O(1) lookup + O(1) update access order
   
   HashMap: O(1) lookup by key
   Doubly Linked List: O(1) insertion/removal at any position
   
   Combine both!

2. WHY DOUBLY LINKED LIST?
   
   - Need to remove from middle in O(1)
   - Singly linked can't do O(1) removal without prev pointer
   - Array would be O(n) for removal

3. DUMMY HEAD/TAIL:
   
   Avoids null checks in add/remove operations.
   
   head <-> node1 <-> node2 <-> ... <-> tail
   
   head.next = MRU, tail.prev = LRU

4. KEY IN NODE:
   
   Store key in node so when evicting, we can delete from HashMap too!
   
   Without key, we'd need O(n) search to find which key to delete.

5. OPERATIONS:
   
   get(key):
   1. If not found, return -1
   2. Move node to head (MRU)
   3. Return value
   
   put(key, value):
   1. If exists, update value, move to head
   2. If new, create node, add to head
   3. If over capacity, remove tail.prev (LRU), delete from HashMap

6. ORDEREDDICT SHORTCUT:
   
   Python's OrderedDict has move_to_end() and popitem(last=False).
   Perfect for LRU!
   
   But understand the HashMap + DLL version first.

7. COMMON MISTAKES:
   
   ❌ Forgetting to delete from HashMap when evicting
   ❌ Not storing key in node
   ❌ Using singly linked list
   ❌ Not handling update (put on existing key)

8. FOLLOW-UP: LFU CACHE:
   
   Least Frequently Used - evict by frequency, then by recency.
   Need additional frequency tracking and frequency-to-nodes mapping.

9. RELATED PROBLEMS:
   
   - LFU Cache (LC 460)
   - All O(1) Data Structure (LC 432)
   - Design HashMap (LC 706)

10. HOW TO EXPLAIN IT:
    
    "I need O(1) for both get and put. HashMap gives O(1) lookup,
    but I also need to track access order.
    
    I'll use a doubly linked list where:
    - Head = most recently used
    - Tail = least recently used
    
    Each node stores key and value. On get/put, I move the node
    to head. On eviction, I remove tail.prev.
    
    The HashMap maps key → node for O(1) access."
    
    Draw the data structure before coding!

================================================================================
"""
