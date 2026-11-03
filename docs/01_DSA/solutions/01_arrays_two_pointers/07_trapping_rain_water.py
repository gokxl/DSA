"""
================================================================================
PROBLEM: Trapping Rain Water (LeetCode 42)
Difficulty: Hard | Pattern: Two Pointers / DP / Monotonic Stack
================================================================================

PROBLEM STATEMENT:
Given n non-negative integers representing an elevation map where the width 
of each bar is 1, compute how much water it can trap after raining.

EXAMPLES:
    Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
    Output: 6
    Explanation: 
        The elevation map looks like:
        
              3
          2   █ 2   2
        1 █ 2 █ █ 1 █ █ 1
        █ █ █ █ █ █ █ █ █ █ █
        0 1 0 2 1 0 1 3 2 1 2 1
        
        Water trapped (6 units shown as ~):
              3
          2 ~ █ 2 ~ 2
        1 █ 2 █ █ 1 █ █ 1
        █ █ █ █ █ █ █ █ █ █ █

    Input: height = [4,2,0,3,2,5]
    Output: 9

CONSTRAINTS:
- n == height.length
- 1 <= n <= 2 * 10^4
- 0 <= height[i] <= 10^5

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION 1: Two Pointers (Optimal - O(1) space)
# ============================================================================
def trap(height: List[int]) -> int:
    """
    Key insight: Water at position i = min(max_left, max_right) - height[i]
    
    Use two pointers from both ends.
    Process the side with smaller max height.
    
    Why this works:
    - If left_max < right_max, we KNOW water at left is bounded by left_max
    - We don't need to know the actual right_max (it's >= right_max so far)
    
    Time: O(n) - single pass
    Space: O(1) - just pointers
    """
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            # Process left side
            if height[left] >= left_max:
                left_max = height[left]  # Update max, no water here
            else:
                water += left_max - height[left]  # Water bounded by left_max
            left += 1
        else:
            # Process right side
            if height[right] >= right_max:
                right_max = height[right]  # Update max, no water here
            else:
                water += right_max - height[right]  # Water bounded by right_max
            right -= 1
    
    return water


# ============================================================================
# SOLUTION 2: Dynamic Programming (Pre-compute left/right max)
# ============================================================================
def trap_dp(height: List[int]) -> int:
    """
    Pre-compute:
    - left_max[i] = max height to the left of i (including i)
    - right_max[i] = max height to the right of i (including i)
    
    Water at i = min(left_max[i], right_max[i]) - height[i]
    
    Time: O(n) - three passes
    Space: O(n) - two arrays
    """
    if not height:
        return 0
    
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n
    
    # Compute left max for each position
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])
    
    # Compute right max for each position
    right_max[n-1] = height[n-1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], height[i])
    
    # Calculate water at each position
    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]
    
    return water


# ============================================================================
# SOLUTION 3: Monotonic Stack
# ============================================================================
def trap_stack(height: List[int]) -> int:
    """
    Use a decreasing stack to find "valleys".
    When we find a taller bar, we can trap water.
    
    Stack stores indices of bars in decreasing order.
    When we see a taller bar:
    - Pop the valley (bounded bar)
    - Calculate water trapped with the valley as bottom
    
    Time: O(n) - each element pushed/popped once
    Space: O(n) - stack size
    """
    stack = []  # Store indices
    water = 0
    
    for i, h in enumerate(height):
        # While current bar is taller than stack top
        while stack and height[stack[-1]] < h:
            bottom_idx = stack.pop()  # This is the valley
            
            if not stack:
                break  # No left boundary
            
            left_idx = stack[-1]
            
            # Width of water
            width = i - left_idx - 1
            
            # Height of water = min of boundaries - valley height
            bounded_height = min(height[left_idx], h) - height[bottom_idx]
            
            water += width * bounded_height
        
        stack.append(i)
    
    return water


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard example
    height1 = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"Input: {height1}")
    print(f"Output (Two Pointers): {trap(height1)}")
    print(f"Output (DP): {trap_dp(height1)}")
    print(f"Output (Stack): {trap_stack(height1)}")
    # Expected: 6
    print()
    
    # Test Case 2: Another example
    height2 = [4, 2, 0, 3, 2, 5]
    print(f"Input: {height2}")
    print(f"Output (Two Pointers): {trap(height2)}")
    print(f"Output (DP): {trap_dp(height2)}")
    print(f"Output (Stack): {trap_stack(height2)}")
    # Expected: 9
    print()
    
    # Test Case 3: No water
    height3 = [1, 2, 3, 4]  # Ascending
    print(f"Input: {height3}")
    print(f"Output (Two Pointers): {trap(height3)}")
    # Expected: 0
    print()
    
    # Test Case 4: Single valley
    height4 = [3, 0, 3]
    print(f"Input: {height4}")
    print(f"Output (Two Pointers): {trap(height4)}")
    # Expected: 3
    print()
    
    # Test Case 5: Multiple valleys
    height5 = [5, 2, 1, 2, 1, 5]
    print(f"Input: {height5}")
    print(f"Output (Two Pointers): {trap(height5)}")
    # Expected: 14
    print()
    
    # Test Case 6: Empty or single element
    print(f"Empty: {trap([])}")  # 0
    print(f"Single: {trap([5])}")  # 0
    print(f"Two: {trap([3, 3])}")  # 0


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. CORE FORMULA (Understand this first!):
   
   Water at position i = min(left_max, right_max) - height[i]
   
   Why? Water level is bounded by the shorter of two surrounding walls.
   If height[i] >= water level, no water can be trapped.

2. THREE APPROACHES (Know all three!):
   
   a) DP Approach (easiest to understand):
      - Pre-compute left_max[] and right_max[]
      - Apply formula at each position
      - Space: O(n)
   
   b) Two Pointers (optimal):
      - Process from both ends
      - Always process the side with smaller max
      - Key insight: if left_max < right_max, water is bounded by left_max
      - Space: O(1)
   
   c) Monotonic Stack (layer by layer):
      - Process "valleys" when taller bar is found
      - Calculate water layer by layer
      - Space: O(n)

3. WHY TWO POINTERS WORKS:
   
   At each step, we process either left or right based on:
   - If height[left] < height[right]:
     - right_max >= height[right] > height[left]
     - So right_max >= left_max's potential
     - Water at left is bounded by left_max
   - Similar logic for right side

4. STACK APPROACH VISUALIZED:
   
   height = [3, 0, 2, 0, 4]
   
   Step by step:
   - Push 0 (height 3)
   - Push 1 (height 0) - smaller, push
   - See 2 (height 2) - larger than 0
     - Pop 1, bottom=0, left=0, right=2
     - Water = (2-0-1) * min(3,2)-0 = 1*2 = 2
   - Push 2 (height 2)
   - Push 3 (height 0)
   - See 4 (height 4)
     - Pop 3, bottom=0, calculate water
     - Pop 2, calculate water with left=0

5. COMMON MISTAKES:
   - Forgetting edge cases (empty, single element)
   - Off-by-one in width calculation for stack
   - Not handling the case where no left/right boundary exists

6. FOLLOW-UP QUESTIONS:
   
   Q: What if the bars have different widths?
   A: Need to modify to consider width in calculations
   
   Q: Trapping Water 3D (LC 407)?
   A: Use BFS + Min Heap from boundaries inward

7. COMPLEXITY COMPARISON:
   | Approach      | Time    | Space |
   |---------------|---------|-------|
   | DP            | O(n)    | O(n)  |
   | Two Pointers  | O(n)    | O(1)  | ← Optimal
   | Stack         | O(n)    | O(n)  |

8. PATTERN RECOGNITION:
   - "Min of maxes" → Two pointer or DP with prefix/suffix
   - "Find valleys" → Monotonic stack
   - "Water between bars" → Similar to Container With Most Water

================================================================================
"""
