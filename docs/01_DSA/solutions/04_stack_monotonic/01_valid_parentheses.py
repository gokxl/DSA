"""
================================================================================
PROBLEM: Valid Parentheses (LeetCode 20)
Difficulty: Easy | Pattern: Stack
================================================================================

PROBLEM STATEMENT:
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

EXAMPLES:
    Input: s = "()"
    Output: true

    Input: s = "()[]{}"
    Output: true

    Input: s = "(]"
    Output: false

    Input: s = "([)]"
    Output: false

    Input: s = "{[]}"
    Output: true

CONSTRAINTS:
- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'

================================================================================
"""


# ============================================================================
# SOLUTION 1: Stack with HashMap (Clean)
# ============================================================================
def isValid(s: str) -> bool:
    """
    Use a stack to track opening brackets.
    When closing bracket found, check if it matches top of stack.
    
    Time: O(n)
    Space: O(n) - stack can have all opening brackets
    """
    # Map closing bracket to its corresponding opening bracket
    bracket_map = {
        ')': '(',
        '}': '{',
        ']': '['
    }
    
    stack = []
    
    for char in s:
        if char in bracket_map:
            # It's a closing bracket
            if not stack or stack[-1] != bracket_map[char]:
                return False
            stack.pop()
        else:
            # It's an opening bracket
            stack.append(char)
    
    return len(stack) == 0


# ============================================================================
# SOLUTION 2: Stack with Direct Comparison
# ============================================================================
def isValid_direct(s: str) -> bool:
    """
    Same approach but with direct if-else comparisons.
    
    Time: O(n)
    Space: O(n)
    """
    stack = []
    
    for char in s:
        if char == '(':
            stack.append(')')
        elif char == '{':
            stack.append('}')
        elif char == '[':
            stack.append(']')
        elif not stack or stack.pop() != char:
            return False
    
    return len(stack) == 0


# ============================================================================
# SOLUTION 3: Stack with Early Exit
# ============================================================================
def isValid_optimized(s: str) -> bool:
    """
    Optimization: If odd length, immediately return False.
    
    Time: O(n)
    Space: O(n)
    """
    if len(s) % 2 == 1:
        return False  # Odd length can never be valid
    
    bracket_map = {')': '(', '}': '{', ']': '['}
    stack = []
    
    for char in s:
        if char in '([{':
            stack.append(char)
        else:
            if not stack or stack[-1] != bracket_map[char]:
                return False
            stack.pop()
    
    return not stack


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Simple valid
    s1 = "()"
    print(f"Input: '{s1}'")
    print(f"Output: {isValid(s1)}")
    # Expected: True
    print()
    
    # Test Case 2: Multiple types valid
    s2 = "()[]{}"
    print(f"Input: '{s2}'")
    print(f"Output: {isValid(s2)}")
    # Expected: True
    print()
    
    # Test Case 3: Mismatched types
    s3 = "(]"
    print(f"Input: '{s3}'")
    print(f"Output: {isValid(s3)}")
    # Expected: False
    print()
    
    # Test Case 4: Wrong order
    s4 = "([)]"
    print(f"Input: '{s4}'")
    print(f"Output: {isValid(s4)}")
    # Expected: False
    print()
    
    # Test Case 5: Nested valid
    s5 = "{[]}"
    print(f"Input: '{s5}'")
    print(f"Output: {isValid(s5)}")
    # Expected: True
    print()
    
    # Test Case 6: Complex nested
    s6 = "({[]})"
    print(f"Input: '{s6}'")
    print(f"Output: {isValid(s6)}")
    # Expected: True
    print()
    
    # Test Case 7: Only opening
    s7 = "((("
    print(f"Input: '{s7}'")
    print(f"Output: {isValid(s7)}")
    # Expected: False
    print()
    
    # Test Case 8: Only closing
    s8 = ")))"
    print(f"Input: '{s8}'")
    print(f"Output: {isValid(s8)}")
    # Expected: False


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. STACK PATTERN FOR MATCHING:
   
   Stack is the perfect data structure for matching because:
   - LIFO (Last In First Out) matches the nesting structure
   - Most recent opening bracket must be closed first

2. TWO APPROACHES:
   
   a) Push opening brackets, pop and compare for closing:
      - Stack contains: '(' '{' '['
      - Compare: ')' should match top '('
   
   b) Push EXPECTED closing bracket:
      - When see '(', push ')'
      - When see ')', compare with pop
      - More elegant, one comparison type

3. VISUAL WALKTHROUGH for "{[]}":
   
   char   action          stack
   '{'    push '{'        ['{']
   '['    push '['        ['{', '[']
   ']'    pop, match '['  ['{']
   '}'    pop, match '{'  []
   
   Stack empty → Valid!

4. EDGE CASES:
   
   - Empty string: Valid (convention)
   - Odd length: Always invalid (optimization!)
   - Only opening brackets: Invalid (stack not empty)
   - Only closing brackets: Invalid (stack empty when need to pop)
   - Single bracket: Invalid

5. COMMON MISTAKES:
   
   - Forgetting to check if stack is empty before popping
   - Forgetting to check if stack is empty at the end
   - Wrong bracket mapping

6. VARIATION: MINIMUM REMOVALS TO MAKE VALID
   
   Count unmatched brackets:
   
   def minRemovalsToMakeValid(s):
       stack = []
       for char in s:
           if char == '(':
               stack.append(char)
           elif char == ')':
               if stack and stack[-1] == '(':
                   stack.pop()
               else:
                   stack.append(char)
       return len(stack)

7. VARIATION: GENERATE ALL VALID COMBINATIONS (LC 22)
   
   Use backtracking with counts:
   - Track open_count and close_count
   - Can add '(' if open_count < n
   - Can add ')' if close_count < open_count

8. RELATED PROBLEMS:
   - Generate Parentheses (LC 22)
   - Minimum Remove to Make Valid (LC 1249)
   - Longest Valid Parentheses (LC 32)
   - Score of Parentheses (LC 856)

9. HOW TO EXPLAIN IT:
   
   Always mention the optimization for odd length strings.
   Shows attention to edge cases and optimization thinking.

10. TIME COMPLEXITY:
    
    - Time: O(n) - single pass through string
    - Space: O(n) - worst case stack has n/2 opening brackets

================================================================================
"""
