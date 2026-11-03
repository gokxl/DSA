"""
================================================================================
PROBLEM: Daily Temperatures (LeetCode 739)
Difficulty: Medium | Pattern: Monotonic Stack
================================================================================

PROBLEM STATEMENT:
Given an array of integers temperatures represents the daily temperatures, 
return an array answer such that answer[i] is the number of days you have 
to wait after the ith day to get a warmer temperature. 

If there is no future day for which this is possible, keep answer[i] == 0 instead.

EXAMPLES:
    Input: temperatures = [73,74,75,71,69,72,76,73]
    Output: [1,1,4,2,1,1,0,0]
    
    Explanation:
    - Day 0 (73): Wait 1 day for 74
    - Day 1 (74): Wait 1 day for 75
    - Day 2 (75): Wait 4 days for 76
    - Day 3 (71): Wait 2 days for 72
    - Day 4 (69): Wait 1 day for 72
    - Day 5 (72): Wait 1 day for 76
    - Day 6 (76): No warmer day
    - Day 7 (73): No warmer day

    Input: temperatures = [30,40,50,60]
    Output: [1,1,1,0]

    Input: temperatures = [30,60,90]
    Output: [1,1,0]

CONSTRAINTS:
- 1 <= temperatures.length <= 10^5
- 30 <= temperatures[i] <= 100

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION 1: Monotonic Decreasing Stack (Optimal)
# ============================================================================
def dailyTemperatures(temperatures: List[int]) -> List[int]:
    """
    Use a monotonically decreasing stack storing indices.
    
    When we find a warmer temperature, pop all cooler ones and calculate days.
    
    Why decreasing? Because we're looking for the NEXT GREATER element.
    - If current > stack top, we found the answer for stack top
    - Stack maintains temperatures that haven't found their warmer day yet
    
    Time: O(n) - each element pushed and popped at most once
    Space: O(n) - stack size in worst case
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # Store indices of temperatures waiting for warmer day
    
    for i, temp in enumerate(temperatures):
        # While current temp is warmer than stack top
        while stack and temperatures[stack[-1]] < temp:
            prev_index = stack.pop()
            result[prev_index] = i - prev_index
        
        stack.append(i)
    
    return result


# ============================================================================
# SOLUTION 2: Process from Right to Left
# ============================================================================
def dailyTemperatures_right(temperatures: List[int]) -> List[int]:
    """
    Process from right to left.
    Use stack to track future temperatures.
    
    Time: O(n)
    Space: O(n)
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # Stack of (temperature, index)
    
    for i in range(n - 1, -1, -1):
        temp = temperatures[i]
        
        # Remove all temperatures <= current (they can't be the answer)
        while stack and stack[-1][0] <= temp:
            stack.pop()
        
        if stack:
            result[i] = stack[-1][1] - i
        
        stack.append((temp, i))
    
    return result


# ============================================================================
# SOLUTION 3: Brute Force (For comparison)
# ============================================================================
def dailyTemperatures_brute(temperatures: List[int]) -> List[int]:
    """
    Brute force: For each day, scan forward to find warmer day.
    
    Time: O(n^2)
    Space: O(1) excluding result
    """
    n = len(temperatures)
    result = [0] * n
    
    for i in range(n):
        for j in range(i + 1, n):
            if temperatures[j] > temperatures[i]:
                result[i] = j - i
                break
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard example
    temps1 = [73, 74, 75, 71, 69, 72, 76, 73]
    print(f"Input: {temps1}")
    print(f"Output (Stack): {dailyTemperatures(temps1)}")
    print(f"Output (Right): {dailyTemperatures_right(temps1)}")
    # Expected: [1, 1, 4, 2, 1, 1, 0, 0]
    print()
    
    # Test Case 2: Increasing temperatures
    temps2 = [30, 40, 50, 60]
    print(f"Input: {temps2}")
    print(f"Output: {dailyTemperatures(temps2)}")
    # Expected: [1, 1, 1, 0]
    print()
    
    # Test Case 3: Decreasing temperatures
    temps3 = [60, 50, 40, 30]
    print(f"Input: {temps3}")
    print(f"Output: {dailyTemperatures(temps3)}")
    # Expected: [0, 0, 0, 0]
    print()
    
    # Test Case 4: All same
    temps4 = [50, 50, 50, 50]
    print(f"Input: {temps4}")
    print(f"Output: {dailyTemperatures(temps4)}")
    # Expected: [0, 0, 0, 0]
    print()
    
    # Test Case 5: Single element
    temps5 = [70]
    print(f"Input: {temps5}")
    print(f"Output: {dailyTemperatures(temps5)}")
    # Expected: [0]
    print()
    
    # Test Case 6: Two elements
    temps6 = [30, 60]
    print(f"Input: {temps6}")
    print(f"Output: {dailyTemperatures(temps6)}")
    # Expected: [1, 0]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. MONOTONIC STACK PATTERN:
   
   "Find the NEXT GREATER element" → Monotonic DECREASING stack
   "Find the NEXT SMALLER element" → Monotonic INCREASING stack
   
   Daily Temperatures = Next Greater Element with distance

2. WHY DECREASING STACK?
   
   Stack stores indices of elements waiting for their "answer".
   
   - If stack is decreasing, all elements need a LARGER value
   - When we find a larger value, pop all smaller ones
   - Calculate the distance for each popped element

3. VISUAL WALKTHROUGH for [73, 74, 75, 71, 69, 72, 76, 73]:
   
   i=0, temp=73: stack=[] → push 0, stack=[0]
   i=1, temp=74: 74>73, pop 0, result[0]=1-0=1, push 1, stack=[1]
   i=2, temp=75: 75>74, pop 1, result[1]=2-1=1, push 2, stack=[2]
   i=3, temp=71: 71<75, push 3, stack=[2,3]
   i=4, temp=69: 69<71, push 4, stack=[2,3,4]
   i=5, temp=72: 72>69, pop 4, result[4]=5-4=1
                 72>71, pop 3, result[3]=5-3=2
                 72<75, push 5, stack=[2,5]
   i=6, temp=76: 76>72, pop 5, result[5]=6-5=1
                 76>75, pop 2, result[2]=6-2=4
                 push 6, stack=[6]
   i=7, temp=73: 73<76, push 7, stack=[6,7]
   
   Remaining in stack (6, 7) have result[6]=result[7]=0

4. STACK INVARIANT:
   
   At any point, stack contains indices in DECREASING order of temperature.
   
   temperatures[stack[i]] > temperatures[stack[i+1]] for all i

5. WHY O(n)?
   
   Each element is pushed exactly once and popped at most once.
   Total operations = 2n = O(n)

6. TEMPLATE FOR NEXT GREATER:

   def nextGreater(nums):
       n = len(nums)
       result = [-1] * n  # or 0 for this problem
       stack = []
       
       for i in range(n):
           while stack and nums[stack[-1]] < nums[i]:
               idx = stack.pop()
               result[idx] = nums[i]  # or i - idx for distance
           stack.append(i)
       
       return result

7. VARIATIONS:
   
   - Next Greater Element I (LC 496): Simple next greater
   - Next Greater Element II (LC 503): Circular array
   - Daily Temperatures (this): Next greater with distance
   - Online Stock Span (LC 901): Previous greater (span)

8. RELATED PROBLEMS:
   - Next Greater Element I, II, III
   - Online Stock Span
   - Largest Rectangle in Histogram (LC 84)
   - Sum of Subarray Minimums (LC 907)

9. practice TIP:
   
   Draw the stack state at each step. It really helps visualize:
   
   Index:  0   1   2   3   4   5   6   7
   Temp:   73  74  75  71  69  72  76  73
   Stack:  [0]→[1]→[2]→[2,3]→[2,3,4]→[2,5]→[6]→[6,7]

10. COMMON MISTAKES:
    - Storing values instead of indices in stack
    - Wrong comparison (< vs <=)
    - Forgetting that remaining elements in stack have 0 as answer

================================================================================
"""
