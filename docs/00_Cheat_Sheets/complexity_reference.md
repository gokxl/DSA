# Complexity Reference

State complexity immediately after coding. Don't wait to be asked.

---

## Big-O at a Glance

| Complexity | Name | Example | n=1000 |
|------------|------|---------|--------|
| O(1) | Constant | Array access, HashMap get | 1 |
| O(log n) | Logarithmic | Binary search | 10 |
| O(n) | Linear | Single loop | 1,000 |
| O(n log n) | Linearithmic | Merge sort, heap sort | 10,000 |
| O(n²) | Quadratic | Nested loops | 1,000,000 |
| O(2ⁿ) | Exponential | Subsets, recursive fib | Very large |
| O(n!) | Factorial | Permutations | Huge |

---

## Complexity by Pattern

### Arrays / Two Pointers

| Operation | Time | Space |
|-----------|------|-------|
| Two Sum (sorted) | O(n) | O(1) |
| 3Sum | O(n²) | O(1) |
| Container With Most Water | O(n) | O(1) |
| Trapping Rain Water | O(n) | O(1) |

### Sliding Window

| Operation | Time | Space |
|-----------|------|-------|
| Fixed window | O(n) | O(k) |
| Variable window | O(n) | O(n) worst |
| Minimum Window Substring | O(n + m) | O(m) |

### Binary Search

| Operation | Time | Space |
|-----------|------|-------|
| Standard binary search | O(log n) | O(1) |
| Binary search on answer | O(n log k) | O(1) |
| Search rotated array | O(log n) | O(1) |

### Stack

| Operation | Time | Space |
|-----------|------|-------|
| Push/Pop | O(1) | - |
| Valid parentheses | O(n) | O(n) |
| Monotonic stack (next greater) | O(n) | O(n) |
| Largest rectangle histogram | O(n) | O(n) |

### Linked List

| Operation | Time | Space |
|-----------|------|-------|
| Access by index | O(n) | - |
| Insert/Delete at head | O(1) | - |
| Reverse | O(n) | O(1) |
| Find middle | O(n) | O(1) |
| Detect cycle | O(n) | O(1) |

### Trees

| Operation | Time | Space |
|-----------|------|-------|
| DFS traversal | O(n) | O(h) |
| BFS traversal | O(n) | O(w) |
| BST search (balanced) | O(log n) | O(1) |
| Level order | O(n) | O(n) |

h = height, w = max width

### Graphs

| Operation | Time | Space |
|-----------|------|-------|
| DFS | O(V + E) | O(V) |
| BFS | O(V + E) | O(V) |
| Dijkstra | O((V+E) log V) | O(V) |
| Topological Sort | O(V + E) | O(V) |

### Heap

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(log n) | - |
| Extract min/max | O(log n) | - |
| Peek | O(1) | - |
| Heapify | O(n) | - |
| Top K elements | O(n log k) | O(k) |
| Merge K sorted lists | O(n log k) | O(k) |

### Backtracking

| Operation | Time | Space |
|-----------|------|-------|
| Subsets | O(2ⁿ) | O(n) |
| Permutations | O(n!) | O(n) |
| Combinations | O(C(n,k)) | O(k) |

### Dynamic Programming

| Pattern | Time | Space |
|---------|------|-------|
| 1D DP (climbing stairs) | O(n) | O(n) or O(1) |
| 2D DP (LCS, edit distance) | O(m×n) | O(m×n) or O(n) |
| Knapsack | O(n×W) | O(W) |

### Design

| Data Structure | Get | Put | Delete |
|---------------|-----|-----|--------|
| LRU Cache | O(1) | O(1) | O(1) |
| Min Stack | O(1) | O(1) | O(1) |
| Trie | O(L) | O(L) | O(L) |

L = length of word

---

## Space Complexity Tips

### What Counts as Space

Counts:
- Extra arrays/lists you create
- HashMap/HashSet storage
- Recursion call stack depth
- Queue/Stack you use

Usually doesn't count:
- Input array (unless you modify it)
- Output array (sometimes)
- A few variables (O(1))

### Recursion Stack Space

| Type | Stack Depth |
|------|-------------|
| Tree DFS | O(h) where h = height |
| Balanced BST | O(log n) |
| Skewed tree | O(n) |
| Graph DFS | O(V) worst |
| Binary search recursive | O(log n) |

---

## Warning Signs (Usually Too Slow)

| If your solution is... | For n = 10⁵... | Action |
|------------------------|----------------|--------|
| O(n³) | Too slow | Rethink approach |
| O(n²) | Too slow | Need O(n log n) or O(n) |
| O(2ⁿ) for n > 25 | Too slow | Need DP with memoization |
| O(n!) for n > 10 | Too slow | Need pruning or DP |

---

## How to State Complexity

**Good:**
> "The time complexity is O(n) where n is the length of the input array. We iterate through the array once, and each HashMap operation is O(1). The space complexity is O(n) because in the worst case we store all n elements in the HashMap."

**Bad:**
> "It's O(n)."

**Template:**
> "Time complexity is O(___) because [main loop/recursion explanation]. Space complexity is O(___) because [what we're storing]."

---

## Common Optimizations

| From | To | How |
|------|-----|-----|
| O(n²) | O(n log n) | Sort + two pointers |
| O(n²) | O(n) | HashMap instead of nested loop |
| O(2ⁿ) | O(n²) or O(n³) | DP with memoization |
| O(n) space | O(1) space | Rolling array for DP |

---

## Python Operations Reference

| Operation | List | Dict | Set |
|-----------|------|------|-----|
| Access | O(1) | O(1) | - |
| Search | O(n) | O(1) | O(1) |
| Insert | O(n) | O(1) | O(1) |
| Append | O(1) | - | - |
| Delete | O(n) | O(1) | O(1) |

---

Memorize the patterns table. Always state complexity immediately after coding.
