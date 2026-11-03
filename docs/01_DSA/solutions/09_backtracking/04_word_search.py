"""
================================================================================
PROBLEM: Word Search (LeetCode 79)
Difficulty: Medium | Pattern: Backtracking + DFS
================================================================================

PROBLEM STATEMENT:
Given an m x n grid of characters board and a string word, return true if word 
exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where 
adjacent cells are horizontally or vertically neighboring. The same letter cell 
may not be used more than once.

EXAMPLES:
    Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], 
           word = "ABCCED"
    Output: true
    
    A B C E
    S F C S
    A D E E
    
    Path: A(0,0) → B(0,1) → C(0,2) → C(1,2) → E(2,2) → D(2,1)

    Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], 
           word = "SEE"
    Output: true

    Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], 
           word = "ABCB"
    Output: false
    Explanation: Can't reuse the B at (0,1)

CONSTRAINTS:
- m == board.length
- n == board[i].length
- 1 <= m, n <= 6
- 1 <= word.length <= 15
- board and word consists of only lowercase and uppercase English letters

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: DFS Backtracking
# ============================================================================
def exist(board: List[List[str]], word: str) -> bool:
    """
    DFS from each starting cell that matches first character.
    Mark cells as visited during path, unmark on backtrack.
    
    Time: O(m × n × 4^L) where L = word length
    Space: O(L) for recursion
    """
    rows, cols = len(board), len(board[0])
    
    def dfs(r: int, c: int, idx: int) -> bool:
        # Found complete word
        if idx == len(word):
            return True
        
        # Out of bounds or wrong character or already visited
        if (r < 0 or r >= rows or c < 0 or c >= cols or 
            board[r][c] != word[idx]):
            return False
        
        # Mark as visited
        temp = board[r][c]
        board[r][c] = '#'
        
        # Explore all 4 directions
        found = (dfs(r + 1, c, idx + 1) or
                 dfs(r - 1, c, idx + 1) or
                 dfs(r, c + 1, idx + 1) or
                 dfs(r, c - 1, idx + 1))
        
        # Backtrack
        board[r][c] = temp
        
        return found
    
    # Try starting from each cell
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0] and dfs(r, c, 0):
                return True
    
    return False


# ============================================================================
# SOLUTION 2: With Explicit Visited Set
# ============================================================================
def exist_visited_set(board: List[List[str]], word: str) -> bool:
    """
    Use separate visited set instead of modifying board.
    
    Time: O(m × n × 4^L)
    Space: O(L) for recursion + O(L) for visited set
    """
    rows, cols = len(board), len(board[0])
    visited = set()
    
    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or board[r][c] != word[idx]):
            return False
        
        visited.add((r, c))
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if dfs(r + dr, c + dc, idx + 1):
                return True
        
        visited.remove((r, c))
        return False
    
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    
    return False


# ============================================================================
# SOLUTION 3: With Pruning (Optimized)
# ============================================================================
def exist_optimized(board: List[List[str]], word: str) -> bool:
    """
    Add pruning: check if all characters exist in board first.
    Also reverse word if last char is less frequent.
    
    Time: O(m × n × 4^L) but with better pruning
    Space: O(L)
    """
    from collections import Counter
    
    rows, cols = len(board), len(board[0])
    
    # Count characters in board
    board_counter = Counter()
    for row in board:
        board_counter.update(row)
    
    # Check if word can be formed
    word_counter = Counter(word)
    for char, count in word_counter.items():
        if board_counter[char] < count:
            return False
    
    # Reverse word if last char is less frequent (pruning optimization)
    if board_counter[word[0]] > board_counter[word[-1]]:
        word = word[::-1]
    
    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        
        if (r < 0 or r >= rows or c < 0 or c >= cols or 
            board[r][c] != word[idx]):
            return False
        
        temp = board[r][c]
        board[r][c] = '#'
        
        found = (dfs(r + 1, c, idx + 1) or
                 dfs(r - 1, c, idx + 1) or
                 dfs(r, c + 1, idx + 1) or
                 dfs(r, c - 1, idx + 1))
        
        board[r][c] = temp
        return found
    
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    
    return False


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case - found
    board1 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    word1 = "ABCCED"
    print(f"Board:")
    for row in board1:
        print(row)
    print(f"Word: {word1}")
    print(f"Exists: {exist([row[:] for row in board1], word1)}")
    # Expected: True
    print()
    
    # Test Case 2: Another valid word
    word2 = "SEE"
    print(f"Word: {word2}")
    print(f"Exists: {exist([row[:] for row in board1], word2)}")
    # Expected: True
    print()
    
    # Test Case 3: Can't reuse cell
    word3 = "ABCB"
    print(f"Word: {word3}")
    print(f"Exists: {exist([row[:] for row in board1], word3)}")
    # Expected: False
    print()
    
    # Test Case 4: Single cell
    board4 = [["A"]]
    word4 = "A"
    print(f"Single cell: {exist(board4, word4)}")
    # Expected: True
    print()
    
    # Test Case 5: Word longer than possible
    word5 = "ABCDEFGHIJ"
    print(f"Long word: {exist([row[:] for row in board1], word5)}")
    # Expected: False


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. BACKTRACKING ON GRID:
   
   Mark cell as visited → Explore 4 directions → Unmark
   
   temp = board[r][c]
   board[r][c] = '#'  # Mark visited
   # ... explore ...
   board[r][c] = temp  # Backtrack

2. WHY BACKTRACKING NEEDED?
   
   Same cell can be part of multiple paths.
   We need to "unvisit" to try other paths.
   
   Example: "ABCB" - B might be needed later

3. IN-PLACE VS VISITED SET:
   
   In-place (modify board):
   - No extra space for visited
   - Slightly faster
   
   Visited set:
   - Cleaner code
   - Doesn't modify input

4. TIME COMPLEXITY:
   
   O(m × n × 4^L)
   - m × n starting positions
   - 4 directions at each step
   - L = word length (max depth)
   
   Actually less due to backtracking and pruning

5. PRUNING OPTIMIZATIONS:
   
   a) Check character existence first:
      Count chars in board, compare with word
   
   b) Start from rarer character:
      If last char is rarer, reverse word
   
   c) Early termination:
      Return immediately when found

6. COMMON MISTAKES:
   
   ❌ Forgetting to backtrack (unmark visited)
   ❌ Not checking bounds before character
   ❌ Using visited globally instead of per-path

7. TERMINATION CONDITIONS ORDER:
   
   1. Check if word complete (idx == len(word)) → True
   2. Check bounds
   3. Check if visited
   4. Check if character matches
   
   Order matters for correctness!

8. FOLLOW-UP: WORD SEARCH II (LC 212):
   
   Find all words from dictionary in grid.
   Solution: Build Trie from words, then DFS.
   
   Much more complex - know the approach!

9. RELATED PROBLEMS:
   
   - Word Search II (LC 212) - Trie + DFS
   - Number of Islands (LC 200)
   - Surrounded Regions (LC 130)

10. practice TIP:
    
    "I'll use DFS backtracking from each cell that matches
    the first character.
    
    At each cell, I mark it visited (using '#'), explore
    all 4 directions for the next character, then unmark
    it to allow other paths to use this cell.
    
    Time is O(m × n × 4^L) where L is word length, but
    pruning makes it much faster in practice."
    
    Mention the optimization of checking char counts first!

================================================================================
"""
