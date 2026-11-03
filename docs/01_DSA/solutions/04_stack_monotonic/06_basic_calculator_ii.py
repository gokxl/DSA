"""
================================================================================
PROBLEM: Basic Calculator II (LeetCode 227)
Difficulty: Medium | Pattern: Stack + Expression
================================================================================

PROBLEM STATEMENT:
Given a string s which represents an expression, evaluate this expression and 
return its value.

The integer division should truncate toward zero.

Note: You are not allowed to use any built-in function which evaluates strings 
as mathematical expressions, such as eval().

EXAMPLES:
    Input: s = "3+2*2"
    Output: 7

    Input: s = " 3/2 "
    Output: 1

    Input: s = " 3+5 / 2 "
    Output: 5

CONSTRAINTS:
- 1 <= s.length <= 3 * 10^5
- s consists of integers and operators ('+', '-', '*', '/') separated by spaces
- All integers are non-negative and fit in a 32-bit integer
- s is guaranteed to be a valid expression

================================================================================
"""


# ============================================================================
# SOLUTION 1: Stack with Deferred Addition (Optimal)
# ============================================================================
def calculate(s: str) -> int:
    """
    Process * and / immediately, defer + and - using stack.
    
    Key insight:
    - * and / have higher precedence, process immediately
    - + and - can wait, push to stack and sum at end
    
    Time: O(n)
    Space: O(n) for stack
    """
    stack = []
    num = 0
    prev_op = '+'  # Start with '+' so first number gets pushed
    
    for i, char in enumerate(s):
        if char.isdigit():
            num = num * 10 + int(char)
        
        # Process when we see an operator or reach end
        if char in '+-*/' or i == len(s) - 1:
            if prev_op == '+':
                stack.append(num)
            elif prev_op == '-':
                stack.append(-num)
            elif prev_op == '*':
                stack.append(stack.pop() * num)
            elif prev_op == '/':
                # Truncate toward zero
                top = stack.pop()
                stack.append(int(top / num))
            
            prev_op = char
            num = 0
    
    return sum(stack)


# ============================================================================
# SOLUTION 2: Two Passes (More intuitive)
# ============================================================================
def calculate_two_pass(s: str) -> int:
    """
    First pass: Parse into tokens
    Second pass: Evaluate with stack
    
    Time: O(n)
    Space: O(n)
    """
    # Parse into tokens
    tokens = []
    num = 0
    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)
        elif char in '+-*/':
            tokens.append(num)
            tokens.append(char)
            num = 0
    tokens.append(num)
    
    # First handle * and /
    stack = []
    i = 0
    while i < len(tokens):
        if tokens[i] == '*':
            stack.append(stack.pop() * tokens[i + 1])
            i += 2
        elif tokens[i] == '/':
            stack.append(int(stack.pop() / tokens[i + 1]))
            i += 2
        else:
            stack.append(tokens[i])
            i += 1
    
    # Then handle + and -
    result = 0
    op = '+'
    for item in stack:
        if item == '+':
            op = '+'
        elif item == '-':
            op = '-'
        else:
            if op == '+':
                result += item
            else:
                result -= item
    
    return result


# ============================================================================
# SOLUTION 3: Without Stack (O(1) space)
# ============================================================================
def calculate_no_stack(s: str) -> int:
    """
    Optimize space by tracking only what we need.
    
    Time: O(n)
    Space: O(1)
    """
    result = 0      # Running sum
    prev_num = 0    # Last number (for * and /)
    curr_num = 0    # Current number being built
    prev_op = '+'   # Previous operator
    
    for i, char in enumerate(s):
        if char.isdigit():
            curr_num = curr_num * 10 + int(char)
        
        if char in '+-*/' or i == len(s) - 1:
            if prev_op == '+':
                result += prev_num
                prev_num = curr_num
            elif prev_op == '-':
                result += prev_num
                prev_num = -curr_num
            elif prev_op == '*':
                prev_num = prev_num * curr_num
            elif prev_op == '/':
                prev_num = int(prev_num / curr_num)
            
            prev_op = char
            curr_num = 0
    
    result += prev_num
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Mixed operators
    s1 = "3+2*2"
    print(f"Input: '{s1}'")
    print(f"Output (Stack): {calculate(s1)}")
    print(f"Output (Two-pass): {calculate_two_pass(s1)}")
    print(f"Output (No-stack): {calculate_no_stack(s1)}")
    # Expected: 7 → 3 + 4
    print()
    
    # Test Case 2: Division
    s2 = " 3/2 "
    print(f"Input: '{s2}'")
    print(f"Output: {calculate(s2)}")
    # Expected: 1
    print()
    
    # Test Case 3: Spaces
    s3 = " 3+5 / 2 "
    print(f"Input: '{s3}'")
    print(f"Output: {calculate(s3)}")
    # Expected: 5 → 3 + 2
    print()
    
    # Test Case 4: Subtraction
    s4 = "1-1+1"
    print(f"Input: '{s4}'")
    print(f"Output: {calculate(s4)}")
    # Expected: 1
    print()
    
    # Test Case 5: Multiple * and /
    s5 = "14/3*2"
    print(f"Input: '{s5}'")
    print(f"Output: {calculate(s5)}")
    # Expected: 8 → (14/3)*2 = 4*2
    print()
    
    # Test Case 6: Single number
    s6 = "42"
    print(f"Input: '{s6}'")
    print(f"Output: {calculate(s6)}")
    # Expected: 42


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE CHALLENGE:
   
   Operator precedence:
   - * and / have higher precedence
   - + and - have lower precedence
   
   "3+2*2" = 3 + (2*2) = 7, not (3+2)*2 = 10

2. THE TRICK - DEFERRED ADDITION:
   
   When we see + or -, we DON'T compute yet.
   We push the number (with sign) to stack.
   
   When we see * or /, we compute immediately with stack top.
   
   Finally, sum everything in stack.

3. WHY PREV_OP PATTERN WORKS:
   
   "3+2*2"
   
   See '3': num=3, prev_op='+', don't process yet
   See '+': Process prev! prev_op='+', push 3, update prev_op='+'
   See '2': num=2, prev_op='+', don't process yet
   See '*': Process prev! prev_op='+', push 2, update prev_op='*'
   See '2': num=2, prev_op='*', don't process yet
   End:     Process prev! prev_op='*', stack[-1]*2, push result
   
   Stack: [3, 4] → sum = 7

4. HANDLING SUBTRACTION:
   
   Push negative number instead of tracking '-':
   
   "5-3+2":
   - Push 5 (with prev_op '+')
   - Push -3 (with prev_op '-')
   - Push 2 (with prev_op '+')
   - Sum: 5 + (-3) + 2 = 4

5. DIVISION TRUNCATION:
   
   int(a / b) truncates toward zero:
   int(7 / 3) = 2
   int(-7 / 3) = -2 (not -3!)

6. PROCESSING AT END:
   
   Don't forget to process the last number!
   Check: `i == len(s) - 1`
   
   This handles the final number after last operator.

7. FOLLOW-UP: BASIC CALCULATOR (LC 224)
   
   Adds parentheses, only + and -:
   - Use recursion or stack of states
   - Process parentheses as sub-expressions

8. RELATED PROBLEMS:
   - Basic Calculator (LC 224) - +, -, ()
   - Basic Calculator III (LC 772) - Full with ()
   - Evaluate Reverse Polish Notation (LC 150)

9. SPACE OPTIMIZATION:
   
   We can avoid stack by tracking:
   - result: sum of all finalized terms
   - prev_num: current term being modified by * or /
   
   Only add to result when we see + or - (and at end)

10. practice TIP:
    
    Walk through "3+2*2" step by step:
    - Show how you defer + operations
    - Show how you process * immediately
    - Demonstrate the stack state at each step

================================================================================
"""
