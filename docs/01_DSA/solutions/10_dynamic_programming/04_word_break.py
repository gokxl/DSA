"""
================================================================================
PROBLEM: Word Break (LeetCode 139)
Difficulty: Medium | Pattern: DP
================================================================================

PROBLEM STATEMENT:
Given a string s and a dictionary of strings wordDict, return true if s can 
be segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be reused multiple times in the 
segmentation.

EXAMPLES:
    Input: s = "leetcode", wordDict = ["leet","code"]
    Output: true
    Explanation: "leetcode" can be segmented as "leet code"

    Input: s = "applepenapple", wordDict = ["apple","pen"]
    Output: true
    Explanation: "applepenapple" = "apple pen apple"

    Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
    Output: false

CONSTRAINTS:
- 1 <= s.length <= 300
- 1 <= wordDict.length <= 1000
- 1 <= wordDict[i].length <= 20
- s and wordDict[i] consist of only lowercase English letters
- All the strings of wordDict are unique

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Bottom-Up DP
# ============================================================================
def wordBreak(s: str, wordDict: List[str]) -> bool:
    """
    dp[i] = True if s[0:i] can be segmented
    
    dp[i] = True if any dp[j] is True AND s[j:i] is a word
    
    Time: O(n² × m) where n = len(s), m = max word length
    Space: O(n)
    """
    word_set = set(wordDict)
    n = len(s)
    
    # dp[i] = True if s[0:i] can be segmented
    dp = [False] * (n + 1)
    dp[0] = True  # Empty string
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break  # No need to check further
    
    return dp[n]


# ============================================================================
# SOLUTION 2: Optimized DP (Check word lengths only)
# ============================================================================
def wordBreak_optimized(s: str, wordDict: List[str]) -> bool:
    """
    Only check substrings of lengths that exist in dictionary.
    
    Time: O(n × w × m) where w = unique word lengths
    Space: O(n)
    """
    word_set = set(wordDict)
    word_lengths = set(len(w) for w in wordDict)
    n = len(s)
    
    dp = [False] * (n + 1)
    dp[0] = True
    
    for i in range(1, n + 1):
        for length in word_lengths:
            j = i - length
            if j >= 0 and dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    
    return dp[n]


# ============================================================================
# SOLUTION 3: Top-Down DP with Memoization
# ============================================================================
def wordBreak_memo(s: str, wordDict: List[str]) -> bool:
    """
    Recursive approach with memoization.
    
    Time: O(n² × m)
    Space: O(n)
    """
    word_set = set(wordDict)
    memo = {}
    
    def dp(start: int) -> bool:
        if start == len(s):
            return True
        
        if start in memo:
            return memo[start]
        
        for end in range(start + 1, len(s) + 1):
            if s[start:end] in word_set and dp(end):
                memo[start] = True
                return True
        
        memo[start] = False
        return False
    
    return dp(0)


# ============================================================================
# SOLUTION 4: BFS Approach
# ============================================================================
from collections import deque

def wordBreak_bfs(s: str, wordDict: List[str]) -> bool:
    """
    BFS: Each valid prefix leads to checking remaining suffix.
    
    Time: O(n² × m)
    Space: O(n)
    """
    word_set = set(wordDict)
    n = len(s)
    
    queue = deque([0])  # Starting positions
    visited = set([0])
    
    while queue:
        start = queue.popleft()
        
        if start == n:
            return True
        
        for end in range(start + 1, n + 1):
            if end not in visited and s[start:end] in word_set:
                queue.append(end)
                visited.add(end)
    
    return False


# ============================================================================
# SOLUTION 5: Using Trie (Good for many words)
# ============================================================================
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


def wordBreak_trie(s: str, wordDict: List[str]) -> bool:
    """
    Build Trie from dictionary, then DP with Trie lookup.
    
    Time: O(n² + m × k) where m = dict size, k = avg word length
    Space: O(m × k) for Trie
    """
    # Build Trie
    root = TrieNode()
    for word in wordDict:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
    
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    
    for i in range(n):
        if not dp[i]:
            continue
        
        node = root
        for j in range(i, n):
            if s[j] not in node.children:
                break
            node = node.children[s[j]]
            if node.is_word:
                dp[j + 1] = True
    
    return dp[n]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    s1, dict1 = "leetcode", ["leet", "code"]
    print(f"s = '{s1}', wordDict = {dict1}")
    print(f"DP: {wordBreak(s1, dict1)}")
    print(f"Memo: {wordBreak_memo(s1, dict1)}")
    # Expected: True
    print()
    
    # Test Case 2: Reuse word
    s2, dict2 = "applepenapple", ["apple", "pen"]
    print(f"s = '{s2}', wordDict = {dict2}")
    print(f"Result: {wordBreak(s2, dict2)}")
    # Expected: True
    print()
    
    # Test Case 3: Cannot segment
    s3, dict3 = "catsandog", ["cats", "dog", "sand", "and", "cat"]
    print(f"s = '{s3}', wordDict = {dict3}")
    print(f"Result: {wordBreak(s3, dict3)}")
    # Expected: False
    print()
    
    # Test Case 4: Single word
    s4, dict4 = "hello", ["hello"]
    print(f"s = '{s4}', wordDict = {dict4}")
    print(f"Result: {wordBreak_bfs(s4, dict4)}")
    # Expected: True
    print()
    
    # Test Case 5: Using Trie
    s5, dict5 = "pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]
    print(f"Trie approach: {wordBreak_trie(s5, dict5)}")
    # Expected: True


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. DP DEFINITION:
   
   dp[i] = True if s[0:i] can be segmented using dictionary words
   
   Base: dp[0] = True (empty string)
   Transition: dp[i] = any(dp[j] and s[j:i] in dict) for j < i

2. OPTIMIZATION: CHECK WORD LENGTHS:
   
   Instead of trying all j from 0 to i-1,
   only try j = i - len(word) for each word length.
   
   word_lengths = set(len(w) for w in wordDict)

3. WHY SET FOR DICTIONARY?
   
   O(1) lookup for "is this substring a word?"
   
   word_set = set(wordDict)

4. BFS INTERPRETATION:
   
   Think of it as graph traversal:
   - Node i represents position i in string
   - Edge from i to j if s[i:j] is a word
   - Question: Can we reach node n from node 0?

5. TRIE OPTIMIZATION:
   
   When dictionary is large, Trie helps:
   - Build Trie from all words
   - At each position, traverse Trie to find valid words
   
   Good when many words share prefixes.

6. TIME COMPLEXITY:
   
   Basic: O(n² × m) where m = max word length (for substring comparison)
   Optimized: O(n × w × m) where w = unique word lengths
   
   String comparison is O(m) for substring of length m.

7. WORD BREAK II (LC 140):
   
   Return all possible segmentations.
   Solution: Backtracking + memoization
   
   Much harder - exponential number of results possible!

8. COMMON MISTAKES:
   
   ❌ Forgetting dp[0] = True
   ❌ Not using set for dictionary (slow lookup)
   ❌ Using backtracking without memoization (TLE)

9. RELATED PROBLEMS:
   
   - Word Break II (LC 140)
   - Concatenated Words (LC 472)
   - Palindrome Partitioning (LC 131)

10. practice TIP:
    
    "I'll use DP where dp[i] = true if s[0:i] can be segmented.
    For each position i, I check all previous positions j:
    if dp[j] is true and s[j:i] is in the dictionary, then dp[i] = true.
    
    I'll use a set for O(1) word lookup.
    
    Optimization: Only check substrings whose lengths match
    words in the dictionary."
    
    Mention the BFS interpretation - shows graph thinking!

================================================================================
"""
