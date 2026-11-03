"""
================================================================================
PROBLEM: Permutation in String (LeetCode 567)
Difficulty: Medium | Pattern: Sliding Window + Frequency Count
================================================================================

PROBLEM STATEMENT:
Given two strings s1 and s2, return true if s2 contains a permutation of s1,
or false otherwise.

In other words, return true if one of s1's permutations is a substring of s2.

EXAMPLES:
    Input: s1 = "ab", s2 = "eidbaooo"
    Output: true
    Explanation: s2 contains "ba" which is a permutation of "ab".

    Input: s1 = "ab", s2 = "eidboaoo"
    Output: false
    Explanation: s2 doesn't contain any permutation of "ab".

CONSTRAINTS:
- 1 <= s1.length, s2.length <= 10^4
- s1 and s2 consist of lowercase English letters

================================================================================
"""

from collections import Counter


# ============================================================================
# SOLUTION 1: Sliding Window with Counter (Simple)
# ============================================================================
def checkInclusion_simple(s1: str, s2: str) -> bool:
    """
    Fixed-size sliding window of length len(s1).
    Check if window frequency matches s1 frequency.
    
    Time: O(n) where n = len(s2)
    Space: O(26) = O(1)
    """
    if len(s1) > len(s2):
        return False
    
    s1_count = Counter(s1)
    window_count = Counter(s2[:len(s1)])
    
    if window_count == s1_count:
        return True
    
    # Slide the window
    for i in range(len(s1), len(s2)):
        # Add new character
        window_count[s2[i]] += 1
        
        # Remove old character
        old_char = s2[i - len(s1)]
        window_count[old_char] -= 1
        if window_count[old_char] == 0:
            del window_count[old_char]
        
        if window_count == s1_count:
            return True
    
    return False


# ============================================================================
# SOLUTION 2: Sliding Window with Match Counter (Optimal)
# ============================================================================
def checkInclusion(s1: str, s2: str) -> bool:
    """
    Track number of characters with matching frequency.
    When all unique chars in s1 match → permutation found.
    
    Time: O(n)
    Space: O(26) = O(1)
    """
    if len(s1) > len(s2):
        return False
    
    s1_count = Counter(s1)
    required = len(s1_count)  # Unique chars to match
    
    window_count = {}
    formed = 0  # Chars with matching frequency
    
    left = 0
    
    for right, char in enumerate(s2):
        # Add to window
        window_count[char] = window_count.get(char, 0) + 1
        
        # Check if this char now matches
        if char in s1_count and window_count[char] == s1_count[char]:
            formed += 1
        
        # Window too large - shrink
        if right - left + 1 > len(s1):
            left_char = s2[left]
            
            # Check if removing breaks a match
            if left_char in s1_count and window_count[left_char] == s1_count[left_char]:
                formed -= 1
            
            window_count[left_char] -= 1
            if window_count[left_char] == 0:
                del window_count[left_char]
            
            left += 1
        
        # Check for match
        if formed == required:
            return True
    
    return False


# ============================================================================
# SOLUTION 3: Array-based counting
# ============================================================================
def checkInclusion_array(s1: str, s2: str) -> bool:
    """
    Use array for counting, track matches.
    
    Time: O(n)
    Space: O(26) = O(1)
    """
    if len(s1) > len(s2):
        return False
    
    # Frequency difference: window - s1
    diff = [0] * 26
    
    # Initialize s1 frequencies (negative)
    for char in s1:
        diff[ord(char) - ord('a')] -= 1
    
    # Add first window
    for i in range(len(s1)):
        diff[ord(s2[i]) - ord('a')] += 1
    
    # Count non-zero entries
    matches = sum(1 for d in diff if d == 0)
    
    if matches == 26:
        return True
    
    # Slide window
    for i in range(len(s1), len(s2)):
        # Add new char
        idx = ord(s2[i]) - ord('a')
        if diff[idx] == 0:
            matches -= 1
        diff[idx] += 1
        if diff[idx] == 0:
            matches += 1
        
        # Remove old char
        idx = ord(s2[i - len(s1)]) - ord('a')
        if diff[idx] == 0:
            matches -= 1
        diff[idx] -= 1
        if diff[idx] == 0:
            matches += 1
        
        if matches == 26:
            return True
    
    return False


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Permutation exists
    s1_1, s2_1 = "ab", "eidbaooo"
    print(f"Input: s1 = '{s1_1}', s2 = '{s2_1}'")
    print(f"Output (Simple): {checkInclusion_simple(s1_1, s2_1)}")
    print(f"Output (Match): {checkInclusion(s1_1, s2_1)}")
    print(f"Output (Array): {checkInclusion_array(s1_1, s2_1)}")
    # Expected: True (contains "ba")
    print()
    
    # Test Case 2: No permutation
    s1_2, s2_2 = "ab", "eidboaoo"
    print(f"Input: s1 = '{s1_2}', s2 = '{s2_2}'")
    print(f"Output: {checkInclusion(s1_2, s2_2)}")
    # Expected: False
    print()
    
    # Test Case 3: Exact match
    s1_3, s2_3 = "abc", "bca"
    print(f"Input: s1 = '{s1_3}', s2 = '{s2_3}'")
    print(f"Output: {checkInclusion(s1_3, s2_3)}")
    # Expected: True
    print()
    
    # Test Case 4: s1 longer than s2
    s1_4, s2_4 = "abc", "ab"
    print(f"Input: s1 = '{s1_4}', s2 = '{s2_4}'")
    print(f"Output: {checkInclusion(s1_4, s2_4)}")
    # Expected: False
    print()
    
    # Test Case 5: All same characters
    s1_5, s2_5 = "aaa", "aaaa"
    print(f"Input: s1 = '{s1_5}', s2 = '{s2_5}'")
    print(f"Output: {checkInclusion(s1_5, s2_5)}")
    # Expected: True
    print()
    
    # Test Case 6: Single character
    s1_6, s2_6 = "a", "ab"
    print(f"Input: s1 = '{s1_6}', s2 = '{s2_6}'")
    print(f"Output: {checkInclusion(s1_6, s2_6)}")
    # Expected: True


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THIS IS BASICALLY "FIND ANY ANAGRAM":
   
   - Find All Anagrams (LC 438) → Return all indices
   - Permutation in String (LC 567) → Return True/False
   
   Same algorithm, just return early when found!

2. PERMUTATION = ANAGRAM:
   
   "Is s1's permutation in s2?" = "Is any anagram of s1 a substring of s2?"
   
   Same frequency count = permutation = anagram

3. SLIDING WINDOW KEY POINTS:
   
   - Window size is FIXED at len(s1)
   - When window > len(s1), shrink from left
   - Check validity at each step

4. OPTIMIZATION - TRACK MATCHES:
   
   Instead of comparing full counters:
   
   Simple: window_count == s1_count  → O(26) comparison
   
   Optimized: formed == required     → O(1) check
   
   Update 'formed' only when frequency changes TO or FROM target.

5. ARRAY-BASED OPTIMIZATION:
   
   Track difference: diff[i] = window_count[i] - s1_count[i]
   
   - When diff[i] == 0, character i matches
   - When all 26 characters have diff == 0, found permutation
   - Track count of matches, update on each add/remove

6. VISUAL EXAMPLE for s1="ab", s2="eidbaooo":
   
   s1_count = {a:1, b:1}
   
   Window sliding through s2:
   [e i] → {e:1, i:1} → matches: 0
   [i d] → {i:1, d:1} → matches: 0  
   [d b] → {d:1, b:1} → matches: 1 (b matches)
   [b a] → {b:1, a:1} → matches: 2 ✓ FOUND!

7. COMMON FOLLOW-UP QUESTIONS:
   
   Q: What's the starting index of the permutation?
   A: Return left pointer when match found
   
   Q: Case insensitive?
   A: Convert both to lowercase
   
   Q: What if we need to find all positions?
   A: That's LC 438 - Find All Anagrams

8. RELATED PROBLEMS:
   - Find All Anagrams in a String (LC 438)
   - Minimum Window Substring (LC 76) - variable window
   - Longest Substring Without Repeating (LC 3)

9. practice TIP:
   
   If interviewer says "optimize your comparison", discuss:
   - Tracking formed/required instead of full comparison
   - Array-based diff tracking
   - Each gives O(1) validity check instead of O(26)

================================================================================
"""
