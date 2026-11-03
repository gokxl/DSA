"""
================================================================================
PROBLEM: Minimum Window Substring (LeetCode 76)
Difficulty: Hard | Pattern: Sliding Window + Frequency Count
================================================================================

PROBLEM STATEMENT:
Given two strings s and t of lengths m and n respectively, return the minimum 
window substring of s such that every character in t (including duplicates) 
is included in the window. If there is no such substring, return "".

The testcases will be generated such that the answer is unique.

EXAMPLES:
    Input: s = "ADOBECODEBANC", t = "ABC"
    Output: "BANC"
    Explanation: "BANC" is the minimum window substring that contains 
                 'A', 'B', and 'C' from string t.

    Input: s = "a", t = "a"
    Output: "a"
    Explanation: The entire string s is the minimum window.

    Input: s = "a", t = "aa"
    Output: ""
    Explanation: Both 'a's from t must be included, but s only has one 'a'.

CONSTRAINTS:
- m == s.length
- n == t.length
- 1 <= m, n <= 10^5
- s and t consist of uppercase and lowercase English letters

================================================================================
"""

from collections import Counter


# ============================================================================
# SOLUTION 1: Sliding Window with Formed Counter (Optimal)
# ============================================================================
def minWindow(s: str, t: str) -> str:
    """
    Variable-size sliding window:
    - Expand when window doesn't contain all of t
    - Shrink when window is valid to find minimum
    
    Key insight: Track how many unique chars have required frequency.
    
    Time: O(m + n) where m = len(s), n = len(t)
    Space: O(n) for t's frequency map + O(m) for window
    """
    if not s or not t or len(s) < len(t):
        return ""
    
    # Frequency map for t
    t_count = Counter(t)
    required = len(t_count)  # Number of unique chars in t
    
    # Sliding window variables
    window_count = {}
    formed = 0  # Number of unique chars in window with required frequency
    
    # Result tracking
    min_len = float('inf')
    result_left = 0
    
    left = 0
    
    for right, char in enumerate(s):
        # Add character to window
        window_count[char] = window_count.get(char, 0) + 1
        
        # Check if this char's frequency now satisfies t's requirement
        if char in t_count and window_count[char] == t_count[char]:
            formed += 1
        
        # Try to shrink window while it's valid
        while formed == required:
            # Update result if this window is smaller
            window_size = right - left + 1
            if window_size < min_len:
                min_len = window_size
                result_left = left
            
            # Remove left character
            left_char = s[left]
            
            # Check if removing will break a match
            if left_char in t_count and window_count[left_char] == t_count[left_char]:
                formed -= 1
            
            window_count[left_char] -= 1
            left += 1
    
    return "" if min_len == float('inf') else s[result_left:result_left + min_len]


# ============================================================================
# SOLUTION 2: Sliding Window with Total Count (Alternative)
# ============================================================================
def minWindow_count(s: str, t: str) -> str:
    """
    Instead of tracking 'formed', track total characters satisfied.
    
    Time: O(m + n)
    Space: O(n + m)
    """
    if not s or not t or len(s) < len(t):
        return ""
    
    t_count = Counter(t)
    required_total = len(t)  # Total chars needed (with duplicates)
    
    window_count = {}
    have = 0  # Characters we have that are needed
    
    min_len = float('inf')
    result = ""
    
    left = 0
    
    for right, char in enumerate(s):
        # Add to window
        window_count[char] = window_count.get(char, 0) + 1
        
        # If this char is needed and we don't have excess
        if char in t_count and window_count[char] <= t_count[char]:
            have += 1
        
        # Shrink while valid
        while have == required_total:
            # Update result
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right + 1]
            
            # Remove left char
            left_char = s[left]
            if left_char in t_count and window_count[left_char] <= t_count[left_char]:
                have -= 1
            
            window_count[left_char] -= 1
            left += 1
    
    return result


# ============================================================================
# SOLUTION 3: Optimized with Filtered String (For sparse t)
# ============================================================================
def minWindow_filtered(s: str, t: str) -> str:
    """
    Optimization when t is much smaller than s and s has many irrelevant chars.
    
    Filter s to only include chars from t, then apply sliding window.
    
    Time: O(m + n) but with smaller constant
    Space: O(m + n)
    """
    if not s or not t or len(s) < len(t):
        return ""
    
    t_count = Counter(t)
    required = len(t_count)
    
    # Filter s: only keep (index, char) where char is in t
    filtered = [(i, char) for i, char in enumerate(s) if char in t_count]
    
    if not filtered:
        return ""
    
    window_count = {}
    formed = 0
    
    min_len = float('inf')
    result_left = 0
    
    left = 0  # Index in filtered array
    
    for right in range(len(filtered)):
        char = filtered[right][1]
        window_count[char] = window_count.get(char, 0) + 1
        
        if window_count[char] == t_count[char]:
            formed += 1
        
        while formed == required:
            # Calculate actual window size in s
            start = filtered[left][0]
            end = filtered[right][0]
            
            if end - start + 1 < min_len:
                min_len = end - start + 1
                result_left = start
            
            # Shrink
            left_char = filtered[left][1]
            if window_count[left_char] == t_count[left_char]:
                formed -= 1
            window_count[left_char] -= 1
            left += 1
    
    return "" if min_len == float('inf') else s[result_left:result_left + min_len]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard example
    s1, t1 = "ADOBECODEBANC", "ABC"
    print(f"Input: s = '{s1}', t = '{t1}'")
    print(f"Output (Formed): {minWindow(s1, t1)}")
    print(f"Output (Count): {minWindow_count(s1, t1)}")
    print(f"Output (Filtered): {minWindow_filtered(s1, t1)}")
    # Expected: "BANC"
    print()
    
    # Test Case 2: Exact match
    s2, t2 = "a", "a"
    print(f"Input: s = '{s2}', t = '{t2}'")
    print(f"Output: {minWindow(s2, t2)}")
    # Expected: "a"
    print()
    
    # Test Case 3: Impossible
    s3, t3 = "a", "aa"
    print(f"Input: s = '{s3}', t = '{t3}'")
    print(f"Output: '{minWindow(s3, t3)}'")
    # Expected: ""
    print()
    
    # Test Case 4: Multiple valid windows
    s4, t4 = "cabwefgewcwaefgcf", "cae"
    print(f"Input: s = '{s4}', t = '{t4}'")
    print(f"Output: {minWindow(s4, t4)}")
    # Expected: "cwae" or "aefgc" depending on order found
    print()
    
    # Test Case 5: t has duplicate chars
    s5, t5 = "aaab", "aab"
    print(f"Input: s = '{s5}', t = '{t5}'")
    print(f"Output: {minWindow(s5, t5)}")
    # Expected: "aab"
    print()
    
    # Test Case 6: Window is entire string
    s6, t6 = "abc", "abc"
    print(f"Input: s = '{s6}', t = '{t6}'")
    print(f"Output: {minWindow(s6, t6)}")
    # Expected: "abc"


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THIS IS THE HARDEST SLIDING WINDOW PROBLEM:
   
   Variable-size window with:
   - Expand when invalid
   - Shrink when valid (to find minimum)
   
   Opposite of "longest" problems where you shrink when invalid!

2. THE "FORMED" COUNTER TRICK:
   
   Instead of comparing full frequency maps each time:
   - Track how many unique chars have sufficient frequency
   - When formed == required → window is valid
   - O(1) validity check instead of O(26)

3. VARIABLE-SIZE WINDOW TEMPLATE:

   left = 0
   for right in range(len(s)):
       # 1. Add s[right] to window
       
       # 2. While window is valid:
       #    - Update result (if better)
       #    - Shrink from left
       
   return result

4. VISUAL WALKTHROUGH for s="ADOBECODEBANC", t="ABC":
   
   t_count = {A:1, B:1, C:1}, required=3
   
   Expand until valid:
   [A D O B E C] → formed=3 ✓ → len=6, min=6
   
   Shrink while valid:
   [D O B E C] → formed=2 ✗ → stop shrinking
   
   Expand again:
   [D O B E C O D E B A N C] → formed=3 ✓ → len=12, skip
   
   Shrink:
   ... eventually find [B A N C] → len=4, min=4 ✓

5. KEY DETAILS:
   
   a) When to update 'formed':
      - Increment: when window_count[char] REACHES t_count[char]
      - Decrement: when window_count[char] GOES BELOW t_count[char]
   
   b) Handle duplicates in t:
      - "aa" in t means we need TWO 'a's in window
      - formed only increments when we have ENOUGH

6. FILTERED OPTIMIZATION:
   
   When len(t) << len(s) and s has many irrelevant chars:
   - Create filtered list: [(idx, char) for relevant chars]
   - Slide window over filtered list
   - Calculate actual indices from filtered positions

7. COMMON MISTAKES:
   - Forgetting to handle duplicates in t
   - Off-by-one in window size calculation
   - Not updating result before shrinking
   - Updating formed incorrectly (==, not >= or <=)

8. COMPLEXITY ANALYSIS:
   
   Time: O(|s| + |t|)
   - Each character in s visited at most twice (add and remove)
   - O(|t|) to build t_count
   
   Space: O(|s| + |t|)
   - O(|t|) for t_count
   - O(|s|) for window_count in worst case

9. RELATED PROBLEMS:
   - Longest Substring Without Repeating (LC 3) - max, no freq
   - Longest Substring with At Most K Distinct (LC 340) - max, limited
   - Find All Anagrams (LC 438) - fixed size, same freq
   - Permutation in String (LC 567) - fixed size, same freq

10. HOW TO EXPLAIN IT:
    
    This problem has multiple edge cases. Walk through your solution 
    with these test cases:
    - t has duplicates: s="aaab", t="aab"
    - No valid window: s="a", t="aa"
    - Entire string is answer: s="abc", t="cba"

================================================================================
"""
