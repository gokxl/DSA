"""
================================================================================
PROBLEM: Alien Dictionary (LeetCode 269)
Difficulty: Hard | Pattern: Topological Sort
================================================================================

PROBLEM STATEMENT:
There is a new alien language that uses the English alphabet. However, the order 
of the letters is unknown to you.

You are given a list of strings words from the alien language's dictionary, 
where the strings in words are sorted lexicographically by the rules of this 
new language.

Derive the order of letters in this language. If the order is invalid, return "".
If there are multiple valid orders, return any of them.

EXAMPLES:
    Input: words = ["wrt","wrf","er","ett","rftt"]
    Output: "wertf"
    Explanation:
    - "wrt" < "wrf" → t < f (at position 2)
    - "wrf" < "er"  → w < e (at position 0)
    - "er" < "ett"  → r < t (at position 1)
    - "ett" < "rftt"→ e < r (at position 0)
    Order: w < e < r < t < f

    Input: words = ["z","x"]
    Output: "zx"
    Explanation: "z" < "x" → z < x

    Input: words = ["z","x","z"]
    Output: ""
    Explanation: Order "z" < "x" and "x" < "z" - contradiction (cycle)

CONSTRAINTS:
- 1 <= words.length <= 100
- 1 <= words[i].length <= 100
- words[i] consists of only lowercase English letters

================================================================================
"""
from typing import List
from collections import defaultdict, deque


# ============================================================================
# SOLUTION 1: BFS Topological Sort (Kahn's Algorithm)
# ============================================================================
def alienOrder(words: List[str]) -> str:
    """
    Build graph from word comparisons, then topological sort.
    
    1. Extract ordering relationships from adjacent words
    2. Build directed graph and in-degree map
    3. Topological sort using BFS (Kahn's algorithm)
    
    Time: O(C) where C = total characters in all words
    Space: O(U) where U = unique characters
    """
    # Step 1: Initialize graph with all unique characters
    graph = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}
    
    # Step 2: Build graph from adjacent word pairs
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        
        # Check for invalid case: "abc" before "ab"
        if len(word1) > len(word2) and word1.startswith(word2):
            return ""
        
        # Find first different character
        for c1, c2 in zip(word1, word2):
            if c1 != c2:
                if c2 not in graph[c1]:  # Avoid duplicate edges
                    graph[c1].add(c2)
                    in_degree[c2] += 1
                break  # Only first difference matters
    
    # Step 3: Topological sort (Kahn's algorithm)
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []
    
    while queue:
        c = queue.popleft()
        result.append(c)
        
        for neighbor in graph[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If not all characters included, there's a cycle
    if len(result) != len(in_degree):
        return ""
    
    return ''.join(result)


# ============================================================================
# SOLUTION 2: DFS Topological Sort
# ============================================================================
def alienOrder_dfs(words: List[str]) -> str:
    """
    DFS approach for topological sort.
    
    Time: O(C)
    Space: O(U)
    """
    # Build graph
    graph = defaultdict(set)
    all_chars = set()
    
    for word in words:
        all_chars.update(word)
    
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        
        if len(word1) > len(word2) and word1.startswith(word2):
            return ""
        
        for c1, c2 in zip(word1, word2):
            if c1 != c2:
                graph[c1].add(c2)
                break
    
    # DFS topological sort
    # State: 0 = not visited, 1 = visiting, 2 = visited
    state = {c: 0 for c in all_chars}
    result = []
    
    def dfs(c: str) -> bool:
        """Returns False if cycle detected"""
        if state[c] == 1:
            return False  # Cycle
        if state[c] == 2:
            return True  # Already processed
        
        state[c] = 1  # Visiting
        
        for neighbor in graph[c]:
            if not dfs(neighbor):
                return False
        
        state[c] = 2  # Visited
        result.append(c)
        return True
    
    for c in all_chars:
        if state[c] == 0:
            if not dfs(c):
                return ""
    
    return ''.join(reversed(result))


# ============================================================================
# SOLUTION 3: BFS with detailed validation
# ============================================================================
def alienOrder_detailed(words: List[str]) -> str:
    """
    More explicit validation with comments.
    
    Time: O(C)
    Space: O(U)
    """
    # Collect all characters
    chars = set()
    for word in words:
        chars.update(word)
    
    # Build adjacency list and in-degree
    adj = {c: [] for c in chars}
    in_deg = {c: 0 for c in chars}
    
    # Compare adjacent words
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        
        # Invalid: longer word comes before its prefix
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        
        # Find first difference
        for j in range(min_len):
            if w1[j] != w2[j]:
                adj[w1[j]].append(w2[j])
                in_deg[w2[j]] += 1
                break
    
    # BFS
    queue = deque([c for c in chars if in_deg[c] == 0])
    order = []
    
    while queue:
        c = queue.popleft()
        order.append(c)
        
        for next_c in adj[c]:
            in_deg[next_c] -= 1
            if in_deg[next_c] == 0:
                queue.append(next_c)
    
    return ''.join(order) if len(order) == len(chars) else ""


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    words1 = ["wrt", "wrf", "er", "ett", "rftt"]
    print(f"Words: {words1}")
    print(f"Alien Order (BFS): {alienOrder(words1)}")
    print(f"Alien Order (DFS): {alienOrder_dfs(words1)}")
    # Expected: "wertf" (or any valid order)
    print()
    
    # Test Case 2: Simple case
    words2 = ["z", "x"]
    print(f"Words: {words2}")
    print(f"Alien Order: {alienOrder(words2)}")
    # Expected: "zx"
    print()
    
    # Test Case 3: Cycle (invalid)
    words3 = ["z", "x", "z"]
    print(f"Words: {words3}")
    print(f"Alien Order: {alienOrder(words3)}")
    # Expected: "" (cycle: z < x and x < z)
    print()
    
    # Test Case 4: Invalid prefix order
    words4 = ["abc", "ab"]
    print(f"Words: {words4}")
    print(f"Alien Order: {alienOrder(words4)}")
    # Expected: "" (longer word can't come before prefix)
    print()
    
    # Test Case 5: Single word
    words5 = ["abc"]
    print(f"Words: {words5}")
    print(f"Alien Order: {alienOrder(words5)}")
    # Expected: "abc" (any order of a, b, c)
    print()
    
    # Test Case 6: All same characters
    words6 = ["z", "z"]
    print(f"Words: {words6}")
    print(f"Alien Order: {alienOrder(words6)}")
    # Expected: "z"


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE KEY INSIGHT - EXTRACT ORDERING:
   
   Compare ADJACENT words to find character ordering:
   
   "wrt" < "wrf" → First difference at position 2: t < f
   
   Only the FIRST different character gives us information!
   After that, we don't know the relative order.

2. BUILDING THE GRAPH:
   
   For each pair of adjacent words:
   1. Find first position where they differ
   2. Add edge: word1[pos] → word2[pos]
   3. Only add ONE edge per word pair
   
   Characters with no edges can appear anywhere in order.

3. INVALID CASE - PREFIX CHECK:
   
   "abc" before "ab" is INVALID!
   
   In any dictionary, shorter prefix comes first.
   "ab" < "abc" is correct.
   
   if len(word1) > len(word2) and word1.startswith(word2):
       return ""

4. DETECT CYCLES:
   
   Cycle in graph = contradiction = impossible ordering
   
   BFS: If not all chars in result, cycle exists
   DFS: If we revisit a "visiting" node, cycle exists

5. INCLUDE ALL CHARACTERS:
   
   Don't forget characters that have no ordering constraints!
   
   Initialize: all_chars = {c for word in words for c in word}
   
   These can appear anywhere in final order.

6. EDGE CASE - DUPLICATE EDGES:
   
   Comparing "abc" with "abd" and "axc" with "axd"
   both give c < d edge.
   
   Use set for adjacency to avoid counting twice:
   graph[c1].add(c2)
   
   Or check before adding to in-degree.

7. TIME COMPLEXITY:
   
   O(C) where C = total characters across all words
   
   - Building graph: O(C)
   - Topological sort: O(V + E) where V = unique chars, E = edges

8. COMMON MISTAKES:
   
   ❌ Not handling prefix case ("abc" < "ab")
   ❌ Using all chars from both words (only use first diff)
   ❌ Counting duplicate edges in in-degree
   ❌ Forgetting standalone characters

9. FOLLOW-UP VARIATIONS:
   
   - Verify if given order is valid for the words
   - Find lexicographically smallest valid order
   - Count number of valid orderings

10. HOW TO EXPLAIN IT:
    
    Walk through an example step by step:
    
    "For ['wrt', 'wrf', 'er']:
    - Compare 'wrt' and 'wrf': t < f (position 2)
    - Compare 'wrf' and 'er': w < e (position 0)
    
    So edges: t→f, w→e
    
    Topological sort starting from in-degree 0..."
    
    This shows clear thinking!

================================================================================
"""
