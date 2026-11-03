"""
================================================================================
PROBLEM: Longest Repeating Character Replacement (LeetCode 424)
Difficulty: Medium | Pattern: Sliding Window + Frequency Count
================================================================================

PROBLEM STATEMENT:
You are given a string s and an integer k. You can choose any character of the
string and change it to any other uppercase English character. You can perform
this operation at most k times.

Return the length of the longest substring containing the same letter you can 
get after performing the above operations.

EXAMPLES:
    Input: s = "ABAB", k = 2
    Output: 4
    Explanation: Replace the two 'A's with two 'B's or vice versa.

    Input: s = "AABABBA", k = 1
    Output: 4
    Explanation: Replace the one 'A' in the middle with 'B' → "AABBBBA".
                 The longest repeating letters is "BBBB" with length 4.
                 Or replace one B → "AAABBBA" → "AAAA" has length 4.

CONSTRAINTS:
- 1 <= s.length <= 10^5
- s consists of only uppercase English letters
- 0 <= k <= s.length

================================================================================
"""

from collections import defaultdict


# ============================================================================
# SOLUTION 1: Sliding Window (Optimal)
# ============================================================================
def characterReplacement(s: str, k: int) -> int:
    """
    Sliding window where we track the max frequency character.
    
    Key insight:
    - For a window to be valid: window_size - max_freq <= k
    - We need at most k replacements to make all chars the same
    
    Optimization: We don't shrink the window unnecessarily.
    - Even if max_count decreases, keeping larger window is fine
    - We're looking for MAXIMUM length
    
    Time: O(n)
    Space: O(26) = O(1)
    """
    count = defaultdict(int)
    max_count = 0  # Max frequency of any single character in window
    max_length = 0
    left = 0
    
    for right, char in enumerate(s):
        count[char] += 1
        max_count = max(max_count, count[char])
        
        # Window size - max freq = chars to replace
        # If > k, we need to shrink
        window_size = right - left + 1
        if window_size - max_count > k:
            # Shrink from left
            count[s[left]] -= 1
            left += 1
        
        # Update max length
        max_length = max(max_length, right - left + 1)
    
    return max_length


# ============================================================================
# SOLUTION 2: Sliding Window with strict shrinking (More intuitive)
# ============================================================================
def characterReplacement_strict(s: str, k: int) -> int:
    """
    Same approach but shrink until window is valid again.
    Slightly slower but easier to understand.
    
    Time: O(n) - each element visited at most twice
    Space: O(26) = O(1)
    """
    count = defaultdict(int)
    max_length = 0
    left = 0
    
    for right, char in enumerate(s):
        count[char] += 1
        
        # Get max frequency in current window (have to recalculate)
        max_count = max(count.values())
        
        # Shrink while invalid
        while (right - left + 1) - max_count > k:
            count[s[left]] -= 1
            left += 1
            max_count = max(count.values()) if count else 0
        
        max_length = max(max_length, right - left + 1)
    
    return max_length


# ============================================================================
# SOLUTION 3: Binary Search + Fixed Window (Alternative approach)
# ============================================================================
def characterReplacement_binary(s: str, k: int) -> int:
    """
    Binary search on the answer (window size).
    For each candidate size, check if valid window exists.
    
    Time: O(n log n)
    Space: O(26) = O(1)
    
    This is slower but shows a different thinking pattern.
    """
    def can_make_window_of_size(size):
        """Check if we can make a valid window of given size."""
        count = defaultdict(int)
        
        # Build first window
        for i in range(size):
            count[s[i]] += 1
        
        if size - max(count.values()) <= k:
            return True
        
        # Slide window
        for i in range(size, len(s)):
            count[s[i]] += 1
            count[s[i - size]] -= 1
            
            if size - max(count.values()) <= k:
                return True
        
        return False
    
    left, right = 1, len(s)
    result = 0
    
    while left <= right:
        mid = (left + right) // 2
        
        if can_make_window_of_size(mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard example
    s1, k1 = "ABAB", 2
    print(f"Input: s = '{s1}', k = {k1}")
    print(f"Output (Optimal): {characterReplacement(s1, k1)}")
    print(f"Output (Strict): {characterReplacement_strict(s1, k1)}")
    # Expected: 4
    print()
    
    # Test Case 2: Another example
    s2, k2 = "AABABBA", 1
    print(f"Input: s = '{s2}', k = {k2}")
    print(f"Output (Optimal): {characterReplacement(s2, k2)}")
    # Expected: 4
    print()
    
    # Test Case 3: All same characters
    s3, k3 = "AAAA", 2
    print(f"Input: s = '{s3}', k = {k3}")
    print(f"Output: {characterReplacement(s3, k3)}")
    # Expected: 4
    print()
    
    # Test Case 4: k = 0
    s4, k4 = "ABAB", 0
    print(f"Input: s = '{s4}', k = {k4}")
    print(f"Output: {characterReplacement(s4, k4)}")
    # Expected: 1 (can't replace anything)
    print()
    
    # Test Case 5: k >= len(s)
    s5, k5 = "ABCD", 4
    print(f"Input: s = '{s5}', k = {k5}")
    print(f"Output: {characterReplacement(s5, k5)}")
    # Expected: 4
    print()
    
    # Test Case 6: Single character
    s6, k6 = "A", 0
    print(f"Input: s = '{s6}', k = {k6}")
    print(f"Output: {characterReplacement(s6, k6)}")
    # Expected: 1


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. CORE FORMULA:
   
   For a window to be valid (can make all chars same with k replacements):
   
   window_size - max_freq <= k
   
   This means: characters to replace = total - most frequent <= k

2. THE CLEVER OPTIMIZATION (Why we don't shrink fully):
   
   When max_count decreases, we DON'T update it!
   
   Why? We're looking for MAXIMUM length.
   - If previous max_count gave us a valid window of size X
   - Any future max window must be at least size X
   - No need to shrink below X
   
   This makes the algorithm O(n) instead of O(n * 26)

3. VISUAL WALKTHROUGH for "AABABBA", k=1:
   
   A A B A B B A
   ^           ^
   
   Window [A A B A B B]: size=6, max_count=3(A or B), 6-3=3 > k=1, invalid
   
   Shrink: [A B A B B]: size=5, max_count=3(B), 5-3=2 > k=1, invalid
   
   Shrink: [B A B B]: size=4, max_count=3(B), 4-3=1 <= k=1, VALID! length=4

4. WINDOW VALIDITY CHECK:
   
   chars_to_replace = window_size - max_freq
   
   If chars_to_replace > k → Invalid, shrink
   If chars_to_replace <= k → Valid, expand

5. COMMON VARIATIONS:
   
   Q: What if we can only replace with a specific character?
   A: Track frequency of that character only
   
   Q: What if string has lowercase too?
   A: Same algorithm, just 52 possible characters
   
   Q: What if k is cost per replacement (not count)?
   A: Need to track total cost, same sliding window idea

6. WHY THIS IS TRICKY:
   
   - max_count doesn't decrease when we remove chars
   - This is an OPTIMIZATION, not a bug
   - We only care about the MAXIMUM valid window
   - If we found a valid window of size X, future answer >= X

7. COMPARISON OF APPROACHES:
   
   | Approach          | Time      | Space | Notes            |
   |-------------------|-----------|-------|------------------|
   | Optimal           | O(n)      | O(26) | Don't shrink max |
   | Strict shrinking  | O(n)      | O(26) | Recalculate max  |
   | Binary search     | O(n log n)| O(26) | Alternative idea |

8. RELATED PROBLEMS:
   - Max Consecutive Ones III (LC 1004) - binary array version
   - Longest Subarray with Ones after Deletion (LC 1493)
   - Minimum Window Substring (LC 76)

9. HOW TO EXPLAIN IT:
   
   Start with the strict shrinking approach (easier to explain).
   Then mention: "We can optimize by not updating max_count 
   when shrinking, since we only care about maximum length."

================================================================================
"""
