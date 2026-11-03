"""
================================================================================
PROBLEM: Find All Anagrams in a String (LeetCode 438)
Difficulty: Medium | Pattern: Sliding Window + Frequency Count
================================================================================

PROBLEM STATEMENT:
Given two strings s and p, return an array of all the start indices of p's 
anagrams in s. You may return the answer in any order.

An Anagram is a word formed by rearranging the letters of another word,
using all the original letters exactly once.

EXAMPLES:
    Input: s = "cbaebabacd", p = "abc"
    Output: [0, 6]
    Explanation:
        - At index 0: "cba" is anagram of "abc"
        - At index 6: "bac" is anagram of "abc"

    Input: s = "abab", p = "ab"
    Output: [0, 1, 2]
    Explanation:
        - At index 0: "ab" is anagram
        - At index 1: "ba" is anagram
        - At index 2: "ab" is anagram

CONSTRAINTS:
- 1 <= s.length, p.length <= 3 * 10^4
- s and p consist of lowercase English letters

================================================================================
"""

from typing import List
from collections import Counter


# ============================================================================
# SOLUTION 1: Sliding Window with Counter Comparison (Simple)
# ============================================================================
def findAnagrams_simple(s: str, p: str) -> List[int]:
    """
    Fixed-size sliding window of length len(p).
    Compare frequency counts at each position.
    
    Time: O(n * 26) = O(n) where n = len(s)
    Space: O(26) = O(1) for frequency arrays
    """
    if len(p) > len(s):
        return []
    
    result = []
    p_count = Counter(p)
    window_count = Counter(s[:len(p)])
    
    # Check first window
    if window_count == p_count:
        result.append(0)
    
    # Slide the window
    for i in range(len(p), len(s)):
        # Add new character
        window_count[s[i]] += 1
        
        # Remove old character (left of window)
        old_char = s[i - len(p)]
        window_count[old_char] -= 1
        if window_count[old_char] == 0:
            del window_count[old_char]
        
        # Check if anagram
        if window_count == p_count:
            result.append(i - len(p) + 1)
    
    return result


# ============================================================================
# SOLUTION 2: Sliding Window with Match Counter (Optimal)
# ============================================================================
def findAnagrams(s: str, p: str) -> List[int]:
    """
    Optimization: Instead of comparing full counters, track number of matched chars.
    
    Key insight:
    - Track how many characters have the correct frequency
    - When all 'unique chars in p' match → found anagram
    
    Time: O(n) - true single pass
    Space: O(26) = O(1)
    """
    if len(p) > len(s):
        return []
    
    result = []
    p_count = Counter(p)
    window_count = {}
    
    required = len(p_count)  # Number of unique chars needed to match
    formed = 0  # Number of unique chars currently matching
    
    left = 0
    
    for right, char in enumerate(s):
        # Add character to window
        window_count[char] = window_count.get(char, 0) + 1
        
        # Check if this char's frequency now matches p's
        if char in p_count and window_count[char] == p_count[char]:
            formed += 1
        
        # If window is larger than p, shrink from left
        if right - left + 1 > len(p):
            left_char = s[left]
            
            # Check if removing will break a match
            if left_char in p_count and window_count[left_char] == p_count[left_char]:
                formed -= 1
            
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]
            
            left += 1
        
        # Check if all required chars match
        if formed == required:
            result.append(left)
    
    return result


# ============================================================================
# SOLUTION 3: Using Array for Counts (Most Efficient)
# ============================================================================
def findAnagrams_array(s: str, p: str) -> List[int]:
    """
    Use array instead of hashmap for slightly better performance.
    Track difference between window and target.
    
    Time: O(n)
    Space: O(26) = O(1)
    """
    if len(p) > len(s):
        return []
    
    result = []
    
    # diff[i] = count in window - count in p
    # When all diff[i] == 0, we have an anagram
    diff = [0] * 26
    
    # Initialize difference for pattern
    for char in p:
        diff[ord(char) - ord('a')] -= 1
    
    # Build first window
    for i in range(len(p)):
        diff[ord(s[i]) - ord('a')] += 1
    
    # Count how many characters have diff != 0
    def count_non_zero():
        return sum(1 for d in diff if d != 0)
    
    non_zero = count_non_zero()
    if non_zero == 0:
        result.append(0)
    
    # Slide window
    for i in range(len(p), len(s)):
        # Add new character
        idx_new = ord(s[i]) - ord('a')
        if diff[idx_new] == 0:
            non_zero += 1
        diff[idx_new] += 1
        if diff[idx_new] == 0:
            non_zero -= 1
        
        # Remove old character
        idx_old = ord(s[i - len(p)]) - ord('a')
        if diff[idx_old] == 0:
            non_zero += 1
        diff[idx_old] -= 1
        if diff[idx_old] == 0:
            non_zero -= 1
        
        # Check for anagram
        if non_zero == 0:
            result.append(i - len(p) + 1)
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard example
    s1, p1 = "cbaebabacd", "abc"
    print(f"Input: s = '{s1}', p = '{p1}'")
    print(f"Output (Simple): {findAnagrams_simple(s1, p1)}")
    print(f"Output (Match): {findAnagrams(s1, p1)}")
    print(f"Output (Array): {findAnagrams_array(s1, p1)}")
    # Expected: [0, 6]
    print()
    
    # Test Case 2: Multiple overlapping anagrams
    s2, p2 = "abab", "ab"
    print(f"Input: s = '{s2}', p = '{p2}'")
    print(f"Output: {findAnagrams(s2, p2)}")
    # Expected: [0, 1, 2]
    print()
    
    # Test Case 3: No anagram
    s3, p3 = "hello", "xyz"
    print(f"Input: s = '{s3}', p = '{p3}'")
    print(f"Output: {findAnagrams(s3, p3)}")
    # Expected: []
    print()
    
    # Test Case 4: Exact match
    s4, p4 = "abc", "cba"
    print(f"Input: s = '{s4}', p = '{p4}'")
    print(f"Output: {findAnagrams(s4, p4)}")
    # Expected: [0]
    print()
    
    # Test Case 5: Pattern longer than string
    s5, p5 = "ab", "abc"
    print(f"Input: s = '{s5}', p = '{p5}'")
    print(f"Output: {findAnagrams(s5, p5)}")
    # Expected: []
    print()
    
    # Test Case 6: All same characters
    s6, p6 = "aaaa", "aa"
    print(f"Input: s = '{s6}', p = '{p6}'")
    print(f"Output: {findAnagrams(s6, p6)}")
    # Expected: [0, 1, 2]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. PATTERN RECOGNITION:
   
   "Find all substrings that are anagrams" = Fixed-size Sliding Window
   
   Window size = len(p) (never changes)
   
   Key insight: Anagram = same character frequencies

2. THREE APPROACHES:
   
   a) Compare full counters each time - O(26) per comparison
   b) Track "formed" matches - only update when frequencies match/unmatch
   c) Track non-zero differences - minimize operations

3. THE "FORMED" COUNTER TRICK:
   
   Instead of comparing entire counter objects:
   - Track how many unique characters have matching frequency
   - When formed == required → anagram found
   
   This makes checking O(1) instead of O(26)

4. VISUAL WALKTHROUGH for s="cbaebabacd", p="abc":
   
   p_count = {a:1, b:1, c:1}, required = 3
   
   Window positions:
   [c b a] e b a b a c d    formed=3 ✓ → index 0
    [b a e] b a b a c d     formed=2 (no 'c')
     [a e b] a b a c d      formed=2 (no 'c')
      [e b a] b a c d       formed=2 (extra 'e')
       [b a b] a c d        formed=2 (extra 'b')
        [a b a] c d         formed=2 (extra 'a')
         [b a c] d          formed=3 ✓ → index 6
          [a c d]           formed=2 (no 'b')

5. FIXED vs VARIABLE SLIDING WINDOW:
   
   Fixed-size (this problem):
   - Window size is constant
   - Always shrink when window > size
   
   Variable-size (Minimum Window Substring):
   - Shrink when valid, expand when invalid
   - Looking for minimum/maximum valid window

6. COMMON practice VARIATIONS:
   
   Q: What if the string contains uppercase letters?
   A: Normalize to lowercase: s.lower()
   
   Q: What if we need to return the actual anagrams, not indices?
   A: Return s[i:i+len(p)] for each index i
   
   Q: What if pattern has spaces/special chars?
   A: Include them in the count or filter them out

7. RELATED PROBLEMS:
   - Permutation in String (LC 567) - return True/False
   - Minimum Window Substring (LC 76) - variable size, harder
   - Group Anagrams (LC 49) - grouping, not sliding window

8. TEMPLATE FOR FIXED-SIZE SLIDING WINDOW:

   def fixed_sliding_window(s, k):
       # Build first window of size k
       window = build_window(s[:k])
       
       results = []
       if is_valid(window):
           results.append(0)
       
       # Slide window
       for i in range(k, len(s)):
           add_to_window(s[i])
           remove_from_window(s[i - k])
           
           if is_valid(window):
               results.append(i - k + 1)
       
       return results

================================================================================
"""
