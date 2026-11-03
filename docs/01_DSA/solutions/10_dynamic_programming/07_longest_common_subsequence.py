"""
================================================================================
PROBLEM: Longest Common Subsequence (LeetCode 1143)
Difficulty: Medium | Pattern: DP (2D)
================================================================================

PROBLEM STATEMENT:
Given two strings text1 and text2, return the length of their longest common 
subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string 
with some characters (can be none) deleted without changing the relative order 
of the remaining characters.

EXAMPLES:
    Input: text1 = "abcde", text2 = "ace" 
    Output: 3  
    Explanation: The longest common subsequence is "ace" and its length is 3.

    Input: text1 = "abc", text2 = "abc"
    Output: 3
    Explanation: The longest common subsequence is "abc" and its length is 3.

    Input: text1 = "abc", text2 = "def"
    Output: 0
    Explanation: There is no such common subsequence.

CONSTRAINTS:
- 1 <= text1.length, text2.length <= 1000
- text1 and text2 consist of only lowercase English characters

================================================================================
"""


# ============================================================================
# SOLUTION 1: 2D DP
# ============================================================================
def longestCommonSubsequence(text1: str, text2: str) -> int:
    """
    dp[i][j] = LCS of text1[0:i] and text2[0:j]
    
    If text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
    Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    Time: O(m × n)
    Space: O(m × n)
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


# ============================================================================
# SOLUTION 2: Space Optimized (Two rows)
# ============================================================================
def longestCommonSubsequence_optimized(text1: str, text2: str) -> int:
    """
    Only need two rows at a time.
    
    Time: O(m × n)
    Space: O(min(m, n))
    """
    if len(text1) < len(text2):
        text1, text2 = text2, text1
    
    m, n = len(text1), len(text2)
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev
    
    return prev[n]


# ============================================================================
# SOLUTION 3: Single Row (Most optimized space)
# ============================================================================
def longestCommonSubsequence_1d(text1: str, text2: str) -> int:
    """
    Single row with diagonal tracking.
    
    Time: O(m × n)
    Space: O(min(m, n))
    """
    if len(text1) < len(text2):
        text1, text2 = text2, text1
    
    n = len(text2)
    dp = [0] * (n + 1)
    
    for char1 in text1:
        prev = 0  # dp[i-1][j-1]
        for j in range(1, n + 1):
            temp = dp[j]  # Save for next iteration's diagonal
            if char1 == text2[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = temp
    
    return dp[n]


# ============================================================================
# SOLUTION 4: Top-Down with Memoization
# ============================================================================
def longestCommonSubsequence_memo(text1: str, text2: str) -> int:
    """
    Recursive approach with memoization.
    
    Time: O(m × n)
    Space: O(m × n)
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def lcs(i: int, j: int) -> int:
        if i == 0 or j == 0:
            return 0
        
        if text1[i - 1] == text2[j - 1]:
            return lcs(i - 1, j - 1) + 1
        else:
            return max(lcs(i - 1, j), lcs(i, j - 1))
    
    return lcs(len(text1), len(text2))


# ============================================================================
# SOLUTION 5: Get actual LCS string
# ============================================================================
def getLCS(text1: str, text2: str) -> tuple:
    """
    Return both length and actual LCS string.
    
    Time: O(m × n)
    Space: O(m × n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Backtrack to find actual LCS
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return dp[m][n], ''.join(reversed(lcs))


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    text1_1, text2_1 = "abcde", "ace"
    print(f"text1 = '{text1_1}', text2 = '{text2_1}'")
    print(f"2D DP: {longestCommonSubsequence(text1_1, text2_1)}")
    print(f"1D DP: {longestCommonSubsequence_1d(text1_1, text2_1)}")
    length, lcs = getLCS(text1_1, text2_1)
    print(f"LCS: '{lcs}' (length {length})")
    # Expected: 3 ("ace")
    print()
    
    # Test Case 2: Same strings
    text1_2, text2_2 = "abc", "abc"
    print(f"text1 = '{text1_2}', text2 = '{text2_2}'")
    print(f"Result: {longestCommonSubsequence(text1_2, text2_2)}")
    # Expected: 3
    print()
    
    # Test Case 3: No common
    text1_3, text2_3 = "abc", "def"
    print(f"text1 = '{text1_3}', text2 = '{text2_3}'")
    print(f"Result: {longestCommonSubsequence(text1_3, text2_3)}")
    # Expected: 0
    print()
    
    # Test Case 4: One empty
    text1_4, text2_4 = "", "abc"
    print(f"text1 = '{text1_4}', text2 = '{text2_4}'")
    print(f"Result: {longestCommonSubsequence(text1_4, text2_4)}")
    # Expected: 0
    print()
    
    # Test Case 5: Complex case
    text1_5, text2_5 = "AGGTAB", "GXTXAYB"
    print(f"text1 = '{text1_5}', text2 = '{text2_5}'")
    length, lcs = getLCS(text1_5, text2_5)
    print(f"LCS: '{lcs}' (length {length})")
    # Expected: 4 ("GTAB")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. RECURRENCE RELATION:
   
   If text1[i-1] == text2[j-1]:
       dp[i][j] = dp[i-1][j-1] + 1  (extend LCS)
   Else:
       dp[i][j] = max(dp[i-1][j], dp[i][j-1])  (skip one char)

2. INTUITION:
   
   "If characters match, they're part of LCS.
   If not, try skipping each character and take max."
   
   This explores all possible subsequences efficiently.

3. BASE CASE:
   
   dp[0][j] = 0 (empty string has LCS 0)
   dp[i][0] = 0
   
   First row and column are all 0s.

4. SPACE OPTIMIZATION:
   
   Two rows: O(min(m, n))
   Single row with diagonal tracking: O(min(m, n))
   
   Key: Save dp[i-1][j-1] before overwriting!

5. RECONSTRUCTING LCS:
   
   Backtrack from dp[m][n]:
   - If chars equal: add to result, go diagonal
   - Else: go to larger of (up, left)

6. LCS VS LIS:
   
   LCS: Two sequences, find common subsequence
   LIS: One sequence, find increasing subsequence
   
   LIS can be solved with LCS of original and sorted!

7. EDIT DISTANCE CONNECTION:
   
   Edit distance = m + n - 2 × LCS
   (Delete non-LCS chars from both, then insert)

8. COMMON MISTAKES:
   
   ❌ Confusing substring (contiguous) with subsequence
   ❌ Off-by-one with 1-indexed DP
   ❌ Not saving diagonal in space-optimized version

9. RELATED PROBLEMS:
   
   - Edit Distance (LC 72)
   - Longest Palindromic Subsequence (LC 516)
   - Shortest Common Supersequence (LC 1092)
   - Delete Operation for Two Strings (LC 583)

10. practice TIP:
    
    "I'll use 2D DP where dp[i][j] is the LCS of text1[0:i]
    and text2[0:j].
    
    If characters match, we extend the LCS: dp[i-1][j-1] + 1.
    Otherwise, we try skipping each character: max(dp[i-1][j], dp[i][j-1]).
    
    For space optimization, I only need the previous row,
    but I must save the diagonal value before overwriting."
    
    Be ready to reconstruct the actual LCS!

================================================================================
"""
