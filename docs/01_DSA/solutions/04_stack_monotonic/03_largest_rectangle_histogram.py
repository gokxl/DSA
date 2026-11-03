"""
================================================================================
PROBLEM: Largest Rectangle in Histogram (LeetCode 84)
Difficulty: Hard | Pattern: Monotonic Stack
================================================================================

PROBLEM STATEMENT:
Given an array of integers heights representing the histogram's bar height 
where the width of each bar is 1, return the area of the largest rectangle 
in the histogram.

EXAMPLES:
    Input: heights = [2,1,5,6,2,3]
    Output: 10
    Explanation: 
        The largest rectangle is formed by bars at index 2 and 3 (heights 5, 6)
        with width 2. Area = 5 * 2 = 10
        
                  6
              5   █
              █   █
              █   █   3
          2   █   █ 2 █
          █ 1 █   █ █ █
          █ █ █   █ █ █
          0 1 2 3 4 5

    Input: heights = [2,4]
    Output: 4

CONSTRAINTS:
- 1 <= heights.length <= 10^5
- 0 <= heights[i] <= 10^4

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION 1: Monotonic Increasing Stack (Optimal)
# ============================================================================
def largestRectangleArea(heights: List[int]) -> int:
    """
    Use a monotonically INCREASING stack.
    
    Key insight: For each bar, we want to know:
    - How far left can it extend? (until a shorter bar)
    - How far right can it extend? (until a shorter bar)
    
    When we encounter a shorter bar, all taller bars in stack
    have found their right boundary.
    
    Time: O(n) - each element pushed and popped once
    Space: O(n)
    """
    heights.append(0)  # Add sentinel to force final processing
    stack = []  # Store indices
    max_area = 0
    
    for i, h in enumerate(heights):
        # Pop all bars taller than current
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            
            # Width calculation:
            # Left boundary: Previous element in stack (or -1 if empty)
            # Right boundary: Current index i
            width = i if not stack else i - stack[-1] - 1
            
            max_area = max(max_area, height * width)
        
        stack.append(i)
    
    heights.pop()  # Restore original array
    return max_area


# ============================================================================
# SOLUTION 2: Without Modifying Input Array
# ============================================================================
def largestRectangleArea_clean(heights: List[int]) -> int:
    """
    Same approach but without modifying the input array.
    Process remaining elements explicitly.
    
    Time: O(n)
    Space: O(n)
    """
    n = len(heights)
    stack = []  # Stores indices
    max_area = 0
    
    for i in range(n + 1):
        # Use 0 as virtual height for processing remaining bars
        h = heights[i] if i < n else 0
        
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        
        stack.append(i)
    
    return max_area


# ============================================================================
# SOLUTION 3: Two-Pass (Find left and right boundaries separately)
# ============================================================================
def largestRectangleArea_two_pass(heights: List[int]) -> int:
    """
    Calculate left and right boundaries for each bar using two passes.
    
    left[i] = index of first shorter bar to the left (or -1)
    right[i] = index of first shorter bar to the right (or n)
    width[i] = right[i] - left[i] - 1
    
    Time: O(n)
    Space: O(n)
    """
    n = len(heights)
    left = [-1] * n   # First shorter bar to left
    right = [n] * n   # First shorter bar to right
    
    # Calculate left boundaries
    stack = []
    for i in range(n):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    
    # Calculate right boundaries
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
    
    # Calculate max area
    max_area = 0
    for i in range(n):
        width = right[i] - left[i] - 1
        max_area = max(max_area, heights[i] * width)
    
    return max_area


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard example
    heights1 = [2, 1, 5, 6, 2, 3]
    print(f"Input: {heights1}")
    print(f"Output (Stack): {largestRectangleArea(heights1)}")
    print(f"Output (Clean): {largestRectangleArea_clean(heights1)}")
    print(f"Output (Two-pass): {largestRectangleArea_two_pass(heights1)}")
    # Expected: 10
    print()
    
    # Test Case 2: Two bars
    heights2 = [2, 4]
    print(f"Input: {heights2}")
    print(f"Output: {largestRectangleArea(heights2)}")
    # Expected: 4
    print()
    
    # Test Case 3: Single bar
    heights3 = [5]
    print(f"Input: {heights3}")
    print(f"Output: {largestRectangleArea(heights3)}")
    # Expected: 5
    print()
    
    # Test Case 4: Increasing heights
    heights4 = [1, 2, 3, 4, 5]
    print(f"Input: {heights4}")
    print(f"Output: {largestRectangleArea(heights4)}")
    # Expected: 9 (3 bars of height 3, or similar)
    print()
    
    # Test Case 5: Decreasing heights
    heights5 = [5, 4, 3, 2, 1]
    print(f"Input: {heights5}")
    print(f"Output: {largestRectangleArea(heights5)}")
    # Expected: 9
    print()
    
    # Test Case 6: All same height
    heights6 = [4, 4, 4, 4]
    print(f"Input: {heights6}")
    print(f"Output: {largestRectangleArea(heights6)}")
    # Expected: 16
    print()
    
    # Verification
    print("\nVerification for [2,1,5,6,2,3]:")
    print("Possible rectangles:")
    print("- Height 1, width 6: 6")
    print("- Height 2, width 4: 8 (indices 0,4,5)")
    print("- Height 5, width 2: 10 (indices 2,3) ← Maximum")
    print("- Height 6, width 1: 6")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. PROBLEM TRANSLATION:
   
   "Find largest rectangle" = 
   For each bar, find how far left and right it can extend.
   
   A bar can extend until it hits a SHORTER bar.
   → This is a "Previous/Next Smaller Element" problem!

2. WHY MONOTONIC INCREASING STACK?
   
   We want to find the first shorter bar on left/right.
   
   Stack stores bars in increasing order.
   When we see a shorter bar:
   - All taller bars in stack have found their right boundary
   - Pop them and calculate area

3. WIDTH CALCULATION (Tricky!):
   
   When we pop index j:
   - Right boundary = current index i
   - Left boundary = new stack top (or -1 if empty)
   - Width = i - left_boundary - 1
   
   Why stack[-1]? Because everything between was taller and already popped!

4. VISUAL WALKTHROUGH for [2, 1, 5, 6, 2, 3]:
   
   Add sentinel 0 at end: [2, 1, 5, 6, 2, 3, 0]
   
   i=0: h=2, stack=[0]
   i=1: h=1, pop 0, area=2*(1-(-1)-1)=2*1=2, stack=[1]
   i=2: h=5, stack=[1,2]
   i=3: h=6, stack=[1,2,3]
   i=4: h=2, pop 3, area=6*(4-2-1)=6*1=6
              pop 2, area=5*(4-1-1)=5*2=10 ← MAX
              stack=[1,4]
   i=5: h=3, stack=[1,4,5]
   i=6: h=0 (sentinel)
              pop 5, area=3*(6-4-1)=3*1=3
              pop 4, area=2*(6-1-1)=2*4=8
              pop 1, area=1*(6-(-1)-1)=1*6=6

5. THE SENTINEL TRICK:
   
   Adding 0 at the end ensures all bars get processed.
   Every bar is eventually popped because 0 is shorter than any bar.

6. COMMON MISTAKES:
   
   - Wrong width formula (forgetting the -1)
   - Not handling empty stack case
   - Off-by-one errors

7. RELATED PROBLEMS:
   
   - Maximal Rectangle (LC 85) - Build histogram for each row
   - Trapping Rain Water (LC 42) - Uses similar stack approach
   - Container With Most Water (LC 11) - Different, uses two pointers

8. MAXIMAL RECTANGLE IN MATRIX (LC 85):
   
   For each row, build a histogram:
   - If cell is 1, add to height
   - If cell is 0, reset height to 0
   
   Then apply Largest Rectangle in Histogram to each row!
   
   def maximalRectangle(matrix):
       if not matrix: return 0
       heights = [0] * len(matrix[0])
       max_area = 0
       for row in matrix:
           for j in range(len(row)):
               heights[j] = heights[j] + 1 if row[j] == '1' else 0
           max_area = max(max_area, largestRectangleArea(heights))
       return max_area

9. COMPLEXITY:
   
   - Time: O(n) - each bar pushed and popped once
   - Space: O(n) - stack size

10. HOW TO EXPLAIN IT:
    
    Draw the histogram! Label each bar with its index.
    For the popped bar, draw the rectangle it creates.
    This makes the width calculation crystal clear.

================================================================================
"""
