"""
================================================================================
PROBLEM: Longest Substring Without Repeating Characters (LeetCode 3)
Difficulty: Medium | Pattern: Sliding Window + HashSet/HashMap
================================================================================

PROBLEM STATEMENT:
Given a string s, find the length of the longest substring without repeating characters.

EXAMPLES:
    Input: s = "abcabcbb"
    Output: 3
    Explanation: "abc" is the longest substring without repeating characters.

    Input: s = "bbbbb"
    Output: 1
    Explanation: "b" is the longest, length is 1.

    Input: s = "pwwkew"
    Output: 3
    Explanation: "wke" is the longest. "pwke" is a subsequence, not substring.

    Input: s = ""
    Output: 0

CONSTRAINTS:
- 0 <= s.length <= 5 * 10^4
- s consists of English letters, digits, symbols and spaces

================================================================================
"""


# ============================================================================
# SOLUTION 1: Sliding Window with HashSet (Most Intuitive)
# ============================================================================
def lengthOfLongestSubstring_set(s: str) -> int:
    """
    Expand window to right, shrink from left when duplicate found.
    Use a set to track characters in current window.
    
    Time: O(n) - each character visited at most twice
    Space: O(min(m, n)) where m is charset size (26 for lowercase)
    """
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        # Shrink window until no duplicate
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character
        char_set.add(s[right])
        
        # Update max length
        max_length = max(max_length, right - left + 1)
    
    return max_length


# ============================================================================
# SOLUTION 2: Sliding Window with HashMap (Optimal - Jump directly)
# ============================================================================
def lengthOfLongestSubstring(s: str) -> int:
    """
    Use a hashmap to store the last index of each character.
    When duplicate found, jump left pointer directly to position after the duplicate.
    
    Key insight: No need to shrink one by one, just jump!
    
    Time: O(n) - single pass
    Space: O(min(m, n)) where m is charset size
    """
    char_index = {}  # char -> last seen index
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # If char seen before and is within current window
        if char in char_index and char_index[char] >= left:
            # Jump left to position after the previous occurrence
            left = char_index[char] + 1
        
        # Update last seen index
        char_index[char] = right
        
        # Update max length
        max_length = max(max_length, right - left + 1)
    
    return max_length


# ============================================================================
# SOLUTION 3: Using Array for ASCII (Space optimized for ASCII)
# ============================================================================
def lengthOfLongestSubstring_array(s: str) -> int:
    """
    Use an array of size 128 (ASCII) instead of hashmap.
    Store -1 for unseen characters, index for seen ones.
    
    Time: O(n)
    Space: O(128) = O(1) for ASCII charset
    """
    # Index array: last seen position of each ASCII character
    last_seen = [-1] * 128
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # If character was seen and is in current window
        if last_seen[ord(char)] >= left:
            left = last_seen[ord(char)] + 1
        
        last_seen[ord(char)] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard example
    s1 = "abcabcbb"
    print(f"Input: '{s1}'")
    print(f"Output (Set): {lengthOfLongestSubstring_set(s1)}")
    print(f"Output (HashMap): {lengthOfLongestSubstring(s1)}")
    print(f"Output (Array): {lengthOfLongestSubstring_array(s1)}")
    # Expected: 3 ("abc")
    print()
    
    # Test Case 2: All same characters
    s2 = "bbbbb"
    print(f"Input: '{s2}'")
    print(f"Output: {lengthOfLongestSubstring(s2)}")
    # Expected: 1
    print()
    
    # Test Case 3: Multiple substrings of same length
    s3 = "pwwkew"
    print(f"Input: '{s3}'")
    print(f"Output: {lengthOfLongestSubstring(s3)}")
    # Expected: 3 ("wke" or "kew")
    print()
    
    # Test Case 4: Empty string
    s4 = ""
    print(f"Input: '{s4}'")
    print(f"Output: {lengthOfLongestSubstring(s4)}")
    # Expected: 0
    print()
    
    # Test Case 5: All unique
    s5 = "abcdef"
    print(f"Input: '{s5}'")
    print(f"Output: {lengthOfLongestSubstring(s5)}")
    # Expected: 6
    print()
    
    # Test Case 6: With spaces and symbols
    s6 = "a b c d"
    print(f"Input: '{s6}'")
    print(f"Output: {lengthOfLongestSubstring(s6)}")
    # Expected: 3 (e.g., "a b")
    print()
    
    # Test Case 7: Duplicate not in current window
    s7 = "abba"
    print(f"Input: '{s7}'")
    print(f"Output: {lengthOfLongestSubstring(s7)}")
    # Expected: 2 ("ab" or "ba")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. SLIDING WINDOW PATTERN:
   
   This is THE classic sliding window problem!
   
   Window = [left, right]
   - Expand: Move right to include more characters
   - Shrink: Move left when invariant broken (duplicate found)
   
   Invariant: All characters in window are unique

2. TWO APPROACHES:
   
   a) HashSet approach:
      - Set tracks what's in window
      - When duplicate: shrink one by one until no duplicate
      - Simple but O(2n) in worst case
   
   b) HashMap approach:
      - Map stores last index of each char
      - When duplicate: JUMP left directly
      - Optimal O(n)

3. THE KEY OPTIMIZATION:
   
   HashSet version:
       while s[right] in char_set:
           char_set.remove(s[left])
           left += 1
   
   HashMap version:
       if char in char_index and char_index[char] >= left:
           left = char_index[char] + 1
   
   HashMap jumps directly, no while loop needed!

4. CRITICAL EDGE CASE - "abba":
   
   Walking through "abba":
   - right=0 ('a'): char_index={'a':0}, window=[0,0], max=1
   - right=1 ('b'): char_index={'a':0,'b':1}, window=[0,1], max=2
   - right=2 ('b'): duplicate! left=2, char_index={'a':0,'b':2}, max=2
   - right=3 ('a'): 'a' is in map at 0, but 0 < left=2!
                    So 'a' is NOT in current window, don't move left!
                    char_index={'a':3,'b':2}, window=[2,3], max=2
   
   This is why we check: char_index[char] >= left

5. VISUAL WALKTHROUGH for "abcabcbb":
   
   a b c a b c b b
   ^           ^
   L           R    → "abc" → max=3
   
     ^ a found  ^
     L           R  → "bca" → max still 3
   
   Continue sliding...

6. TEMPLATE FOR SIMILAR PROBLEMS:

   def sliding_window(s):
       left = 0
       window_state = {}  # or set
       result = 0
       
       for right, char in enumerate(s):
           # Update window state
           
           # Shrink if needed
           while INVALID_CONDITION:
               # Remove s[left] from state
               left += 1
           
           # Update result
           result = max(result, right - left + 1)
       
       return result

7. COMMON FOLLOW-UP QUESTIONS:
   
   Q: What if we need to find the actual substring, not just length?
   A: Track start index when max is updated
   
   Q: What about "longest substring with at most K distinct"?
   A: Same pattern, but shrink when len(char_count) > k
   
   Q: What if case-insensitive?
   A: Convert to lowercase/uppercase first

8. RELATED PROBLEMS:
   - Longest Substring with At Most K Distinct (LC 340)
   - Longest Repeating Character Replacement (LC 424)
   - Minimum Window Substring (LC 76)
   - Find All Anagrams (LC 438)

================================================================================
"""
