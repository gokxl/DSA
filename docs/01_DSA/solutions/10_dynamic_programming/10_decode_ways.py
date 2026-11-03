"""
================================================================================
PROBLEM: Decode Ways (LeetCode 91)
Difficulty: Medium | Pattern: DP (1D)
================================================================================

PROBLEM STATEMENT:
A message containing letters from A-Z can be encoded into numbers using the 
following mapping:

'A' -> "1"
'B' -> "2"
...
'Z' -> "26"

To decode an encoded message, all the digits must be grouped then mapped back 
into letters using the reverse of the mapping above (there may be multiple ways).

Given a string s containing only digits, return the number of ways to decode it.

EXAMPLES:
    Input: s = "12"
    Output: 2
    Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).

    Input: s = "226"
    Output: 3
    Explanation: "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).

    Input: s = "06"
    Output: 0
    Explanation: "06" cannot be mapped to "F" because "6" != "06" (leading zero).

CONSTRAINTS:
- 1 <= s.length <= 100
- s contains only digits and may contain leading zero(s)

================================================================================
"""


# ============================================================================
# SOLUTION 1: Bottom-Up DP
# ============================================================================
def numDecodings(s: str) -> int:
    """
    dp[i] = number of ways to decode s[0:i]
    
    At position i:
    - Single digit (s[i-1]): valid if 1-9
    - Two digits (s[i-2:i]): valid if 10-26
    
    Time: O(n)
    Space: O(n)
    """
    if not s or s[0] == '0':
        return 0
    
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1  # Empty string
    dp[1] = 1  # First char (already checked not '0')
    
    for i in range(2, n + 1):
        # Single digit decode
        if s[i - 1] != '0':
            dp[i] += dp[i - 1]
        
        # Two digit decode
        two_digit = int(s[i - 2:i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i - 2]
    
    return dp[n]


# ============================================================================
# SOLUTION 2: Space Optimized
# ============================================================================
def numDecodings_optimized(s: str) -> int:
    """
    Only need last two values.
    
    Time: O(n)
    Space: O(1)
    """
    if not s or s[0] == '0':
        return 0
    
    # prev2 = dp[i-2], prev1 = dp[i-1]
    prev2, prev1 = 1, 1
    
    for i in range(1, len(s)):
        current = 0
        
        # Single digit
        if s[i] != '0':
            current += prev1
        
        # Two digits
        two_digit = int(s[i - 1:i + 1])
        if 10 <= two_digit <= 26:
            current += prev2
        
        prev2, prev1 = prev1, current
    
    return prev1


# ============================================================================
# SOLUTION 3: Top-Down with Memoization
# ============================================================================
def numDecodings_memo(s: str) -> int:
    """
    Recursive with memoization.
    
    Time: O(n)
    Space: O(n)
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def decode(i: int) -> int:
        # Reached end - valid decoding
        if i == len(s):
            return 1
        
        # Leading zero - invalid
        if s[i] == '0':
            return 0
        
        # Single digit
        ways = decode(i + 1)
        
        # Two digits
        if i + 1 < len(s) and int(s[i:i + 2]) <= 26:
            ways += decode(i + 2)
        
        return ways
    
    return decode(0)


# ============================================================================
# SOLUTION 4: Cleaner validation
# ============================================================================
def numDecodings_clean(s: str) -> int:
    """
    Cleaner version with explicit validation functions.
    
    Time: O(n)
    Space: O(1)
    """
    def valid_single(c: str) -> bool:
        return c != '0'
    
    def valid_double(s: str) -> bool:
        return s[0] != '0' and 1 <= int(s) <= 26
    
    if not s:
        return 0
    
    prev2, prev1 = 1, 1 if valid_single(s[0]) else 0
    
    for i in range(1, len(s)):
        current = 0
        
        if valid_single(s[i]):
            current += prev1
        
        if valid_double(s[i - 1:i + 1]):
            current += prev2
        
        prev2, prev1 = prev1, current
    
    return prev1


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Two ways
    s1 = "12"
    print(f"s = '{s1}'")
    print(f"DP: {numDecodings(s1)}")
    print(f"Optimized: {numDecodings_optimized(s1)}")
    # Expected: 2 ("AB" or "L")
    print()
    
    # Test Case 2: Three ways
    s2 = "226"
    print(f"s = '{s2}'")
    print(f"Result: {numDecodings(s2)}")
    # Expected: 3 ("BZ", "VF", "BBF")
    print()
    
    # Test Case 3: Leading zero
    s3 = "06"
    print(f"s = '{s3}'")
    print(f"Result: {numDecodings(s3)}")
    # Expected: 0
    print()
    
    # Test Case 4: Contains zero
    s4 = "10"
    print(f"s = '{s4}'")
    print(f"Result: {numDecodings(s4)}")
    # Expected: 1 ("J")
    print()
    
    # Test Case 5: All ones
    s5 = "111"
    print(f"s = '{s5}'")
    print(f"Result: {numDecodings_memo(s5)}")
    # Expected: 3 ("AAA", "KA", "AK")
    print()
    
    # Test Case 6: Zero in middle
    s6 = "2101"
    print(f"s = '{s6}'")
    print(f"Result: {numDecodings(s6)}")
    # Expected: 1 (2-10-1 = B-J-A; "01" is invalid, so 10 must pair)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. RECURRENCE:
   
   dp[i] = (dp[i-1] if single valid) + (dp[i-2] if double valid)
   
   At each position, we can take 1 or 2 digits.

2. VALID CONDITIONS:
   
   Single digit: s[i] != '0' (1-9 are valid)
   Two digits: 10 <= int(s[i-1:i+1]) <= 26
   
   Note: "01" through "09" are INVALID (leading zero)

3. HANDLING ZEROS:
   
   - "0" alone is invalid
   - "10", "20" are valid (J, T)
   - "30"-"90" are invalid
   - Leading "0" means 0 ways
   
   Zero forces the previous digit to form pair!

4. BASE CASES:
   
   dp[0] = 1 (empty string = 1 way)
   dp[1] = 1 if s[0] != '0' else 0

5. SIMILAR TO CLIMBING STAIRS:
   
   Like climbing stairs with 1 or 2 steps,
   but with validity constraints!
   
   Same recurrence: dp[i] = dp[i-1] + dp[i-2]
   With conditions on when each term applies.

6. SPACE OPTIMIZATION:
   
   Only need dp[i-1] and dp[i-2], so use two variables.

7. EDGE CASES:
   
   - Empty string: return 0
   - Leading zero: return 0
   - All zeros: return 0
   - "27" through "99": only single digit valid

8. COMMON MISTAKES:
   
   ❌ Not handling leading zeros
   ❌ Treating "01" as valid (it's not!)
   ❌ Off-by-one in substring slicing

9. DECODE WAYS II (LC 639):
   
   String can contain '*' which matches 1-9.
   Much more complex - need to count all possibilities.

10. HOW TO EXPLAIN IT:
    
    "This is like Climbing Stairs but with validity constraints.
    At each position, I can decode 1 or 2 digits if valid.
    
    Single digit valid: '1'-'9' (not '0')
    Two digits valid: '10'-'26' (not '01'-'09')
    
    dp[i] = dp[i-1] (if single valid) + dp[i-2] (if double valid)
    
    Key insight: zeros can only be decoded with previous digit."
    
    Walk through "2026" to show zero handling!

================================================================================
"""
