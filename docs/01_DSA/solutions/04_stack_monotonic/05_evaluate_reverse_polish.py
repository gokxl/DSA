"""
================================================================================
PROBLEM: Evaluate Reverse Polish Notation (LeetCode 150)
Difficulty: Medium | Pattern: Stack
================================================================================

PROBLEM STATEMENT:
You are given an array of strings tokens that represents an arithmetic expression 
in Reverse Polish Notation.

Evaluate the expression. Return an integer that represents the value of the expression.

Note:
- Valid operators are '+', '-', '*', and '/'.
- Each operand may be an integer or another expression.
- Division truncates toward zero.
- The expression is guaranteed to be valid.

EXAMPLES:
    Input: tokens = ["2","1","+","3","*"]
    Output: 9
    Explanation: ((2 + 1) * 3) = 9

    Input: tokens = ["4","13","5","/","+"]
    Output: 6
    Explanation: (4 + (13 / 5)) = 4 + 2 = 6

    Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
    Output: 22

CONSTRAINTS:
- 1 <= tokens.length <= 10^4
- tokens[i] is either an operator or an integer in [-200, 200]

================================================================================
"""

from typing import List
import operator


# ============================================================================
# SOLUTION 1: Stack with Dictionary (Clean)
# ============================================================================
def evalRPN(tokens: List[str]) -> int:
    """
    Use stack to evaluate RPN expression.
    When we see an operator, pop two operands, compute, push result.
    
    Time: O(n)
    Space: O(n) for stack
    """
    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b)  # Truncate toward zero
    }
    
    stack = []
    
    for token in tokens:
        if token in operations:
            # Pop two operands (order matters for - and /)
            b = stack.pop()  # Second operand (top of stack)
            a = stack.pop()  # First operand
            result = operations[token](a, b)
            stack.append(result)
        else:
            stack.append(int(token))
    
    return stack[0]


# ============================================================================
# SOLUTION 2: Stack with If-Else
# ============================================================================
def evalRPN_ifelse(tokens: List[str]) -> int:
    """
    Same approach with explicit if-else statements.
    
    Time: O(n)
    Space: O(n)
    """
    stack = []
    operators = {'+', '-', '*', '/'}
    
    for token in tokens:
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:  # '/'
                # Python division truncates toward negative infinity
                # We need truncation toward zero
                stack.append(int(a / b))
        else:
            stack.append(int(token))
    
    return stack[0]


# ============================================================================
# SOLUTION 3: Using operator module
# ============================================================================
def evalRPN_operator(tokens: List[str]) -> int:
    """
    Using Python's operator module for cleaner function mapping.
    
    Time: O(n)
    Space: O(n)
    """
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': lambda a, b: int(operator.truediv(a, b))
    }
    
    stack = []
    
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    
    return stack[0]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Simple expression
    tokens1 = ["2", "1", "+", "3", "*"]
    print(f"Input: {tokens1}")
    print(f"Output: {evalRPN(tokens1)}")
    # Expected: 9 → (2+1)*3
    print()
    
    # Test Case 2: Division
    tokens2 = ["4", "13", "5", "/", "+"]
    print(f"Input: {tokens2}")
    print(f"Output: {evalRPN(tokens2)}")
    # Expected: 6 → 4 + (13/5) = 4 + 2
    print()
    
    # Test Case 3: Complex expression
    tokens3 = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
    print(f"Input: {tokens3}")
    print(f"Output: {evalRPN(tokens3)}")
    # Expected: 22
    print()
    
    # Test Case 4: Negative numbers
    tokens4 = ["4", "-2", "/"]
    print(f"Input: {tokens4}")
    print(f"Output: {evalRPN(tokens4)}")
    # Expected: -2 (truncate toward zero)
    print()
    
    # Test Case 5: Single number
    tokens5 = ["18"]
    print(f"Input: {tokens5}")
    print(f"Output: {evalRPN(tokens5)}")
    # Expected: 18
    print()
    
    # Test Case 6: Negative result
    tokens6 = ["3", "5", "-"]
    print(f"Input: {tokens6}")
    print(f"Output: {evalRPN(tokens6)}")
    # Expected: -2 → 3-5


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHAT IS RPN (REVERSE POLISH NOTATION)?
   
   Also called "postfix notation":
   - Operators come AFTER operands
   - No parentheses needed
   - Used by HP calculators and some programming languages
   
   Infix:    (2 + 1) * 3
   Postfix:  2 1 + 3 *

2. WHY STACK WORKS:
   
   RPN is designed for stack evaluation:
   - Numbers: Push onto stack
   - Operators: Pop two operands, compute, push result
   
   The last number pushed is the second operand!

3. OPERATOR ORDER MATTERS:
   
   For non-commutative operations (-, /):
   
   tokens = ["a", "b", "-"]
   
   Stack: push a, push b, see '-'
   Pop b (top), pop a
   Result = a - b (NOT b - a)
   
   First popped = second operand

4. DIVISION TRUNCATION:
   
   Python's // truncates toward NEGATIVE infinity
   Problem wants truncation toward ZERO
   
   -7 // 3 = -3 (Python)
   int(-7 / 3) = -2 (toward zero) ← What we want

5. VISUAL WALKTHROUGH for ["2","1","+","3","*"]:
   
   Token   Stack       Action
   "2"     [2]         Push 2
   "1"     [2,1]       Push 1
   "+"     [3]         Pop 1,2; push 2+1=3
   "3"     [3,3]       Push 3
   "*"     [9]         Pop 3,3; push 3*3=9
   
   Result: 9

6. CONVERTING INFIX TO POSTFIX:
   
   Use Shunting-Yard algorithm:
   - Numbers go directly to output
   - Operators go to stack (with precedence rules)
   - Left paren to stack, right paren pops until left paren

7. RELATED PROBLEMS:
   - Basic Calculator (LC 224) - infix with +, -, ()
   - Basic Calculator II (LC 227) - infix with +,-,*,/
   - Basic Calculator III (LC 772) - full expression

8. FOLLOW-UP QUESTIONS:
   
   Q: What if the expression is invalid?
   A: Check for stack underflow when popping
   
   Q: What about unary minus?
   A: Treat as "0 x -" or use special token
   
   Q: How to convert infix to postfix?
   A: Shunting-Yard algorithm

9. COMPLEXITY:
   
   Time: O(n) - process each token once
   Space: O(n) - stack can hold all numbers

10. practice TIP:
    
    Be careful with:
    - Order of operands for subtraction/division
    - Division truncation behavior
    - Negative number handling

================================================================================
"""
