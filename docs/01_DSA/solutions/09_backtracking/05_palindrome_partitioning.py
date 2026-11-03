"""
================================================================================
PROBLEM: Palindrome Partitioning (LeetCode 131)
Difficulty: Medium | Pattern: Backtracking
================================================================================

PROBLEM STATEMENT:
Given a string s, partition s such that every substring of the partition is a 
palindrome. Return all possible palindrome partitioning of s.

EXAMPLES:
    Input: s = "aab"
    Output: [["a","a","b"],["aa","b"]]
    Explanation:
    "a" | "a" | "b" - all palindromes
    "aa" | "b" - both palindromes

    Input: s = "a"
    Output: [["a"]]

CONSTRAINTS:
- 1 <= s.length <= 16
- s contains only lowercase English letters

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Backtracking with Palindrome Check
# ============================================================================
def partition(s: str) -> List[List[str]]:
    """
    Backtracking: try each prefix, if palindrome, recurse on suffix.
    
    Time: O(n × 2^n) - 2^n partitions, O(n) to check each palindrome
    Space: O(n) for recursion and current partition
    """
    result = []
    
    def is_palindrome(string: str) -> bool:
        return string == string[::-1]
    
    def backtrack(start: int, current: List[str]) -> None:
        if start == len(s):
            result.append(current[:])
            return
        
        for end in range(start + 1, len(s) + 1):
            prefix = s[start:end]
            if is_palindrome(prefix):
                current.append(prefix)
                backtrack(end, current)
                current.pop()
    
    backtrack(0, [])
    return result


# ============================================================================
# SOLUTION 2: DP Precompute + Backtracking
# ============================================================================
def partition_dp(s: str) -> List[List[str]]:
    """
    Precompute all palindrome substrings using DP.
    Then backtrack using the precomputed table.
    
    Time: O(n^2) for DP + O(2^n) for backtracking
    Space: O(n^2) for DP table
    """
    n = len(s)
    
    # dp[i][j] = True if s[i:j+1] is palindrome
    dp = [[False] * n for _ in range(n)]
    
    # Single characters are palindromes
    for i in range(n):
        dp[i][i] = True
    
    # Check substrings of length 2 to n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 2:
                dp[i][j] = (s[i] == s[j])
            else:
                dp[i][j] = (s[i] == s[j] and dp[i + 1][j - 1])
    
    result = []
    
    def backtrack(start: int, current: List[str]) -> None:
        if start == n:
            result.append(current[:])
            return
        
        for end in range(start, n):
            if dp[start][end]:  # O(1) palindrome check
                current.append(s[start:end + 1])
                backtrack(end + 1, current)
                current.pop()
    
    backtrack(0, [])
    return result


# ============================================================================
# SOLUTION 3: Two Pointer Palindrome Check
# ============================================================================
def partition_two_pointer(s: str) -> List[List[str]]:
    """
    Use two-pointer technique for palindrome check.
    
    Time: O(n × 2^n)
    Space: O(n)
    """
    result = []
    
    def is_palindrome(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True
    
    def backtrack(start: int, current: List[str]) -> None:
        if start == len(s):
            result.append(current[:])
            return
        
        for end in range(start, len(s)):
            if is_palindrome(start, end):
                current.append(s[start:end + 1])
                backtrack(end + 1, current)
                current.pop()
    
    backtrack(0, [])
    return result


# ============================================================================
# SOLUTION 4: Memoized Palindrome Check
# ============================================================================
def partition_memo(s: str) -> List[List[str]]:
    """
    Memoize palindrome checks on the fly.
    
    Time: O(n × 2^n)
    Space: O(n^2) for memoization
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def is_palindrome(i: int, j: int) -> bool:
        if i >= j:
            return True
        if s[i] != s[j]:
            return False
        return is_palindrome(i + 1, j - 1)
    
    result = []
    
    def backtrack(start: int, current: tuple) -> None:
        if start == len(s):
            result.append(list(current))
            return
        
        for end in range(start, len(s)):
            if is_palindrome(start, end):
                backtrack(end + 1, current + (s[start:end + 1],))
    
    backtrack(0, ())
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    s1 = "aab"
    print(f"s = '{s1}'")
    print(f"Backtrack: {partition(s1)}")
    print(f"DP: {partition_dp(s1)}")
    # Expected: [["a","a","b"], ["aa","b"]]
    print()
    
    # Test Case 2: Single character
    s2 = "a"
    print(f"s = '{s2}'")
    print(f"Result: {partition(s2)}")
    # Expected: [["a"]]
    print()
    
    # Test Case 3: All same characters
    s3 = "aaa"
    print(f"s = '{s3}'")
    print(f"Result: {partition(s3)}")
    # Expected: [["a","a","a"], ["a","aa"], ["aa","a"], ["aaa"]]
    print()
    
    # Test Case 4: No multi-char palindromes
    s4 = "abc"
    print(f"s = '{s4}'")
    print(f"Result: {partition(s4)}")
    # Expected: [["a","b","c"]]
    print()
    
    # Test Case 5: Longer palindrome
    s5 = "aba"
    print(f"s = '{s5}'")
    print(f"Result: {partition_two_pointer(s5)}")
    # Expected: [["a","b","a"], ["aba"]]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. PROBLEM STRUCTURE:
   
   At each position, try all possible first palindrome substrings.
   If s[start:end] is palindrome, recurse on s[end:].
   
   This is a classic partition backtracking pattern.

2. BACKTRACKING TEMPLATE:
   
   def backtrack(start, current):
       if start == len(s):
           result.append(current[:])
           return
       
       for end in range(start+1, len(s)+1):
           if is_palindrome(s[start:end]):
               current.append(s[start:end])
               backtrack(end, current)
               current.pop()

3. PALINDROME CHECK OPTIONS:
   
   a) Slice and reverse: s[i:j] == s[i:j][::-1]
      - O(n) per check
   
   b) Two pointers:
      - O(n) per check, no extra space
   
   c) DP precompute:
      - O(n²) once, then O(1) per check
   
   d) Memoization:
      - O(1) after first check of each pair

4. DP PRECOMPUTATION:
   
   dp[i][j] = True if s[i:j+1] is palindrome
   
   Base: dp[i][i] = True (single char)
   Transition: dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]
   
   Build from small substrings to large.

5. TIME COMPLEXITY:
   
   Number of partitions: O(2^n) in worst case
   (Think: cut or not cut after each character)
   
   Each partition takes O(n) to build/copy.
   Total: O(n × 2^n)

6. SPACE COMPLEXITY:
   
   Without DP: O(n) for recursion
   With DP: O(n²) for table

7. COMMON MISTAKES:
   
   ❌ Off-by-one in substring indices
   ❌ Not copying current partition before adding to result
   ❌ Inefficient palindrome checks in inner loop

8. FOLLOW-UP: MIN CUTS (LC 132):
   
   Find minimum cuts to partition into palindromes.
   Solution: DP - dp[i] = min cuts for s[0:i]

9. RELATED PROBLEMS:
   
   - Palindrome Partitioning II (LC 132) - min cuts
   - Word Break (LC 139)
   - Longest Palindromic Substring (LC 5)

10. HOW TO EXPLAIN IT:
    
    "I'll use backtracking: at each position, I try each
    possible palindrome prefix and recurse on the suffix.
    
    For the palindrome check, I have two options:
    1. Simple: O(n) per check
    2. DP precompute: O(n²) upfront, then O(1) per check
    
    The DP approach is better when the string has many
    palindromic substrings."
    
    Mention both approaches - shows depth of knowledge!

================================================================================
"""
