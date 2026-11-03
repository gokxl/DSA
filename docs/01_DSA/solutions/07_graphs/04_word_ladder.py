"""
================================================================================
PROBLEM: Word Ladder (LeetCode 127)
Difficulty: Hard | Pattern: BFS Shortest Path
================================================================================

PROBLEM STATEMENT:
A transformation sequence from word beginWord to word endWord using a dictionary 
wordList is a sequence of words such that:

- The first word in the sequence is beginWord.
- The last word in the sequence is endWord.
- Only one letter can be changed at a time.
- Every word in the sequence (except beginWord) must be in wordList.

Given beginWord, endWord, and wordList, return the number of words in the 
shortest transformation sequence, or 0 if no such sequence exists.

EXAMPLES:
    Input: beginWord = "hit", endWord = "cog", 
           wordList = ["hot","dot","dog","lot","log","cog"]
    Output: 5
    Explanation: "hit" -> "hot" -> "dot" -> "dog" -> "cog" (5 words)

    Input: beginWord = "hit", endWord = "cog", 
           wordList = ["hot","dot","dog","lot","log"]
    Output: 0
    Explanation: "cog" is not in wordList, no valid transformation.

CONSTRAINTS:
- 1 <= beginWord.length <= 10
- endWord.length == beginWord.length
- 1 <= wordList.length <= 5000
- wordList[i].length == beginWord.length
- beginWord, endWord, and wordList[i] consist of lowercase English letters
- beginWord != endWord
- All words in wordList are unique

================================================================================
"""
from typing import List
from collections import deque, defaultdict
import string


# ============================================================================
# SOLUTION 1: BFS with Pattern Matching (Optimal)
# ============================================================================
def ladderLength(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """
    BFS to find shortest path.
    Use pattern matching (e.g., h*t) for O(1) neighbor lookup.
    
    Time: O(M² × N) where M = word length, N = wordList size
    Space: O(M² × N) for pattern dictionary
    """
    if endWord not in wordList:
        return 0
    
    word_len = len(beginWord)
    word_set = set(wordList)
    
    # Build pattern -> words mapping
    # e.g., "hot" -> ["h*t", "*ot", "ho*"]
    patterns = defaultdict(list)
    for word in wordList:
        for i in range(word_len):
            pattern = word[:i] + '*' + word[i+1:]
            patterns[pattern].append(word)
    
    # BFS
    queue = deque([(beginWord, 1)])  # (word, level)
    visited = {beginWord}
    
    while queue:
        word, level = queue.popleft()
        
        # Generate all patterns for current word
        for i in range(word_len):
            pattern = word[:i] + '*' + word[i+1:]
            
            for neighbor in patterns[pattern]:
                if neighbor == endWord:
                    return level + 1
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, level + 1))
    
    return 0


# ============================================================================
# SOLUTION 2: BFS with Character Replacement
# ============================================================================
def ladderLength_char_replace(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """
    BFS by trying all character replacements.
    Check if resulting word is in wordList.
    
    Time: O(M × N × 26) where M = word length, N = words visited
    Space: O(N)
    """
    if endWord not in wordList:
        return 0
    
    word_set = set(wordList)
    queue = deque([(beginWord, 1)])
    visited = {beginWord}
    
    while queue:
        word, level = queue.popleft()
        
        # Try replacing each character
        for i in range(len(word)):
            for c in string.ascii_lowercase:
                if c == word[i]:
                    continue
                
                new_word = word[:i] + c + word[i+1:]
                
                if new_word == endWord:
                    return level + 1
                
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, level + 1))
    
    return 0


# ============================================================================
# SOLUTION 3: Bidirectional BFS (Most Efficient)
# ============================================================================
def ladderLength_bidirectional(beginWord: str, endWord: str, wordList: List[str]) -> int:
    """
    BFS from both ends, meet in middle.
    Much faster when branching factor is high.
    
    Time: O(M² × N) but often much faster in practice
    Space: O(M² × N)
    """
    if endWord not in wordList:
        return 0
    
    word_set = set(wordList)
    word_len = len(beginWord)
    
    # Build pattern mapping
    patterns = defaultdict(list)
    for word in word_set:
        for i in range(word_len):
            pattern = word[:i] + '*' + word[i+1:]
            patterns[pattern].append(word)
    
    # Two sets for bidirectional BFS
    front = {beginWord}
    back = {endWord}
    visited = {beginWord, endWord}
    level = 1
    
    while front and back:
        # Always expand the smaller set
        if len(front) > len(back):
            front, back = back, front
        
        next_front = set()
        
        for word in front:
            for i in range(word_len):
                pattern = word[:i] + '*' + word[i+1:]
                
                for neighbor in patterns[pattern]:
                    if neighbor in back:
                        return level + 1
                    
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_front.add(neighbor)
        
        front = next_front
        level += 1
    
    return 0


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    beginWord1 = "hit"
    endWord1 = "cog"
    wordList1 = ["hot", "dot", "dog", "lot", "log", "cog"]
    print(f"Begin: '{beginWord1}', End: '{endWord1}'")
    print(f"WordList: {wordList1}")
    print(f"Ladder Length (Pattern): {ladderLength(beginWord1, endWord1, wordList1)}")
    print(f"Ladder Length (Char Replace): {ladderLength_char_replace(beginWord1, endWord1, wordList1)}")
    print(f"Ladder Length (Bidirectional): {ladderLength_bidirectional(beginWord1, endWord1, wordList1)}")
    # Expected: 5
    print()
    
    # Test Case 2: End word not in list
    beginWord2 = "hit"
    endWord2 = "cog"
    wordList2 = ["hot", "dot", "dog", "lot", "log"]
    print(f"Begin: '{beginWord2}', End: '{endWord2}'")
    print(f"Ladder Length: {ladderLength(beginWord2, endWord2, wordList2)}")
    # Expected: 0
    print()
    
    # Test Case 3: Direct transformation
    beginWord3 = "a"
    endWord3 = "c"
    wordList3 = ["a", "b", "c"]
    print(f"Begin: '{beginWord3}', End: '{endWord3}'")
    print(f"Ladder Length: {ladderLength(beginWord3, endWord3, wordList3)}")
    # Expected: 2
    print()
    
    # Test Case 4: No path
    beginWord4 = "hit"
    endWord4 = "cog"
    wordList4 = ["hot", "dot", "tod", "lot", "log"]
    print(f"No path case")
    print(f"Ladder Length: {ladderLength(beginWord4, endWord4, wordList4)}")
    # Expected: 0


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THIS IS SHORTEST PATH → USE BFS:
   
   BFS guarantees shortest path in unweighted graph.
   Each word = node, each valid transformation = edge.
   
   DFS would find A path but not necessarily shortest.

2. THE PATTERN TRICK:
   
   Instead of comparing all word pairs, use patterns:
   
   "hot" → ["*ot", "h*t", "ho*"]
   
   Two words are neighbors if they share a pattern.
   Preprocessing: O(M × N), Lookup: O(1)

3. WHY PATTERN IS BETTER:
   
   Direct comparison: O(M × N²) - compare all pairs
   Pattern matching: O(M² × N) - usually faster
   
   For M=10, N=5000: Pattern is much better!

4. BIDIRECTIONAL BFS:
   
   BFS from both beginWord AND endWord.
   Meet in the middle.
   
   Why faster?
   - Single BFS explores b^d nodes (b=branching, d=depth)
   - Bidirectional explores 2 × b^(d/2) nodes
   
   For b=26, d=10: 26^10 vs 2×26^5 = HUGE difference!

5. ALWAYS EXPAND SMALLER SET:
   
   In bidirectional BFS, expand the smaller frontier.
   Keeps both sides balanced, minimizing total nodes.

6. VISITED SET IS CRITICAL:
   
   Without visited, we'd revisit same words.
   Add to visited WHEN ADDING to queue, not when processing.
   (Prevents duplicate additions)

7. COMMON MISTAKES:
   
   ❌ Using DFS (doesn't give shortest path)
   ❌ Not checking if endWord is in wordList
   ❌ Adding to visited when dequeuing (duplicates in queue)

8. FOLLOW-UP: WORD LADDER II (LC 126)
   
   "Return all shortest transformation sequences"
   
   Much harder! Need to:
   - Track all shortest paths
   - Use BFS to find level of each word
   - Use DFS/backtrack to find all paths at optimal length

9. EDGE CASES:
   
   - endWord not in wordList → 0
   - beginWord == endWord (not possible per constraints)
   - No valid path → 0
   - beginWord in wordList (doesn't matter)

10. HOW TO EXPLAIN IT:
    
    Start with basic BFS + character replacement:
    
    "I'll use BFS since we need shortest path.
    For each word, try replacing each character with a-z,
    check if result is in wordList."
    
    Then optimize:
    
    "To improve, I can precompute pattern->words mapping.
    'hot' matches pattern 'h*t', so any word matching 'h*t'
    is a neighbor."
    
    If time permits, mention bidirectional BFS!

================================================================================
"""
