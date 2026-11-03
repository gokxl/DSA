"""
================================================================================
PROBLEM: Edit Distance (LeetCode 72)
Difficulty: Medium | Pattern: DP (2D)
================================================================================

PROBLEM STATEMENT:
Given two strings word1 and word2, return the minimum number of operations 
required to convert word1 to word2.

You have the following three operations permitted on a word:
- Insert a character
- Delete a character
- Replace a character

EXAMPLES:
    Input: word1 = "horse", word2 = "ros"
    Output: 3
    Explanation: 
    horse -> rorse (replace 'h' with 'r')
    rorse -> rose (remove 'r')
    rose -> ros (remove 'e')

    Input: word1 = "intention", word2 = "execution"
    Output: 5
    Explanation: 
    intention -> inention (remove 't')
    inention -> enention (replace 'i' with 'e')
    enention -> exention (replace 'n' with 'x')
    exention -> exection (replace 'n' with 'c')
    exection -> execution (insert 'u')

CONSTRAINTS:
- 0 <= word1.length, word2.length <= 500
- word1 and word2 consist of lowercase English letters

================================================================================
"""


# ============================================================================
# SOLUTION 1: 2D DP
# ============================================================================
def minDistance(word1: str, word2: str) -> int:
    """
    dp[i][j] = edit distance of word1[0:i] and word2[0:j]
    
    If word1[i-1] == word2[j-1]: dp[i][j] = dp[i-1][j-1]
    Else: dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])
                          (replace)    (delete)   (insert)
    
    Time: O(m × n)
    Space: O(m × n)
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters from word1
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters to get word2
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # Replace
                    dp[i - 1][j],      # Delete from word1
                    dp[i][j - 1]       # Insert into word1
                )
    
    return dp[m][n]


# ============================================================================
# SOLUTION 2: Space Optimized (Two rows)
# ============================================================================
def minDistance_optimized(word1: str, word2: str) -> int:
    """
    Only need two rows.
    
    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(word1), len(word2)
    
    # Ensure word2 is shorter for space optimization
    if m < n:
        word1, word2 = word2, word1
        m, n = n, m
    
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j - 1], prev[j], curr[j - 1])
        prev, curr = curr, prev
    
    return prev[n]


# ============================================================================
# SOLUTION 3: Single Row (Most optimized)
# ============================================================================
def minDistance_1d(word1: str, word2: str) -> int:
    """
    Single row with diagonal tracking.
    
    Time: O(m × n)
    Space: O(min(m, n))
    """
    m, n = len(word1), len(word2)
    
    if m < n:
        word1, word2 = word2, word1
        m, n = n, m
    
    dp = list(range(n + 1))
    
    for i in range(1, m + 1):
        prev = dp[0]  # dp[i-1][j-1]
        dp[0] = i
        
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    
    return dp[n]


# ============================================================================
# SOLUTION 4: Top-Down with Memoization
# ============================================================================
def minDistance_memo(word1: str, word2: str) -> int:
    """
    Recursive approach with memoization.
    
    Time: O(m × n)
    Space: O(m × n)
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> int:
        if i == 0:
            return j  # Insert all remaining chars of word2
        if j == 0:
            return i  # Delete all remaining chars of word1
        
        if word1[i - 1] == word2[j - 1]:
            return dp(i - 1, j - 1)
        
        return 1 + min(
            dp(i - 1, j - 1),  # Replace
            dp(i - 1, j),      # Delete
            dp(i, j - 1)       # Insert
        )
    
    return dp(len(word1), len(word2))


# ============================================================================
# SOLUTION 5: With operation tracking
# ============================================================================
def minDistance_with_ops(word1: str, word2: str) -> tuple:
    """
    Return edit distance and list of operations.
    
    Time: O(m × n)
    Space: O(m × n)
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to find operations
    ops = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and word1[i - 1] == word2[j - 1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(f"Replace '{word1[i-1]}' with '{word2[j-1]}'")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f"Delete '{word1[i-1]}'")
            i -= 1
        else:
            ops.append(f"Insert '{word2[j-1]}'")
            j -= 1
    
    return dp[m][n], list(reversed(ops))


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    word1_1, word2_1 = "horse", "ros"
    print(f"word1 = '{word1_1}', word2 = '{word2_1}'")
    print(f"2D DP: {minDistance(word1_1, word2_1)}")
    print(f"1D DP: {minDistance_1d(word1_1, word2_1)}")
    dist, ops = minDistance_with_ops(word1_1, word2_1)
    print(f"Operations ({dist}): {ops}")
    # Expected: 3
    print()
    
    # Test Case 2: Longer strings
    word1_2, word2_2 = "intention", "execution"
    print(f"word1 = '{word1_2}', word2 = '{word2_2}'")
    print(f"Result: {minDistance(word1_2, word2_2)}")
    # Expected: 5
    print()
    
    # Test Case 3: Same strings
    word1_3, word2_3 = "abc", "abc"
    print(f"word1 = '{word1_3}', word2 = '{word2_3}'")
    print(f"Result: {minDistance(word1_3, word2_3)}")
    # Expected: 0
    print()
    
    # Test Case 4: One empty
    word1_4, word2_4 = "", "abc"
    print(f"word1 = '{word1_4}', word2 = '{word2_4}'")
    print(f"Result: {minDistance(word1_4, word2_4)}")
    # Expected: 3
    print()
    
    # Test Case 5: Completely different
    word1_5, word2_5 = "abc", "xyz"
    print(f"word1 = '{word1_5}', word2 = '{word2_5}'")
    print(f"Result: {minDistance(word1_5, word2_5)}")
    # Expected: 3


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE THREE OPERATIONS:
   
   At position (i, j), if chars don't match:
   - Replace: dp[i-1][j-1] + 1 (change word1[i-1] to word2[j-1])
   - Delete: dp[i-1][j] + 1 (delete word1[i-1])
   - Insert: dp[i][j-1] + 1 (insert word2[j-1] into word1)
   
   Take minimum of all three!

2. BASE CASES:
   
   dp[i][0] = i (delete all i chars from word1)
   dp[0][j] = j (insert all j chars to make word2)
   
   Converting to/from empty string.

3. WHEN CHARS MATCH:
   
   dp[i][j] = dp[i-1][j-1]
   
   No operation needed, just move both pointers.

4. INTUITION FOR DELETE/INSERT:
   
   Delete word1[i-1]: We've converted word1[0:i-1] to word2[0:j]
                      Now delete word1[i-1]
   
   Insert word2[j-1]: We've converted word1[0:i] to word2[0:j-1]
                      Now insert word2[j-1]

5. CONNECTION TO LCS:
   
   Edit distance = m + n - 2 × LCS
   
   Delete (m - LCS) from word1, insert (n - LCS) for word2.
   But this doesn't use replace, so actual can be smaller.

6. SPACE OPTIMIZATION:
   
   Two rows: O(n)
   Single row with diagonal: O(n)
   
   Must save dp[i-1][j-1] before overwriting!

7. COMMON VARIATIONS:
   
   - Different costs for operations
   - Only certain operations allowed
   - Levenshtein distance (same as this)

8. COMMON MISTAKES:
   
   ❌ Forgetting base cases
   ❌ Wrong operation mapping (delete vs insert)
   ❌ Not saving diagonal in space-optimized

9. RELATED PROBLEMS:
   
   - One Edit Distance (LC 161)
   - Delete Operation for Two Strings (LC 583)
   - Minimum ASCII Delete Sum (LC 712)

10. HOW TO EXPLAIN IT:
    
    "I'll use 2D DP where dp[i][j] is the edit distance of
    word1[0:i] and word2[0:j].
    
    If characters match, no operation needed: dp[i-1][j-1].
    
    Otherwise, take minimum of:
    - Replace: dp[i-1][j-1] + 1
    - Delete from word1: dp[i-1][j] + 1
    - Insert into word1: dp[i][j-1] + 1
    
    Base cases: converting to/from empty string."
    
    Walk through an example to clarify the operations!

================================================================================
"""
