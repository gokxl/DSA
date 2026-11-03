"""
================================================================================
PROBLEM: Decode String (LeetCode 394)
Difficulty: Medium | Pattern: Stack + String
================================================================================

PROBLEM STATEMENT:
Given an encoded string, return its decoded string.

The encoding rule is: k[encoded_string], where the encoded_string inside the 
square brackets is being repeated exactly k times. Note that k is guaranteed 
to be a positive integer.

You may assume that the input string is always valid; there are no extra white 
spaces, square brackets are well-formed, etc.

EXAMPLES:
    Input: s = "3[a]2[bc]"
    Output: "aaabcbc"

    Input: s = "3[a2[c]]"
    Output: "accaccacc"
    Explanation: "a2[c]" = "acc", repeated 3 times = "accaccacc"

    Input: s = "2[abc]3[cd]ef"
    Output: "abcabccdcdcdef"

    Input: s = "abc3[cd]xyz"
    Output: "abccdcdcdxyz"

CONSTRAINTS:
- 1 <= s.length <= 30
- s consists of lowercase English letters, digits, and square brackets '[]'
- s is guaranteed to be a valid input
- All integers are in range [1, 300]

================================================================================
"""


# ============================================================================
# SOLUTION 1: Stack Based (Optimal & Intuitive)
# ============================================================================
def decodeString(s: str) -> str:
    """
    Use stack to handle nested brackets.
    
    Stack stores: (previous_string, repeat_count) pairs
    
    Time: O(n * max_k) where n is length, max_k is max repeat count
    Space: O(n) for stack and result string
    """
    stack = []
    curr_str = ""
    curr_num = 0
    
    for char in s:
        if char.isdigit():
            # Build multi-digit number
            curr_num = curr_num * 10 + int(char)
        
        elif char == '[':
            # Save current state and start fresh
            stack.append((curr_str, curr_num))
            curr_str = ""
            curr_num = 0
        
        elif char == ']':
            # Pop and apply repetition
            prev_str, repeat_count = stack.pop()
            curr_str = prev_str + curr_str * repeat_count
        
        else:
            # Regular character
            curr_str += char
    
    return curr_str


# ============================================================================
# SOLUTION 2: Recursive DFS
# ============================================================================
def decodeString_recursive(s: str) -> str:
    """
    Process string recursively, treating [...] as sub-problems.
    
    Time: O(n * max_k)
    Space: O(depth) for recursion stack
    """
    def decode(index: int) -> tuple:
        """Returns (decoded_string, next_index)"""
        result = ""
        num = 0
        
        while index < len(s):
            char = s[index]
            
            if char.isdigit():
                num = num * 10 + int(char)
                index += 1
            
            elif char == '[':
                # Recursively decode inner content
                decoded, index = decode(index + 1)
                result += decoded * num
                num = 0
            
            elif char == ']':
                # End of current level, return
                return result, index + 1
            
            else:
                result += char
                index += 1
        
        return result, index
    
    return decode(0)[0]


# ============================================================================
# SOLUTION 3: Two Stacks (Explicit separation)
# ============================================================================
def decodeString_two_stacks(s: str) -> str:
    """
    Use separate stacks for counts and strings.
    
    Time: O(n * max_k)
    Space: O(n)
    """
    count_stack = []
    string_stack = []
    curr_str = ""
    num = 0
    
    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)
        
        elif char == '[':
            count_stack.append(num)
            string_stack.append(curr_str)
            num = 0
            curr_str = ""
        
        elif char == ']':
            repeat = count_stack.pop()
            prev_str = string_stack.pop()
            curr_str = prev_str + curr_str * repeat
        
        else:
            curr_str += char
    
    return curr_str


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Simple repetition
    s1 = "3[a]2[bc]"
    print(f"Input: '{s1}'")
    print(f"Output (Stack): {decodeString(s1)}")
    print(f"Output (Recursive): {decodeString_recursive(s1)}")
    print(f"Output (Two-stacks): {decodeString_two_stacks(s1)}")
    # Expected: "aaabcbc"
    print()
    
    # Test Case 2: Nested brackets
    s2 = "3[a2[c]]"
    print(f"Input: '{s2}'")
    print(f"Output: {decodeString(s2)}")
    # Expected: "accaccacc"
    print()
    
    # Test Case 3: Multiple groups
    s3 = "2[abc]3[cd]ef"
    print(f"Input: '{s3}'")
    print(f"Output: {decodeString(s3)}")
    # Expected: "abcabccdcdcdef"
    print()
    
    # Test Case 4: Mixed with plain text
    s4 = "abc3[cd]xyz"
    print(f"Input: '{s4}'")
    print(f"Output: {decodeString(s4)}")
    # Expected: "abccdcdcdxyz"
    print()
    
    # Test Case 5: Deeply nested
    s5 = "2[a2[b2[c]]]"
    print(f"Input: '{s5}'")
    print(f"Output: {decodeString(s5)}")
    # Expected: "abccbccabccbcc"
    print()
    
    # Test Case 6: Multi-digit number
    s6 = "10[a]"
    print(f"Input: '{s6}'")
    print(f"Output: {decodeString(s6)}")
    # Expected: "aaaaaaaaaa" (10 a's)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE KEY INSIGHT - STACK FOR NESTING:
   
   When we see '[', we're entering a new level.
   When we see ']', we're completing a level.
   
   Stack naturally handles this nesting!

2. WHAT TO STORE IN STACK:
   
   When entering '[', we need to remember:
   - Previous string (to concatenate with)
   - Repeat count (how many times to repeat inner)
   
   Stack stores: (prev_string, repeat_count)

3. WALKTHROUGH "3[a2[c]]":
   
   '3': num = 3
   '[': push("", 3), curr = "", num = 0
   'a': curr = "a"
   '2': num = 2
   '[': push("a", 2), curr = "", num = 0
   'c': curr = "c"
   ']': pop("a", 2), curr = "a" + "c"*2 = "acc"
   ']': pop("", 3), curr = "" + "acc"*3 = "accaccacc"

4. HANDLE MULTI-DIGIT NUMBERS:
   
   "10[a]" → repeat 10 times, not 1!
   
   num = num * 10 + int(char)
   
   This builds numbers digit by digit.

5. EDGE CASES:
   
   - Plain text without brackets: "abc" → "abc"
   - Multiple groups: "2[a]3[b]" → "aabbb"
   - Text before/after brackets: "x2[a]y" → "xaay"

6. WHY TWO STACKS PATTERN:
   
   Cleaner separation:
   - count_stack: stores repeat counts
   - string_stack: stores previous strings
   
   Same logic, just more explicit.

7. RECURSIVE APPROACH:
   
   Think of [...] as a sub-problem:
   
   def decode(i):
       while not ']':
           if '[': recursively decode
           else: add to result
       return result, next_index

8. COMMON MISTAKES:
   
   ❌ Forgetting to reset curr_str after '['
   ❌ Not handling multi-digit numbers
   ❌ Wrong order in concatenation: prev_str + curr_str * k
   
   Correct order matters!
   "a3[b]" → "a" + "bbb" = "abbb"

9. STRING BUILDING EFFICIENCY:
   
   In Python, string += is O(n) per operation.
   This is usually acceptable.
   
   For production, use list and ''.join():
   result = []
   result.append(char)
   return ''.join(result)

10. FOLLOW-UP QUESTIONS:
    
    Q: What if invalid input?
    A: Add validation - count brackets, check format
    
    Q: What if very large repeat counts?
    A: Check for memory limits, use generators
    
    Q: Encode string (reverse)?
    A: Find repeated patterns, use compression

================================================================================
"""
