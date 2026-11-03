"""
================================================================================
CODE TEMPLATES TO MEMORIZE
================================================================================
These templates should be AUTOMATIC. You should be able to write them without
thinking so you can focus on the PROBLEM-SPECIFIC logic.

Practice: Close this file, rebuild each template, and explain why each line is needed.
================================================================================
"""

# ==============================================================================
# 1. TWO POINTERS - SORTED ARRAY PAIR SUM
# ==============================================================================
def two_pointers_pair(arr, target):
    """
    Find two numbers in SORTED array that sum to target.
    Time: O(n), Space: O(1)
    """
    left, right = 0, len(arr) - 1
    
    while left < right:
        curr_sum = arr[left] + arr[right]
        if curr_sum == target:
            return [left, right]
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    
    return []


# ==============================================================================
# 2. SLIDING WINDOW - VARIABLE SIZE
# ==============================================================================
def sliding_window_variable(s):
    """
    Find longest/shortest substring with constraint.
    Time: O(n), Space: O(k) where k = unique chars
    """
    left = 0
    window = {}  # char -> count (or set for unique)
    result = 0
    
    for right in range(len(s)):
        # Expand: add s[right] to window
        window[s[right]] = window.get(s[right], 0) + 1
        
        # Shrink: while window is invalid
        while not is_valid(window):  # CUSTOMIZE THIS
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1
        
        # Update result (window is now valid)
        result = max(result, right - left + 1)
    
    return result


# ==============================================================================
# 3. BINARY SEARCH - STANDARD
# ==============================================================================
def binary_search(arr, target):
    """
    Search for target in sorted array.
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found (or return left for insertion point)


# ==============================================================================
# 4. BINARY SEARCH - FIND MINIMUM THAT SATISFIES CONDITION
# ==============================================================================
def binary_search_min(lo, hi):
    """
    Find minimum value where condition is True.
    Example: Koko eating bananas, minimum speed to finish
    Time: O(log(range) * check_time), Space: O(1)
    """
    while lo < hi:
        mid = lo + (hi - lo) // 2
        
        if condition(mid):  # CUSTOMIZE THIS
            hi = mid  # mid might be answer, try smaller
        else:
            lo = mid + 1  # mid doesn't work, need bigger
    
    return lo


# ==============================================================================
# 5. MONOTONIC STACK - NEXT GREATER ELEMENT
# ==============================================================================
def next_greater_element(nums):
    """
    Find next greater element for each position.
    Time: O(n), Space: O(n)
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # Stack of INDICES
    
    for i in range(n):
        # Pop while current is greater than stack top
        while stack and nums[i] > nums[stack[-1]]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    
    return result


# ==============================================================================
# 6. LINKED LIST - REVERSE
# ==============================================================================
def reverse_linked_list(head):
    """
    Reverse a singly linked list.
    Time: O(n), Space: O(1)
    """
    prev, curr = None, head
    
    while curr:
        next_temp = curr.next  # Save next
        curr.next = prev       # Reverse pointer
        prev = curr            # Move prev forward
        curr = next_temp       # Move curr forward
    
    return prev  # New head


# ==============================================================================
# 7. LINKED LIST - FAST/SLOW POINTERS (FIND MIDDLE)
# ==============================================================================
def find_middle(head):
    """
    Find middle node of linked list.
    Time: O(n), Space: O(1)
    """
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow  # Middle node (left-middle if even length)


# ==============================================================================
# 8. TREE - DFS RECURSIVE
# ==============================================================================
def tree_dfs(root):
    """
    Generic DFS template for trees.
    Time: O(n), Space: O(h) where h = height
    """
    def dfs(node):
        # Base case
        if not node:
            return base_value  # CUSTOMIZE (e.g., 0, True, [])
        
        # Recursive case
        left_result = dfs(node.left)
        right_result = dfs(node.right)
        
        # Combine results
        return combine(left_result, right_result, node.val)  # CUSTOMIZE
    
    return dfs(root)


# ==============================================================================
# 9. TREE - BFS LEVEL ORDER
# ==============================================================================
from collections import deque

def tree_bfs(root):
    """
    Level order traversal.
    Time: O(n), Space: O(n)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result


# ==============================================================================
# 10. GRAPH - BFS (SHORTEST PATH)
# ==============================================================================
def graph_bfs(graph, start, end):
    """
    BFS for shortest path in unweighted graph.
    graph: adjacency list {node: [neighbors]}
    Time: O(V + E), Space: O(V)
    """
    if start == end:
        return 0
    
    visited = {start}
    queue = deque([(start, 0)])  # (node, distance)
    
    while queue:
        node, dist = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor == end:
                return dist + 1
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return -1  # No path found


# ==============================================================================
# 11. GRAPH - DFS (CONNECTED COMPONENTS / ISLANDS)
# ==============================================================================
def count_islands(grid):
    """
    Count connected components in 2D grid.
    Time: O(m * n), Space: O(m * n) for recursion stack
    """
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        # Bounds check and water check
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        
        # Mark as visited
        grid[r][c] = '0'
        
        # Visit all 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    
    return count


# ==============================================================================
# 12. HEAP - TOP K ELEMENTS
# ==============================================================================
import heapq

def top_k_elements(nums, k):
    """
    Find k largest elements using min heap of size k.
    Time: O(n log k), Space: O(k)
    """
    # Min heap of size k
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)  # Remove smallest
    
    return heap  # Contains k largest


def top_k_frequent(nums, k):
    """
    Find k most frequent elements.
    Time: O(n log k), Space: O(n)
    """
    from collections import Counter
    
    count = Counter(nums)
    # Min heap of (frequency, element)
    heap = []
    
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    
    return [num for freq, num in heap]


# ==============================================================================
# 13. BACKTRACKING - SUBSETS
# ==============================================================================
def subsets(nums):
    """
    Generate all subsets.
    Time: O(2^n * n), Space: O(n) for recursion
    """
    result = []
    
    def backtrack(start, path):
        result.append(path[:])  # Add copy of current subset
        
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()  # Backtrack
    
    backtrack(0, [])
    return result


# ==============================================================================
# 14. BACKTRACKING - PERMUTATIONS
# ==============================================================================
def permutations(nums):
    """
    Generate all permutations.
    Time: O(n! * n), Space: O(n)
    """
    result = []
    used = [False] * len(nums)
    
    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                continue
            
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False
    
    backtrack([])
    return result


# ==============================================================================
# 15. DP - 1D (CLIMBING STAIRS / FIBONACCI)
# ==============================================================================
def climbing_stairs(n):
    """
    Number of ways to climb n stairs (1 or 2 steps at a time).
    Time: O(n), Space: O(1)
    """
    if n <= 2:
        return n
    
    prev2, prev1 = 1, 2
    
    for i in range(3, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    
    return prev1


# ==============================================================================
# 16. DP - COIN CHANGE (UNBOUNDED KNAPSACK)
# ==============================================================================
def coin_change(coins, amount):
    """
    Minimum coins to make amount.
    Time: O(amount * len(coins)), Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


# ==============================================================================
# 17. DP - 2D (LCS)
# ==============================================================================
def longest_common_subsequence(text1, text2):
    """
    Length of longest common subsequence.
    Time: O(m * n), Space: O(m * n) -> can optimize to O(n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


# ==============================================================================
# 18. TRIE
# ==============================================================================
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Time: O(len(word))"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        """Time: O(len(word))"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def starts_with(self, prefix):
        """Time: O(len(prefix))"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


# ==============================================================================
# 19. LRU CACHE
# ==============================================================================
class LRUCache:
    """
    Least Recently Used Cache.
    All operations O(1).
    Uses HashMap + Doubly Linked List.
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> node
        
        # Dummy head and tail
        self.head = ListNode(0, 0)
        self.tail = ListNode(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        """Remove node from list"""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_front(self, node):
        """Add node right after head (most recent)"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.val
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = ListNode(key, value)
        self.cache[key] = node
        self._add_to_front(node)
        
        if len(self.cache) > self.capacity:
            # Remove LRU (node before tail)
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


class ListNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


# ==============================================================================
# 20. UNION-FIND (DISJOINT SET)
# ==============================================================================
class UnionFind:
    """
    Union-Find with path compression and union by rank.
    Nearly O(1) per operation (amortized).
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        """Find with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union by rank, returns True if merged"""
        px, py = self.find(x), self.find(y)
        
        if px == py:
            return False  # Already in same set
        
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        return True


# ==============================================================================
# PRACTICE: Close this file, rebuild each template, and explain why each line is needed.
# ==============================================================================

"""
MEMORIZATION CHECKLIST:

[ ] Two Pointers - pair sum
[ ] Sliding Window - variable
[ ] Binary Search - standard
[ ] Binary Search - min condition
[ ] Monotonic Stack - next greater
[ ] Linked List - reverse
[ ] Linked List - find middle
[ ] Tree DFS - recursive
[ ] Tree BFS - level order
[ ] Graph BFS - shortest path
[ ] Graph DFS - islands
[ ] Heap - top k
[ ] Backtracking - subsets
[ ] Backtracking - permutations
[ ] DP 1D - climbing stairs
[ ] DP - coin change
[ ] DP 2D - LCS
[ ] Trie
[ ] LRU Cache
[ ] Union-Find

Goal: Write all 20 from memory in under 30 minutes.
"""
