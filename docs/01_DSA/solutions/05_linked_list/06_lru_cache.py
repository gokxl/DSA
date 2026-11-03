"""
================================================================================
PROBLEM: LRU Cache (LeetCode 146)
Difficulty: Medium | Pattern: Design + LinkedList + HashMap
================================================================================

PROBLEM STATEMENT:
Design a data structure that follows the constraints of a Least Recently Used 
(LRU) cache.

Implement the LRUCache class:
- LRUCache(int capacity): Initialize the cache with positive size capacity.
- int get(int key): Return the value of the key if it exists, otherwise -1.
- void put(int key, int value): Update or insert the value. If the number of 
  keys exceeds capacity, evict the least recently used key.

The functions get and put must each run in O(1) average time complexity.

EXAMPLES:
    Input:
    ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
    [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
    
    Output: [null, null, null, 1, null, -1, null, -1, 3, 4]
    
    Explanation:
    LRUCache lRUCache = new LRUCache(2);
    lRUCache.put(1, 1);  // cache is {1=1}
    lRUCache.put(2, 2);  // cache is {1=1, 2=2}
    lRUCache.get(1);     // return 1, cache is {2=2, 1=1}
    lRUCache.put(3, 3);  // evicts key 2, cache is {1=1, 3=3}
    lRUCache.get(2);     // returns -1 (not found)
    lRUCache.put(4, 4);  // evicts key 1, cache is {3=3, 4=4}
    lRUCache.get(1);     // return -1 (not found)
    lRUCache.get(3);     // return 3, cache is {4=4, 3=3}
    lRUCache.get(4);     // return 4, cache is {3=3, 4=4}

CONSTRAINTS:
- 1 <= capacity <= 3000
- 0 <= key <= 10^4
- 0 <= value <= 10^5
- At most 2 * 10^5 calls will be made to get and put

================================================================================
"""


# ============================================================================
# SOLUTION 1: Doubly Linked List + HashMap (Optimal - From Scratch)
# ============================================================================
class DLLNode:
    """Doubly Linked List Node"""
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    """
    HashMap for O(1) access by key.
    Doubly Linked List for O(1) insertion/deletion and LRU ordering.
    
    Most recently used at HEAD, least recently used at TAIL.
    
    Time: O(1) for both get and put
    Space: O(capacity)
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> DLLNode
        
        # Dummy head and tail for easier manipulation
        self.head = DLLNode()
        self.tail = DLLNode()
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_to_front(self, node: DLLNode) -> None:
        """Add node right after head (most recently used position)"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node: DLLNode) -> None:
        """Remove node from its current position"""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _move_to_front(self, node: DLLNode) -> None:
        """Move existing node to front (mark as recently used)"""
        self._remove_node(node)
        self._add_to_front(node)
    
    def _remove_lru(self) -> DLLNode:
        """Remove and return the least recently used node (before tail)"""
        lru = self.tail.prev
        self._remove_node(lru)
        return lru
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_front(node)  # Mark as recently used
        return node.val
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing node
            node = self.cache[key]
            node.val = value
            self._move_to_front(node)
        else:
            # Create new node
            node = DLLNode(key, value)
            self.cache[key] = node
            self._add_to_front(node)
            
            # Evict LRU if over capacity
            if len(self.cache) > self.capacity:
                lru = self._remove_lru()
                del self.cache[lru.key]


# ============================================================================
# SOLUTION 2: Using Python's OrderedDict (Concise)
# ============================================================================
from collections import OrderedDict

class LRUCache_OrderedDict(OrderedDict):
    """
    OrderedDict maintains insertion order.
    move_to_end() and popitem(last=False) give us LRU behavior.
    
    Time: O(1) for both operations
    Space: O(capacity)
    """
    
    def __init__(self, capacity: int):
        super().__init__()
        self.capacity = capacity
    
    def get(self, key: int) -> int:
        if key not in self:
            return -1
        
        # Move to end (most recently used)
        self.move_to_end(key)
        return self[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self:
            # Move to end and update
            self.move_to_end(key)
        
        self[key] = value
        
        # Evict LRU (first item) if over capacity
        if len(self) > self.capacity:
            self.popitem(last=False)


# ============================================================================
# SOLUTION 3: Using collections.OrderedDict (Alternative API)
# ============================================================================
class LRUCache_OrderedDict2:
    """
    Same as above but without inheritance.
    """
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        
        self.cache[key] = value
        
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print("=== Testing LRUCache (From Scratch) ===")
    cache = LRUCache(2)
    
    cache.put(1, 1)
    print(f"put(1, 1) → cache: {{1: 1}}")
    
    cache.put(2, 2)
    print(f"put(2, 2) → cache: {{1: 1, 2: 2}}")
    
    result = cache.get(1)
    print(f"get(1) → {result} (expected: 1)")
    
    cache.put(3, 3)
    print(f"put(3, 3) → evicts 2, cache: {{1: 1, 3: 3}}")
    
    result = cache.get(2)
    print(f"get(2) → {result} (expected: -1)")
    
    cache.put(4, 4)
    print(f"put(4, 4) → evicts 1, cache: {{3: 3, 4: 4}}")
    
    print(f"get(1) → {cache.get(1)} (expected: -1)")
    print(f"get(3) → {cache.get(3)} (expected: 3)")
    print(f"get(4) → {cache.get(4)} (expected: 4)")
    print()
    
    print("=== Testing LRUCache (OrderedDict) ===")
    cache2 = LRUCache_OrderedDict(2)
    
    cache2.put(1, 1)
    cache2.put(2, 2)
    print(f"get(1) → {cache2.get(1)} (expected: 1)")
    cache2.put(3, 3)
    print(f"get(2) → {cache2.get(2)} (expected: -1)")
    cache2.put(4, 4)
    print(f"get(1) → {cache2.get(1)} (expected: -1)")
    print(f"get(3) → {cache2.get(3)} (expected: 3)")
    print(f"get(4) → {cache2.get(4)} (expected: 4)")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHY DOUBLY LINKED LIST?
   
   We need:
   - O(1) removal from middle (not possible with singly linked)
   - O(1) insertion at front
   
   DLL with prev/next pointers enables both.
   
   HashMap maps key → node for O(1) access.

2. THE TWO-DUMMY-NODE TRICK:
   
   head ↔ [actual nodes] ↔ tail
   
   Benefits:
   - Never check for null
   - Uniform add/remove logic
   - head.next = MRU, tail.prev = LRU

3. ORDERING STRATEGY:
   
   Most Recently Used (MRU) → head.next
   Least Recently Used (LRU) → tail.prev
   
   On access (get or put): move to front
   On eviction: remove from back

4. KEY OPERATIONS:
   
   get(key):
   1. If not in cache → return -1
   2. Move node to front
   3. Return value
   
   put(key, value):
   1. If key exists → update value, move to front
   2. If key new → create node, add to front
   3. If over capacity → remove LRU, delete from cache

5. WHY STORE KEY IN NODE?
   
   When evicting LRU, we need to delete from hashmap too.
   But hashmap is key → node.
   So node must know its key!
   
   node.key used for: del cache[lru.key]

6. ORDEREDDICT SHORTCUT:
   
   Python's OrderedDict:
   - Maintains insertion order
   - move_to_end(key) - O(1)
   - popitem(last=False) - O(1) removes first (oldest)
   
   Perfect for LRU! But know the manual approach too.

7. EDGE CASES:
   
   - Capacity = 1
   - Put same key twice (update, not insert)
   - Get after eviction
   - Put when exactly at capacity

8. FOLLOW-UP: LFU CACHE (LC 460)
   
   Least FREQUENTLY Used - much harder!
   Need additional frequency tracking.
   Google asks this as follow-up.

9. COMMON MISTAKES:
   
   ❌ Forgetting to update value on put() for existing key
   ❌ Not moving to front on get() (most common!)
   ❌ Forgetting to remove from hashmap on eviction

10. practice TIP:
    
    "I'll implement from scratch to show understanding,
    but in production I might use OrderedDict for simplicity."
    
    Shows you know both approaches!
    
    Draw the DLL state after each operation to verify:
    
    head ↔ [3:3] ↔ [1:1] ↔ tail
    
    Visual helps catch bugs!

================================================================================
"""
