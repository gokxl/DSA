"""
================================================================================
PROBLEM: Letter Combinations of a Phone Number (LeetCode 17)
Difficulty: Medium | Pattern: Backtracking
================================================================================

PROBLEM STATEMENT:
Given a string containing digits from 2-9 inclusive, return all possible letter 
combinations that the number could represent. Return the answer in any order.

A mapping of digits to letters (just like on the telephone buttons):
2 -> "abc"
3 -> "def"
4 -> "ghi"
5 -> "jkl"
6 -> "mno"
7 -> "pqrs"
8 -> "tuv"
9 -> "wxyz"

EXAMPLES:
    Input: digits = "23"
    Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

    Input: digits = ""
    Output: []

    Input: digits = "2"
    Output: ["a","b","c"]

CONSTRAINTS:
- 0 <= digits.length <= 4
- digits[i] is a digit in the range ['2', '9']

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Backtracking (Classic)
# ============================================================================
def letterCombinations(digits: str) -> List[str]:
    """
    Backtracking: at each digit, try all its letters.
    
    Time: O(4^n × n) - up to 4 letters per digit, n digits
    Space: O(n) for recursion
    """
    if not digits:
        return []
    
    phone_map = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    
    result = []
    
    def backtrack(index: int, current: List[str]) -> None:
        if index == len(digits):
            result.append(''.join(current))
            return
        
        for letter in phone_map[digits[index]]:
            current.append(letter)
            backtrack(index + 1, current)
            current.pop()
    
    backtrack(0, [])
    return result


# ============================================================================
# SOLUTION 2: Iterative (BFS-like)
# ============================================================================
def letterCombinations_iterative(digits: str) -> List[str]:
    """
    Build combinations iteratively.
    
    Start with [''], then for each digit, extend all combinations.
    
    Time: O(4^n × n)
    Space: O(4^n) for result
    """
    if not digits:
        return []
    
    phone_map = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    
    result = ['']
    
    for digit in digits:
        new_result = []
        for combo in result:
            for letter in phone_map[digit]:
                new_result.append(combo + letter)
        result = new_result
    
    return result


# ============================================================================
# SOLUTION 3: Using itertools.product
# ============================================================================
from itertools import product

def letterCombinations_product(digits: str) -> List[str]:
    """
    Use Cartesian product of letter choices.
    
    Time: O(4^n × n)
    Space: O(4^n)
    """
    if not digits:
        return []
    
    phone_map = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    
    groups = [phone_map[d] for d in digits]
    return [''.join(combo) for combo in product(*groups)]


# ============================================================================
# SOLUTION 4: Using BFS with Queue
# ============================================================================
from collections import deque

def letterCombinations_bfs(digits: str) -> List[str]:
    """
    BFS approach using queue.
    
    Time: O(4^n × n)
    Space: O(4^n)
    """
    if not digits:
        return []
    
    phone_map = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    
    queue = deque([''])
    
    for digit in digits:
        size = len(queue)
        for _ in range(size):
            combo = queue.popleft()
            for letter in phone_map[digit]:
                queue.append(combo + letter)
    
    return list(queue)


# ============================================================================
# SOLUTION 5: Recursive without explicit backtracking
# ============================================================================
def letterCombinations_recursive(digits: str) -> List[str]:
    """
    Recursive approach building strings directly.
    
    Time: O(4^n × n)
    Space: O(n) for recursion + O(4^n) for result
    """
    if not digits:
        return []
    
    phone_map = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }
    
    def combine(index: int, current: str) -> List[str]:
        if index == len(digits):
            return [current]
        
        result = []
        for letter in phone_map[digits[index]]:
            result.extend(combine(index + 1, current + letter))
        return result
    
    return combine(0, '')


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    digits1 = "23"
    print(f"digits = '{digits1}'")
    print(f"Backtrack: {letterCombinations(digits1)}")
    print(f"Iterative: {letterCombinations_iterative(digits1)}")
    # Expected: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
    print()
    
    # Test Case 2: Empty input
    digits2 = ""
    print(f"digits = '{digits2}'")
    print(f"Result: {letterCombinations(digits2)}")
    # Expected: []
    print()
    
    # Test Case 3: Single digit
    digits3 = "2"
    print(f"digits = '{digits3}'")
    print(f"Result: {letterCombinations(digits3)}")
    # Expected: ["a","b","c"]
    print()
    
    # Test Case 4: Digit with 4 letters
    digits4 = "7"
    print(f"digits = '{digits4}'")
    print(f"Result: {letterCombinations(digits4)}")
    # Expected: ["p","q","r","s"]
    print()
    
    # Test Case 5: Three digits
    digits5 = "234"
    print(f"digits = '{digits5}'")
    result = letterCombinations_product(digits5)
    print(f"Result: {len(result)} combinations")
    # Expected: 3 × 3 × 3 = 27 combinations


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THIS IS A CARTESIAN PRODUCT PROBLEM:
   
   Each digit provides a set of choices.
   Result = all combinations of one choice per digit.
   
   "23" → {a,b,c} × {d,e,f} = 9 combinations

2. BACKTRACKING TEMPLATE:
   
   def backtrack(index, current):
       if index == len(digits):
           result.append(current)
           return
       
       for letter in phone_map[digits[index]]:
           current.append(letter)
           backtrack(index + 1, current)
           current.pop()

3. ITERATIVE IS EQUALLY VALID:
   
   Start with ['']
   For each digit, extend each existing combination:
   
   [''] → ['a', 'b', 'c'] → ['ad', 'ae', ..., 'cf']

4. TIME COMPLEXITY:
   
   Each digit has 3 or 4 letters.
   Worst case: 4 letters per digit, n digits → 4^n combinations
   
   Time: O(4^n × n) - generating and copying each combination

5. PHONE MAP:
   
   '2': "abc"    '3': "def"    '4': "ghi"
   '5': "jkl"    '6': "mno"    '7': "pqrs"
   '8': "tuv"    '9': "wxyz"
   
   Note: 7 and 9 have 4 letters!

6. EDGE CASE:
   
   Empty string → return []
   
   Don't forget this check at the start!

7. WHY NOT DFS WITH VISITED?
   
   Unlike graph problems, each decision is independent.
   No need for visited - we're making sequential choices.

8. itertools.product:
   
   product(*groups) generates Cartesian product
   Very Pythonic and efficient!

9. RELATED PROBLEMS:
   
   - Generate Parentheses (LC 22)
   - Combinations (LC 77)
   - Subsets (LC 78)

10. HOW TO EXPLAIN IT:
    
    "This is a Cartesian product problem. At each digit,
    I have 3-4 letter choices. I'll use backtracking to
    generate all combinations.
    
    Time is O(4^n × n) since there are up to 4^n combinations
    and each takes O(n) to build/copy.
    
    Alternative: Build iteratively by extending all existing
    combinations with each new digit's letters."
    
    Mention it's like generating all paths in a tree!

================================================================================
"""
