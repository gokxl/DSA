# Pattern Recognition Cheat Sheet

Goal: Identify the pattern in under 3 minutes.

---

## Pattern Detection Flowchart

```
Read the problem
      |
      v
Is it asking for SUBSTRING/SUBARRAY with constraint?
      | YES --> SLIDING WINDOW
      | NO
      v
Is array SORTED or can sorting help?
      | YES --> TWO POINTERS or BINARY SEARCH
      | NO
      v
Need to find/count PAIRS with condition?
      | YES --> HASHMAP (Two Sum pattern)
      | NO
      v
Need NEXT GREATER/SMALLER element?
      | YES --> MONOTONIC STACK
      | NO
      v
Is it a TREE structure?
      | YES --> DFS/BFS (recursion or stack/queue)
      | NO
      v
Is it a GRAPH with edges?
      | YES --> BFS (shortest path) or DFS (all paths)
      | NO
      v
Need TOP K or MIN/MAX streaming?
      | YES --> HEAP
      | NO
      v
Generate ALL combinations/permutations?
      | YES --> BACKTRACKING
      | NO
      v
Can break into OVERLAPPING subproblems?
      | YES --> DYNAMIC PROGRAMMING
      | NO
      v
Can make LOCALLY OPTIMAL choice at each step?
      | YES --> GREEDY
      | NO --> Probably a DESIGN problem
```

---

## Keyword to Pattern Mapping

| If you see these words... | Use this pattern |
|---------------------------|------------------|
| subarray, substring, contiguous, window | Sliding Window |
| sorted array, find pair, minimize difference | Two Pointers |
| search sorted, minimum/maximum that works | Binary Search |
| parentheses, valid brackets, matching | Stack |
| next greater, next smaller, span | Monotonic Stack |
| tree, root, leaves, depth, height | Tree DFS/BFS |
| graph, connected, path, cycle | Graph BFS/DFS |
| top k, k largest/smallest, median | Heap |
| all combinations, all permutations, all paths | Backtracking |
| minimum cost, maximum profit, number of ways | DP |
| intervals, scheduling | Greedy |
| implement, design, data structure | Design |

---

## Pattern Templates

### 1. Two Pointers

**When to use:** Sorted array, find pairs, minimize distance, in-place modification

```python
def two_pointers(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        if condition_met(arr, left, right):
            return result
        elif need_bigger:
            left += 1
        else:
            right -= 1
```

**Key problems:** Two Sum (sorted), 3Sum, Container With Most Water, Trapping Rain Water

---

### 2. Sliding Window

**When to use:** Contiguous subarray/substring with constraint (max length, sum <= k, distinct chars)

```python
def sliding_window(s):
    left = 0
    window = {}
    result = 0
    
    for right in range(len(s)):
        # Add s[right] to window
        window[s[right]] = window.get(s[right], 0) + 1
        
        # Shrink window while invalid
        while not valid(window):
            window[s[left]] -= 1
            left += 1
        
        # Update result
        result = max(result, right - left + 1)
    
    return result
```

**Key problems:** Longest Substring Without Repeating, Minimum Window Substring, Find All Anagrams

---

### 3. Binary Search

**When to use:** Sorted array, minimize/maximize something, search space can be halved

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

**Binary search on answer:**
```python
def binary_search_answer(lo, hi):
    while lo < hi:
        mid = (lo + hi) // 2
        if can_achieve(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Key problems:** Search Rotated Array, Koko Eating Bananas, Find Peak Element

---

### 4. Stack / Monotonic Stack

**When to use:** Matching brackets, next greater/smaller, expression evaluation

```python
def next_greater(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # stores indices
    
    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            result[stack.pop()] = nums[i]
        stack.append(i)
    
    return result
```

**Key problems:** Valid Parentheses, Daily Temperatures, Largest Rectangle in Histogram

---

### 5. Linked List

**When to use:** In-place modification, find middle, detect cycle, reverse

```python
def reverse_list(head):
    prev, curr = None, head
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    return prev

def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

**Key problems:** Reverse Linked List, Linked List Cycle, Merge Two Sorted Lists

---

### 6. Trees (DFS/BFS)

**When to use:** Tree traversal, path problems, level-by-level processing

```python
# DFS Recursive
def dfs(node):
    if not node:
        return base_case
    
    left = dfs(node.left)
    right = dfs(node.right)
    
    return combine(left, right, node.val)

# BFS Level Order
from collections import deque

def bfs(root):
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
```

**Key problems:** Max Depth, Level Order, Validate BST, Lowest Common Ancestor

---

### 7. Graphs (BFS/DFS)

**When to use:** Connected components, shortest path, cycle detection, traversal

```python
# BFS - Shortest Path
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([(start, 0)])
    
    while queue:
        node, dist = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

# DFS - Components / Islands
def dfs(r, c, grid):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return
    if grid[r][c] == '0':
        return
    
    grid[r][c] = '0'  # Mark visited
    dfs(r + 1, c, grid)
    dfs(r - 1, c, grid)
    dfs(r, c + 1, grid)
    dfs(r, c - 1, grid)
```

**Key problems:** Number of Islands, Clone Graph, Course Schedule, Word Ladder

---

### 8. Heap / Priority Queue

**When to use:** Top K, streaming data, merge sorted lists, scheduling

```python
import heapq

def top_k_elements(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap

# Note: Python has min heap. For max heap, negate values.
```

**Key problems:** Top K Frequent, Merge K Sorted Lists, Meeting Rooms II

---

### 9. Backtracking

**When to use:** Generate all combinations/permutations/subsets, constraint satisfaction

```python
def backtrack(path, choices):
    if is_solution(path):
        result.append(path[:])  # Make a copy!
        return
    
    for choice in choices:
        if is_valid(choice, path):
            path.append(choice)
            backtrack(path, remaining_choices)
            path.pop()  # Backtrack
```

**Key problems:** Subsets, Permutations, Combinations, Word Search, N-Queens

---

### 10. Dynamic Programming

**When to use:** Overlapping subproblems, optimal substructure, "number of ways", "minimum cost"

```python
# 1D DP
def dp_1d(n):
    dp = [0] * (n + 1)
    dp[0] = base_case
    
    for i in range(1, n + 1):
        dp[i] = recurrence(dp[i-1], dp[i-2])
    
    return dp[n]

# 2D DP
def dp_2d(m, n):
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = recurrence(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

**Key problems:** Climbing Stairs, Coin Change, House Robber, LCS, Edit Distance

---

### 11. Greedy

**When to use:** Local optimal choice leads to global optimal, interval scheduling

**Key insight:** Prove greedy works before coding (exchange argument)

**Key problems:** Jump Game, Merge Intervals, Non-overlapping Intervals

---

### 12. Design

**When to use:** "Design a data structure", "implement X with O(1) operations"

**Key problems:** LRU Cache (HashMap + Doubly Linked List), Min Stack (Two stacks), Trie (Dict of children)

---

## Common Mistakes by Pattern

| Pattern | Common Mistake | Fix |
|---------|---------------|-----|
| Two Pointers | Forgetting to handle duplicates | Skip duplicates after finding answer |
| Sliding Window | Not shrinking window correctly | Shrink until valid again |
| Binary Search | Off-by-one errors | Draw out examples on paper |
| Stack | Empty stack access | Check `if stack:` before pop |
| Trees | Not handling None nodes | Always check `if not node: return` |
| Graphs | Infinite loops | Always use visited set |
| Heap | Using wrong heap type | Max heap needs negative values |
| Backtracking | Forgetting to remove choice | Always `path.pop()` after recursion |
| DP | Wrong base case | What's the smallest subproblem? |
| Greedy | Assuming greedy works | Ask: can I prove local = global? |

---

Use the flowchart to reason from constraints to a pattern, and understand why each pattern fits.
